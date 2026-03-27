import React from 'react'
import { Card, Row, Col, Checkbox, Select, Space, Button, Tooltip, Empty } from 'antd'
import { EyeOutlined, DeleteOutlined, FileOutlined, FileExcelOutlined, FileWordOutlined, FileTextOutlined } from '@ant-design/icons'
import { motion, AnimatePresence } from 'framer-motion'
import { getFileTypeIcon as getFileTypeIconInfo, highlightKeywords as getHighlightedParts } from '../../utils/fileUtils'

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

const { Option } = Select

const SearchResults = ({ 
  searchKeyword, 
  searchResults, 
  searchLoading, 
  fileTypeFilter, 
  setFileTypeFilter, 
  sortBy, 
  setSortBy, 
  handleFilePreview, 
  handleDeleteDocument,
  aiResponse
}) => {
  return (
    <motion.div
      key="search"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
    >
      <Card title={`搜索结果: "${searchKeyword}"`} variant="outlined" className="search-results-card">
        <Row gutter={[24, 24]}>
          {/* 左侧过滤器 */}
          <Col span={6}>
            <Card title="筛选" size="small" variant="outlined" className="filter-card">
              <Space direction="vertical" size="middle" style={{ width: '100%' }}>
                <div className="filter-section">
                  <h4>文件类型</h4>
                  <Checkbox
                    checked={fileTypeFilter.excel}
                    onChange={(e) => setFileTypeFilter({...fileTypeFilter, excel: e.target.checked})}
                  >
                    Excel (.xlsx, .xls)
                  </Checkbox>
                  <Checkbox
                    checked={fileTypeFilter.word}
                    onChange={(e) => setFileTypeFilter({...fileTypeFilter, word: e.target.checked})}
                  >
                    Word (.docx)
                  </Checkbox>
                  <Checkbox
                    checked={fileTypeFilter.txt}
                    onChange={(e) => setFileTypeFilter({...fileTypeFilter, txt: e.target.checked})}
                  >
                    文本 (.txt)
                  </Checkbox>
                </div>
                
                <div className="filter-section">
                  <h4>排序方式</h4>
                  <Select
                    defaultValue="relevance"
                    style={{ width: '100%' }}
                    onChange={setSortBy}
                  >
                    <Option value="relevance">相关度最高</Option>
                    <Option value="newest">最新上传</Option>
                    <Option value="oldest">最早上传</Option>
                  </Select>
                </div>
              </Space>
            </Card>
          </Col>
          
          {/* 中间结果列表 */}
          <Col span={18}>
            <AnimatePresence>
              {searchLoading ? (
                <div className="loading-container">
                  <p>搜索中...</p>
                </div>
              ) : searchResults.length > 0 ? searchResults.map(result => (
                  <motion.div
                    key={result.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    transition={{ duration: 0.3 }}
                  >
                    <Card
                      variant="outlined"
                      className="result-card"
                      hoverable
                      onClick={() => handleFilePreview(result)}
                    >
                      <Space direction="vertical" size="small" style={{ width: '100%' }}>
                        <Space justify="space-between" style={{ width: '100%' }}>
                          <Space>
                                    {renderFileTypeIcon(result.file_type)}
                                    <span className="result-filename">{result.filename}</span>
                                  </Space>
                          <Space size="small">
                            <Tooltip title="预览">
                              <Button 
                                icon={<EyeOutlined />} 
                                size="small"
                                onClick={(e) => {
                                  e.stopPropagation()
                                  handleFilePreview(result)
                                }}
                              />
                            </Tooltip>
                            <Tooltip title="删除">
                              <Button 
                                icon={<DeleteOutlined />} 
                                size="small" 
                                danger
                                onClick={(e) => {
                                  e.stopPropagation()
                                  handleDeleteDocument(result.uuid || result.id, result.filename)
                                }}
                              />
                            </Tooltip>
                          </Space>
                        </Space>
                        <div className="result-snippet">
                          {highlightKeywords(result.snippet || '', searchKeyword)}
                        </div>
                        <div className="result-meta">
                          <span>{new Date(result.created_at).toLocaleString()}</span>
                        </div>
                      </Space>
                    </Card>
                  </motion.div>
                )) : (
                <Empty
                  description="未找到相关文件"
                  style={{ margin: '60px 0' }}
                />
              )}
              
              {/* AI 回答显示 */}
              {aiResponse && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                  style={{ marginTop: 24 }}
                >
                  <Card title="AI 回答" variant="outlined" className="ai-response-card">
                    <div className="ai-response-content">
                      {aiResponse}
                    </div>
                  </Card>
                </motion.div>
              )}
            </AnimatePresence>
          </Col>
        </Row>
      </Card>
    </motion.div>
  )
}

export default SearchResults
