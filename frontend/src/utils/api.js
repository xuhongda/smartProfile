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
export const handleSearch = async (keyword, setSearchLoading, setSearchKeyword, setSearchResults, setActiveMenu) => {
  if (!keyword) return
  
  setSearchLoading(true)
  setSearchKeyword(keyword)
  
  try {
    const response = await fetch(`http://localhost:8000/search?q=${encodeURIComponent(keyword)}`)
    if (!response.ok) {
      throw new Error('搜索失败')
    }
    
    const result = await response.json()
    if (result.success) {
      setSearchResults(result.results)
      setActiveMenu('search')
    } else {
      message.error(result.message, 2) // 2秒
    }
  } catch (error) {
    message.error('搜索失败: ' + error.message, 2) // 2秒
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
export const handleDeleteDocument = async (docId, filename, fetchDocuments, fetchStatistics) => {
  try {
    const response = await fetch(`http://localhost:8000/documents/${docId}`, {
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
    } else {
      message.error(result.message, 2) // 2秒
    }
  } catch (error) {
    message.error('删除失败: ' + error.message, 2) // 2秒
  }
}

// 处理文件预览
export const handleFilePreview = async (source, documents, setFilePreviewLoading, setFilePreviewData, setFilePreviewVisible, getFileTypeInfo) => {
  console.log('开始文件预览:', source)
  setFilePreviewLoading(true)
  try {
    // 检查是否有文档ID
    if (source.id || source.docId) {
      console.log('使用文档ID获取预览')
      const docId = source.id || source.docId
      
      // 调用后端预览API
      const response = await fetch(`http://localhost:8000/preview/${docId}`)
      console.log('响应状态:', response.status)
      if (!response.ok) {
        throw new Error(`无法获取文件预览，状态码: ${response.status}`)
      }
      
      const result = await response.json()
      if (result.success) {
        console.log('后端预览API返回成功')
        setFilePreviewData({
          uri: source.file_path || '',
          fileName: result.filename || source.filename || '未知文件',
          content: result.content,
          fileType: result.file_type,
          contentType: result.content_type
        })
        setFilePreviewVisible(true)
        console.log('设置filePreviewData完成')
        return
      } else {
        throw new Error(result.message || '预览失败')
      }
    }
    
    // 如果没有文档ID，尝试从documents数组中查找
    let filename = source.filename || source.fileName
    if (filename) {
      const doc = documents.find(doc => doc.filename === filename)
      if (doc?.id) {
        console.log('从documents数组获取文档ID')
        const docId = doc.id
        
        // 调用后端预览API
        const response = await fetch(`http://localhost:8000/preview/${docId}`)
        console.log('响应状态:', response.status)
        if (!response.ok) {
          throw new Error(`无法获取文件预览，状态码: ${response.status}`)
        }
        
        const result = await response.json()
        if (result.success) {
          console.log('后端预览API返回成功')
          setFilePreviewData({
            uri: source.file_path || '',
            fileName: result.filename || source.filename || '未知文件',
            content: result.content,
            fileType: result.file_type,
            contentType: result.content_type
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
        console.log('文本文件内容长度:', fileContent.length)
      } else {
        // 对于Word和Excel文件，不读取内容，让前端组件处理
        fileContent = ''
      }
    } else {
      // 对于非文档类型，显示文件信息
      fileContent = `文件类型: ${fileTypeInfo.name}\n文件分类: ${fileTypeInfo.category}\n\n提示: 该文件类型需要在本地打开查看详细内容`
    }
    
    setFilePreviewData({
      uri: fileUrl,
      fileName: filename,
      content: fileContent
    })
    console.log('设置filePreviewData完成')
    setFilePreviewVisible(true)
    console.log('设置filePreviewVisible完成')
  } catch (error) {
    console.error('文件预览失败:', error)
    message.error(`文件预览失败: ${error.message}`, 2) // 2秒
    // 即使出错也显示预览窗口，以便查看错误信息
    setFilePreviewData({
      uri: '',
      fileName: source.filename || '未知文件',
      content: `预览失败: ${error.message}`
    })
    setFilePreviewVisible(true)
  } finally {
    setFilePreviewLoading(false)
    console.log('文件预览加载状态设置为false')
  }
}
