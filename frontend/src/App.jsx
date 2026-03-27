import React, { useEffect } from 'react'
import { Layout } from 'antd'
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

// 导入状态存储
import useAppStore from './stores/useAppStore'
import useChatStore from './stores/useChatStore'
import useDocumentStore from './stores/useDocumentStore'

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

const { Content } = Layout

function App() {
  // 应用状态
  const { activeMenu, setActiveMenu, aiConfigVisible, setAiConfigVisible } = useAppStore()
  
  // 聊天状态
  const { 
    messages, 
    inputValue, 
    setInputValue, 
    chatLoading, 
    typingText, 
    aiMode, 
    setAiMode,
    setMessages,
    setChatLoading,
    setCurrentMessageId,
    setTypingText,
    setTypingInterval,
    clearTypingInterval
  } = useChatStore()
  
  // 文档状态
  const { 
    documents, 
    searchResults, 
    searchLoading, 
    setSearchLoading, 
    fileTypeFilter, 
    setFileTypeFilter, 
    sortBy, 
    setSortBy, 
    statistics, 
    uploading, 
    uploadProgress, 
    filterVisible, 
    setFilterVisible, 
    filterConditions, 
    filteredDocuments, 
    setFilteredDocuments, 
    previewFilterVisible, 
    setPreviewFilterVisible, 
    previewFilterResults, 
    filePreviewVisible, 
    setFilePreviewVisible, 
    filePreviewData, 
    filePreviewLoading,
    aiResponse,
    fetchDocumentsData,
    fetchStatisticsData,
    handleFileUpload,
    handleSearchQuery,
    handleFilePreviewLocal,
    handleDeleteDocumentLocal,
    handleFilterChange,
    handleFileTypeChange,
    handleContentLengthChange,
    resetFilters,
    applyFilters,
    previewFilters
  } = useDocumentStore()
  
  // 处理发送消息
  const handleSend = async () => {
    import('./utils/chatService').then(({ handleSendMessage }) => {
      handleSendMessage(
        inputValue, 
        setMessages, 
        setInputValue, 
        setChatLoading, 
        setCurrentMessageId, 
        setTypingText, 
        setTypingInterval, 
        aiMode, 
        setAiMode, 
        setSearchLoading
      )
    })
  }
  
  // 处理快捷指令点击
  const handleQuickCommandClick = (command) => {
    import('./utils/chatService').then(({ handleQuickCommand }) => {
      handleQuickCommand(command, setInputValue)
    })
  }
  
  // 组件加载时获取文档列表
  useEffect(() => {
    fetchDocumentsData()
  }, [])
  
  // 清理定时器
  useEffect(() => {
    return () => {
      clearTypingInterval()
    }
  }, [])
  
  return (
    <Layout className="layout">
      <Header 
        activeMenu={activeMenu}
        setActiveMenu={setActiveMenu}
        fetchDocuments={fetchDocumentsData}
        onAIClick={() => setAiConfigVisible(true)}
      />
      
      <Content style={{ padding: '0 16px', marginTop: 8, overflowY: 'auto', paddingTop: '72px', height: 'calc(100vh - 64px)' }}>
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
                handleFilePreview={handleFilePreviewLocal}
                highlightKeywords={highlightKeywords}
                handleQuickCommand={handleQuickCommandClick}
              />
            </motion.div>
          )}
          
          {/* 搜索结果页 */}
          {activeMenu === 'search' && (
            <SearchResults 
              searchKeyword={useDocumentStore.getState().searchKeyword}
              searchResults={searchResults}
              searchLoading={searchLoading}
              fileTypeFilter={fileTypeFilter}
              setFileTypeFilter={setFileTypeFilter}
              sortBy={sortBy}
              setSortBy={setSortBy}
              handleFilePreview={handleFilePreviewLocal}
              handleDeleteDocument={handleDeleteDocumentLocal}
              aiResponse={aiResponse}
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
              handleFilePreview={handleFilePreviewLocal}
              handleDeleteDocument={handleDeleteDocumentLocal}
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
