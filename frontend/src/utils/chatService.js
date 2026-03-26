import { message } from 'antd'

// 处理发送消息
export const handleSendMessage = async (inputValue, setMessages, setInputValue, setChatLoading, setCurrentMessageId, setTypingText, setTypingInterval, aiMode, setAiMode, setSearchLoading) => {
  if (!inputValue.trim()) return
  
  // 添加用户消息
  const userMessage = {
    id: Date.now(),
    role: 'user',
    content: inputValue.trim(),
    timestamp: new Date().toISOString()
  }
  setMessages(prev => [...prev, userMessage])
  setInputValue('')
  setChatLoading(true)
  
  // 模拟AI思考中状态
  const thinkingMessage = {
    id: Date.now() + 1,
    role: 'assistant',
    content: '正在阅读文档...',
    timestamp: new Date().toISOString(),
    isThinking: true
  }
  setMessages(prev => [...prev, thinkingMessage])
  setCurrentMessageId(thinkingMessage.id)
  
  try {
    // 模拟API调用延迟
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // 移除思考中消息
    setMessages(prev => prev.filter(msg => msg.id !== thinkingMessage.id))
    
    if (aiMode) {
      // 增强模式：模拟AI回答
      const aiResponse = `我已经分析了你的问题："${userMessage.content}"。\n\n根据我的分析，这是一个关于文档检索的请求。我可以帮你找到相关的文档并提供摘要。\n\n如果你有更具体的问题，比如"帮我总结上个月的财务数据"或"查找所有关于 2025 计划的文档"，我可以提供更详细的回答。`
      
      // 流式输出效果
      setTypingText('')
      let index = 0
      const interval = setInterval(() => {
        if (index < aiResponse.length) {
          setTypingText(prev => prev + aiResponse[index])
          index++
        } else {
          clearInterval(interval)
          setTypingInterval(null)
          setChatLoading(false)
        }
      }, 50)
      setTypingInterval(interval)
      
      // 添加最终回答
      setTimeout(() => {
        const finalMessage = {
          id: Date.now() + 2,
          role: 'assistant',
          content: aiResponse,
          timestamp: new Date().toISOString(),
          sources: [
            {
              id: 1,
              filename: '财务报表2025.xlsx',
              snippet: '2025年第一季度财务数据显示营收增长10%',
              path: '财务报表2025.xlsx'
            }
          ]
        }
        setMessages(prev => [...prev, finalMessage])
        setTypingText('')
      }, aiResponse.length * 50 + 100)
    } else {
      // 基础模式：传统搜索，但结果显示在对话界面中
      setSearchLoading(true)
      try {
        console.log('开始搜索:', inputValue.trim())
        const response = await fetch(`http://localhost:8000/search?q=${encodeURIComponent(inputValue.trim())}`)
        console.log('搜索响应:', response)
        if (!response.ok) {
          throw new Error('后端服务可能未启动，请检查服务状态')
        }
        
        const result = await response.json()
        console.log('搜索结果:', result)
        if (result.success) {
          const searchResults = result.results
          if (searchResults.length > 0) {
            // 添加搜索结果消息
            const searchMessage = {
              id: Date.now() + 2,
              role: 'assistant',
              content: `已为您找到 ${searchResults.length} 个相关文件：`,
              timestamp: new Date().toISOString(),
              sources: searchResults.map((doc, index) => ({
                id: index + 1,
                filename: doc.filename,
                snippet: doc.snippet || '',
                path: doc.filename,
                file_path: doc.file_path || `http://localhost:8000/uploads/${doc.filename}`,
                keyword: inputValue.trim()
              }))
            }
            setMessages(prev => [...prev, searchMessage])
          } else {
            // 无结果消息
            const noResultMessage = {
              id: Date.now() + 2,
              role: 'assistant',
              content: '未找到相关文件，请尝试其他关键词。',
              timestamp: new Date().toISOString()
            }
            setMessages(prev => [...prev, noResultMessage])
          }
        } else {
          // 错误消息
          const errorMessage = {
            id: Date.now() + 2,
            role: 'assistant',
            content: `搜索失败：${result.message}`,
            timestamp: new Date().toISOString()
          }
          setMessages(prev => [...prev, errorMessage])
        }
      } catch (error) {
        console.error('搜索失败:', error)
        // 错误消息 - 友好的错误提示
        const errorMessage = {
          id: Date.now() + 2,
          role: 'assistant',
          content: `后端服务暂时不可用，请检查服务是否启动。\n\n错误信息：${error.message}`,
          timestamp: new Date().toISOString()
        }
        setMessages(prev => [...prev, errorMessage])
      } finally {
        console.log('搜索完成')
        setSearchLoading(false)
        setChatLoading(false)
      }
    }
  } catch (error) {
    console.error('发送消息失败:', error)
    setChatLoading(false)
    // 添加错误消息
    const errorMessage = {
      id: Date.now() + 2,
      role: 'assistant',
      content: '抱歉，处理你的请求时出现错误，请稍后再试。',
      timestamp: new Date().toISOString()
    }
    setMessages(prev => [...prev, errorMessage])
  }
}

// 处理快捷指令点击
export const handleQuickCommand = (command, setInputValue) => {
  let question = ''
  switch (command) {
    case '财务报表':
      question = '请分析最近的财务报表'
      break
    case '会议纪要':
      question = '查找所有会议纪要文档'
      break
    case '2025计划':
      question = '查找所有关于2025计划的文档'
      break
    default:
      question = command
  }
  setInputValue(question)
}
