import React, { useState, useEffect, useMemo } from 'react'
import { Layout, Input, Button, Space, Form, Checkbox, DatePicker, InputNumber, Drawer, Badge, Table, Empty } from 'antd'
import { SearchOutlined, FileOutlined, EyeOutlined, DeleteOutlined, FileExcelOutlined, FileWordOutlined, FileTextOutlined } from '@ant-design/icons'
import { motion, AnimatePresence } from 'framer-motion'

// 导入布局组件
import Header from './components/layout/Header'

// 导入页面组件
import ChatContainer from './components/ChatContainer'
import SearchResults from './components/pages/SearchResults'

import FileManagement from './components/pages/FileManagement'
import DataAnalytics from './components/pages/DataAnalytics'

// 导入UI组件
import FilePreviewDrawer from './components/ui/FilePreviewDrawer'
import FilterDrawer from './components/ui/FilterDrawer'
import FilterPreviewDrawer from './components/ui/FilterPreviewDrawer'
import AIConfigDrawer from './components/ui/AIConfigDrawer'

// 导入工具函数
import { getFileTypeInfo, getFileTypeIcon as getFileTypeIconInfo, highlightKeywords as getHighlightedParts } from './utils/fileUtils'
import { handleUpload, handleSearch, fetchDocuments, fetchStatistics, handleDeleteDocument, handleFilePreview as apiHandleFilePreview } from './utils/api'
import { handleSendMessage, handleQuickCommand } from './utils/chatService'

// 导入样式
import './styles/Content.css'

// 渲染文件类型图标
const renderFileTypeIcon = (fileType) => {
  const iconInfo = getFileTypeIconInfo(fileType)
  const iconMap = {
    'FileExcelOutlined': <FileExcelOutlined style={{ color: iconInfo.color }} />,
    'FileWordOutlined': <FileWordOutlined style={{ color: iconInfo.color }} />,
    'FileTextOutlined': <FileTextOutlined style={{ color: iconInfo.color }} />,
    'FileOutlined': <FileOutlined style={{ color: iconInfo.color }} />
  }
  return iconMap[iconInfo.type] || <FileOutlined style={{ color: iconInfo.color }} />
}

// 渲染高亮关键词
const highlightKeywords = (text, keyword) => {
  const parts = getHighlightedParts(text, keyword)
  if (typeof parts === 'string') return parts
  
  return parts.map((part, index) => {
    if (typeof part === 'string') {
      return <span key={index}>{part}</span>
    } else if (part.type === 'highlight') {
      return <span key={index} className="highlight">{part.content}</span>
    }
    return null
  })
}

const { RangePicker } = DatePicker
const { Content } = Layout
const { Search } = Input

function App() {
  // 状态管理
  const [activeMenu, setActiveMenu] = useState('home')
  const [searchKeyword, setSearchKeyword] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [documents, setDocuments] = useState([])
  const [searchLoading, setSearchLoading] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [fileTypeFilter, setFileTypeFilter] = useState({ excel: true, word: true, txt: true })
  const [sortBy, setSortBy] = useState('relevance')
  const [statistics, setStatistics] = useState(null)
  
  // 筛选功能状态
  const [filterVisible, setFilterVisible] = useState(false)
  const [filterConditions, setFilterConditions] = useState({
    fileTypes: { excel: true, word: true, txt: true },
    dateRange: null,
    contentLength: {
      min: null,
      max: null
    }
  })
  const [filteredDocuments, setFilteredDocuments] = useState([])
  const [previewFilterVisible, setPreviewFilterVisible] = useState(false)
  const [previewFilterResults, setPreviewFilterResults] = useState([])
  
  // 对话式界面状态
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: '你好！我是你的智能文档助手。你可以问我关于财务报表、会议纪要或 2025 计划的问题。',
      timestamp: new Date().toISOString()
    }
  ])
  const [inputValue, setInputValue] = useState('')
  const [chatLoading, setChatLoading] = useState(false)
  const [aiMode, setAiMode] = useState(false) // 模拟AI插件是否安装
  const [currentMessageId, setCurrentMessageId] = useState(null)
  const [typingText, setTypingText] = useState('')
  const [typingInterval, setTypingInterval] = useState(null)
  
  // 文件预览状态
  const [filePreviewVisible, setFilePreviewVisible] = useState(false)
  const [filePreviewData, setFilePreviewData] = useState(null)
  const [filePreviewLoading, setFilePreviewLoading] = useState(false)
  
  // AI配置抽屉状态
  const [aiConfigVisible, setAiConfigVisible] = useState(false)
  
  // 处理文件上传
  const handleFileUpload = async (options) => {
    const { file, onSuccess, onError, onProgress } = options
    // 上传前重置预览状态
    setFilePreviewData(null)
    setFilePreviewVisible(false)
    return handleUpload(file, onSuccess, onError, onProgress, setUploading, setUploadProgress, () => fetchDocumentsData(), () => fetchStatisticsData())
  }

  // 处理搜索
  const handleSearchQuery = async (keyword) => {
    return handleSearch(keyword, setSearchLoading, setSearchKeyword, setSearchResults, setActiveMenu)
  }

  // 获取文档列表
  const fetchDocumentsData = async () => {
    return fetchDocuments(setDocuments)
  }

  // 获取统计数据
  const fetchStatisticsData = async () => {
    return fetchStatistics(documents, setStatistics)
  }

  // 处理文件预览
  const handleFilePreview = async (source) => {
    // 预览前重置预览状态
    setFilePreviewData(null)
    return apiHandleFilePreview(source, documents, setFilePreviewLoading, setFilePreviewData, setFilePreviewVisible, getFileTypeInfo, searchKeyword)
  }

  // 组件加载时获取文档列表和统计数据
  useEffect(() => {
    fetchDocumentsData()
  }, [])

  useEffect(() => {
    fetchStatisticsData()
  }, [documents])
  
  // 筛选逻辑
  const filteredDocs = useMemo(() => {
    return documents.filter(doc => {
      // 筛选文件类型
      if (!filterConditions.fileTypes[doc.file_type]) {
        return false
      }
      
      // 筛选时间范围
      if (filterConditions.dateRange) {
        const [start, end] = filterConditions.dateRange
        const docDate = new Date(doc.created_at)
        if (docDate < start || docDate > end) {
          return false
        }
      }
      
      // 筛选内容长度
      if (filterConditions.contentLength.min !== null && doc.content_length < filterConditions.contentLength.min) {
        return false
      }
      if (filterConditions.contentLength.max !== null && doc.content_length > filterConditions.contentLength.max) {
        return false
      }
      
      return true
    })
  }, [documents, filterConditions])
  
  // 处理筛选条件变化
  const handleFilterChange = (field, value) => {
    setFilterConditions(prev => ({
      ...prev,
      [field]: value
    }))
  }
  
  // 处理文件类型筛选变化
  const handleFileTypeChange = (type, checked) => {
    setFilterConditions(prev => ({
      ...prev,
      fileTypes: {
        ...prev.fileTypes,
        [type]: checked
      }
    }))
  }
  
  // 处理内容长度筛选变化
  const handleContentLengthChange = (field, value) => {
    setFilterConditions(prev => ({
      ...prev,
      contentLength: {
        ...prev.contentLength,
        [field]: value
      }
    }))
  }
  
  // 重置筛选条件
  const resetFilters = () => {
    setFilterConditions({
      fileTypes: { excel: true, word: true, txt: true },
      dateRange: null,
      contentLength: {
        min: null,
        max: null
      }
    })
  }
  
  // 应用筛选
  const applyFilters = () => {
    setFilteredDocuments(filteredDocs)
    setFilterVisible(false)
  }
  
  // 预览筛选结果
  const previewFilters = () => {
    setPreviewFilterResults(filteredDocs)
    setPreviewFilterVisible(true)
  }
  
  // 处理发送消息
  const handleSend = async () => {
    return handleSendMessage(inputValue, setMessages, setInputValue, setChatLoading, setCurrentMessageId, setTypingText, setTypingInterval, aiMode, setAiMode, setSearchLoading)
  }
  
  // 处理快捷指令点击
  const handleQuickCommandClick = (command) => {
    return handleQuickCommand(command, setInputValue)
  }
  
  // 清理定时器
  useEffect(() => {
    return () => {
      if (typingInterval) {
        clearInterval(typingInterval)
      }
    }
  }, [typingInterval])
  
  return (
    <Layout className="layout">
      <Header 
        activeMenu={activeMenu}
        setActiveMenu={setActiveMenu}
        fetchDocuments={fetchDocumentsData}
        onAIClick={() => setAiConfigVisible(true)}
      />
      
      <Content style={{ padding: '0 16px', marginTop: 8, overflow: 'hidden', paddingTop: '72px', height: 'calc(100vh - 64px)' }}>
        <AnimatePresence mode="wait">
          {/* 首页 - 聊天对话界面 */}
          {activeMenu === 'home' && (
            <motion.div
              key="home"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
              style={{ height: '100%', display: 'flex', flexDirection: 'column' }}
            >
              <ChatContainer 
                messages={messages}
                inputValue={inputValue}
                setInputValue={setInputValue}
                chatLoading={chatLoading}
                typingText={typingText}
                aiMode={aiMode}
                setAiMode={setAiMode}
                handleSendMessage={handleSend}
                handleFilePreview={handleFilePreview}
                highlightKeywords={highlightKeywords}
                handleQuickCommand={handleQuickCommandClick}
              />
            </motion.div>
          )}
          
          {/* 搜索结果页 */}
          {activeMenu === 'search' && (
            <SearchResults 
              searchKeyword={searchKeyword}
              searchResults={searchResults}
              searchLoading={searchLoading}
              fileTypeFilter={fileTypeFilter}
              setFileTypeFilter={setFileTypeFilter}
              sortBy={sortBy}
              setSortBy={setSortBy}
              handleFilePreview={handleFilePreview}
              handleDeleteDocument={(docId, filename) => handleDeleteDocument(docId, filename, fetchDocumentsData, fetchStatisticsData, searchResults, setSearchResults)}
            />
          )}
          

          
          {/* 文件管理页 */}
          {activeMenu === 'documents' && (
            <FileManagement 
              documents={documents}
              filteredDocuments={filteredDocuments}
              searchLoading={searchLoading}
              filterVisible={filterVisible}
              setFilterVisible={setFilterVisible}
              setFilteredDocuments={setFilteredDocuments}
              handleFilePreview={handleFilePreview}
              handleDeleteDocument={(docId, filename) => handleDeleteDocument(docId, filename, fetchDocumentsData, fetchStatisticsData, searchResults, setSearchResults)}
              uploading={uploading}
              uploadProgress={uploadProgress}
              handleUpload={handleFileUpload}
            />
          )}
          
          {/* 数据分析页 */}
          {activeMenu === 'analytics' && (
            <DataAnalytics statistics={statistics} />
          )}
        </AnimatePresence>
      </Content>
      
      {/* 文件预览抽屉 */}
      <FilePreviewDrawer 
        visible={filePreviewVisible}
        onClose={() => setFilePreviewVisible(false)}
        fileData={filePreviewData}
        fileTypeInfo={filePreviewData ? getFileTypeInfo(filePreviewData.fileName) : null}
        getFileTypeIcon={renderFileTypeIcon}
        loading={filePreviewLoading}
      />
      
      {/* 筛选条件抽屉 */}
      <FilterDrawer 
        visible={filterVisible}
        onClose={() => setFilterVisible(false)}
        filterConditions={filterConditions}
        handleFilterChange={handleFilterChange}
        handleFileTypeChange={handleFileTypeChange}
        handleContentLengthChange={handleContentLengthChange}
        resetFilters={resetFilters}
        previewFilters={previewFilters}
        applyFilters={applyFilters}
      />
      
      {/* 筛选预览抽屉 */}
      <FilterPreviewDrawer 
        visible={previewFilterVisible}
        onClose={() => setPreviewFilterVisible(false)}
        results={previewFilterResults}
        getFileTypeIcon={renderFileTypeIcon}
      />
      
      {/* AI配置抽屉 */}
      <AIConfigDrawer 
        visible={aiConfigVisible}
        onClose={() => setAiConfigVisible(false)}
      />
    </Layout>
  )
}

export default App
