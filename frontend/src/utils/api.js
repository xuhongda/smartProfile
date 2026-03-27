import { message } from 'antd'

// 处理文件上传
export const handleUpload = async (file, onSuccess, onError, onProgress, setUploading, setUploadProgress, fetchDocuments, fetchStatistics) => {
  setUploading(true)
  setUploadProgress(0)
  
  const formData = new FormData()
  formData.append('file', file)
  
  try {
    // 模拟上传进度
    const progressInterval = setInterval(() => {
      setUploadProgress(prev => {
        if (prev >= 90) {
          clearInterval(progressInterval)
          return prev
        }
        return prev + 10
      })
    }, 200)
    
    const response = await fetch('http://localhost:8000/upload', {
      method: 'POST',
      body: formData,
    })
    
    clearInterval(progressInterval)
    setUploadProgress(100)
    
    if (!response.ok) {
      throw new Error('后端服务可能未启动，请检查服务状态')
    }
    
    const result = await response.json()
    if (result.success) {
      message.success(result.message, 2) // 2秒
      // 重新获取文档列表
      fetchDocuments()
      // 重新获取统计数据
      fetchStatistics()
      onSuccess(result)
    } else {
      message.error(result.message, 2) // 2秒
      onError(new Error(result.message))
    }
  } catch (error) {
    message.error('上传失败: ' + error.message, 2) // 2秒
    onError(error)
  } finally {
    setUploading(false)
    setUploadProgress(0)
  }
  
  return false
}

// 处理搜索
export const handleSearch = async (keyword, setSearchLoading, setSearchKeyword, setSearchResults, setActiveMenu, enableAi = false, setAiResponse = null) => {
  if (!keyword) return
  
  setSearchLoading(true)
  setSearchKeyword(keyword)
  
  try {
    let url = `http://localhost:8000/search?q=${encodeURIComponent(keyword)}`
    if (enableAi) {
      url += '&enable_ai=true'
    }
    
    const response = await fetch(url)
    if (!response.ok) {
      throw new Error('搜索失败')
    }
    
    const result = await response.json()
    if (result.success) {
      setSearchResults(result.results)
      setActiveMenu('search')
      // 处理 AI 回答
      if (result.ai_response && setAiResponse) {
        setAiResponse(result.ai_response)
      } else if (setAiResponse) {
        setAiResponse(null)
      }
    } else {
      message.error(result.message, 2) // 2秒
      if (setAiResponse) {
        setAiResponse(null)
      }
    }
  } catch (error) {
    message.error('搜索失败: ' + error.message, 2) // 2秒
    if (setAiResponse) {
      setAiResponse(null)
    }
  } finally {
    setSearchLoading(false)
  }
}

// 获取文档列表
export const fetchDocuments = async (setDocuments) => {
  try {
    const response = await fetch('http://localhost:8000/documents')
    if (!response.ok) {
      throw new Error('后端服务可能未启动，请检查服务状态')
    }
    
    const result = await response.json()
    if (result.success) {
      setDocuments(result.documents)
    } else {
      message.error(result.message, 2) // 2秒
    }
  } catch (error) {
    message.error('获取文档列表失败: ' + error.message, 2) // 2秒
  }
}

// 获取统计数据
export const fetchStatistics = async (documents, setStatistics) => {
  try {
    // 这里我们从文档列表计算统计数据
    if (documents.length > 0) {
      const fileTypeCount = documents.reduce((acc, doc) => {
        acc[doc.file_type] = (acc[doc.file_type] || 0) + 1
        return acc
      }, {})
      
      setStatistics({
        total_documents: documents.length,
        file_type_distribution: fileTypeCount
      })
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 删除文档
export const handleDeleteDocument = async (docUuid, filename, fetchDocuments, fetchStatistics, searchResults = null, setSearchResults = null) => {
  try {
    const response = await fetch(`http://localhost:8000/documents/${docUuid}`, {
      method: 'DELETE'
    })
    
    if (!response.ok) {
      throw new Error('后端服务可能未启动，请检查服务状态')
    }
    
    const result = await response.json()
    if (result.success) {
      message.success(result.message, 2) // 2秒
      // 重新获取文档列表
      fetchDocuments()
      // 重新获取统计数据
      fetchStatistics()
      // 更新搜索结果列表，移除已删除的文档
      if (searchResults && setSearchResults) {
        const updatedSearchResults = searchResults.filter(doc => doc.uuid !== docUuid && doc.id !== docUuid)
        setSearchResults(updatedSearchResults)
      }
    } else {
      message.error(result.message, 2) // 2秒
    }
  } catch (error) {
    message.error('删除失败: ' + error.message, 2) // 2秒
  }
}

// 处理文件预览
let previewRequestId = 0
export const handleFilePreview = async (source, documents, setFilePreviewLoading, setFilePreviewData, setFilePreviewVisible, getFileTypeInfo, keyword = '') => {
  const currentRequestId = ++previewRequestId
  console.log('开始文件预览:', source, '请求ID:', currentRequestId)
  setFilePreviewLoading(true)
  try {
    // 检查是否有文档UUID
    const docUuid = source.uuid
    if (docUuid) {
      console.log('使用文档UUID获取预览:', docUuid)
      
      // 调用后端预览API
      const response = await fetch(`http://localhost:8000/preview/${docUuid}`)
      
      // 检查是否是最新的请求
      if (currentRequestId !== previewRequestId) {
        console.log('跳过旧请求的响应:', currentRequestId)
        return
      }
      
      console.log('响应状态:', response.status)
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('文档不存在，可能已被删除。请刷新页面获取最新文档列表。')
        }
        throw new Error(`无法获取文件预览，状态码: ${response.status}`)
      }
      
      const result = await response.json()
      
      // 检查是否是最新的请求
      if (currentRequestId !== previewRequestId) {
        console.log('跳过旧请求的响应:', currentRequestId)
        return
      }
      
      if (result.success) {
        console.log('后端预览API返回成功')
        setFilePreviewData({
          uri: source.file_path || '',
          fileName: result.filename || source.filename || '未知文件',
          content: result.content,
          fileType: result.file_type,
          contentType: result.content_type,
          keyword: keyword
        })
        setFilePreviewVisible(true)
        console.log('设置filePreviewData完成')
        return
      } else {
        throw new Error(result.message || '预览失败')
      }
    }
    
    // 如果没有文档UUID，尝试从documents数组中查找
    let filename = source.filename || source.fileName
    if (filename) {
      const doc = documents.find(doc => doc.filename === filename)
      const docUuidFromList = doc?.uuid
      if (docUuidFromList) {
        console.log('从documents数组获取文档UUID:', docUuidFromList)
        
        // 调用后端预览API
        const response = await fetch(`http://localhost:8000/preview/${docUuidFromList}`)
        
        // 检查是否是最新的请求
        if (currentRequestId !== previewRequestId) {
          console.log('跳过旧请求的响应:', currentRequestId)
          return
        }
        
        console.log('响应状态:', response.status)
        if (!response.ok) {
          if (response.status === 404) {
            throw new Error('文档不存在，可能已被删除。请刷新页面获取最新文档列表。')
          }
          throw new Error(`无法获取文件预览，状态码: ${response.status}`)
        }
        
        const result = await response.json()
        
        // 检查是否是最新的请求
        if (currentRequestId !== previewRequestId) {
          console.log('跳过旧请求的响应:', currentRequestId)
          return
        }
        
        if (result.success) {
          console.log('后端预览API返回成功')
          setFilePreviewData({
          uri: source.file_path || '',
          fileName: result.filename || source.filename || '未知文件',
          content: result.content,
          fileType: result.file_type,
          contentType: result.content_type,
          keyword: keyword
        })
          setFilePreviewVisible(true)
          console.log('设置filePreviewData完成')
          return
        } else {
          throw new Error(result.message || '预览失败')
        }
      }
    }
    
    // 如果没有文档ID且无法从documents数组中找到，使用旧的方式
    console.log('使用旧方式获取预览')
    if (!filename) {
      throw new Error('文件名不存在')
    }
    
    // 对文件名进行URL编码，处理中文和空格
    const encodedFilename = encodeURIComponent(filename)
    const fileUrl = source.file_path || `http://localhost:8000/uploads/${encodedFilename}`
    console.log('文件预览URL:', fileUrl)
    
    // 从原文件获取内容
    const response = await fetch(fileUrl)
    
    // 检查是否是最新的请求
    if (currentRequestId !== previewRequestId) {
      console.log('跳过旧请求的响应:', currentRequestId)
      return
    }
    
    console.log('响应状态:', response.status)
    if (!response.ok) {
      throw new Error(`无法获取文件内容，状态码: ${response.status}`)
    }
    
    // 根据文件类型处理内容
    const fileTypeInfo = getFileTypeInfo(filename)
    let fileContent = ''
    
    if (fileTypeInfo.category === 'document') {
      if (fileTypeInfo.type === 'txt') {
        // 文本文件直接读取
        fileContent = await response.text()
        
        // 检查是否是最新的请求
        if (currentRequestId !== previewRequestId) {
          console.log('跳过旧请求的响应:', currentRequestId)
          return
        }
        
        console.log('文本文件内容长度:', fileContent.length)
      } else {
        // 对于Word和Excel文件，不读取内容，让前端组件处理
        fileContent = ''
      }
    } else {
      // 对于非文档类型，显示文件信息
      fileContent = `文件类型: ${fileTypeInfo.name}\n文件分类: ${fileTypeInfo.category}\n\n提示: 该文件类型需要在本地打开查看详细内容`
    }
    
    // 检查是否是最新的请求
    if (currentRequestId !== previewRequestId) {
      console.log('跳过旧请求的响应:', currentRequestId)
      return
    }
    
    setFilePreviewData({
      uri: fileUrl,
      fileName: filename,
      content: fileContent,
      keyword: keyword
    })
    console.log('设置filePreviewData完成')
    setFilePreviewVisible(true)
    console.log('设置filePreviewVisible完成')
  } catch (error) {
    // 检查是否是最新的请求
    if (currentRequestId !== previewRequestId) {
      console.log('跳过旧请求的错误:', currentRequestId)
      return
    }
    
    console.error('文件预览失败:', error)
    message.error(`文件预览失败: ${error.message}`, 2) // 2秒
    // 即使出错也显示预览窗口，以便查看错误信息
    setFilePreviewData({
      uri: '',
      fileName: source.filename || '未知文件',
      content: `预览失败: ${error.message}`,
      keyword: keyword
    })
    setFilePreviewVisible(true)
  } finally {
    // 检查是否是最新的请求
    if (currentRequestId === previewRequestId) {
      setFilePreviewLoading(false)
      console.log('文件预览加载状态设置为false')
    }
  }
}
