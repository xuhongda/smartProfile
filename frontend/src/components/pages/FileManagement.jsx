import React from 'react'
import { Card, Table, Button, Space, Tooltip, Badge } from 'antd'
import { EyeOutlined, DeleteOutlined, FilterOutlined, ReloadOutlined, FileOutlined, FileExcelOutlined, FileWordOutlined, FileTextOutlined } from '@ant-design/icons'
import { motion } from 'framer-motion'
import { getFileTypeIcon as getFileTypeIconInfo } from '../../utils/fileUtils'
import '../../styles/Content.css'

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

const FileManagement = ({ 
  documents, 
  filteredDocuments, 
  searchLoading, 
  filterVisible, 
  setFilterVisible, 
  setFilteredDocuments,
  handleFilePreview, 
  handleDeleteDocument 
}) => {
  const columns = [
    {
      title: '文件',
      dataIndex: 'filename',
      key: 'filename',
      render: (text, record) => (
        <Space>
          {renderFileTypeIcon(record.file_type)}
          <span>{text}</span>
        </Space>
      )
    },
    {
      title: '类型',
      dataIndex: 'file_type',
      key: 'file_type',
      render: (text) => (
        <span>
          {text === 'excel' ? 'Excel' : text === 'word' ? 'Word' : '文本'}
        </span>
      )
    },
    {
      title: '内容长度',
      dataIndex: 'content_length',
      key: 'content_length',
      render: (text) => `${text} 字符`
    },
    {
      title: '上传时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (text) => new Date(text).toLocaleString()
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <Space size="small">
          <Tooltip title="预览">
            <Button 
              icon={<EyeOutlined />} 
              size="small"
              onClick={() => {
                handleFilePreview(record)
              }}
            />
          </Tooltip>
          <Tooltip title="删除">
            <Button 
              icon={<DeleteOutlined />} 
              size="small" 
              danger
              onClick={() => handleDeleteDocument(record.id, record.filename)}
            />
          </Tooltip>
        </Space>
      )
    }
  ]

  return (
    <motion.div
      key="documents"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
    >
      <Card 
        title="文件管理" 
        variant="outlined" 
        className="documents-card"
        extra={
          <Space>
            <Button 
              icon={<FilterOutlined />} 
              onClick={() => setFilterVisible(true)}
            >
              筛选
            </Button>
            {filteredDocuments.length > 0 && (
              <Badge count={filteredDocuments.length} showZero>
                <Button 
                  icon={<ReloadOutlined />} 
                  onClick={() => setFilteredDocuments([])}
                >
                  清除筛选
                </Button>
              </Badge>
            )}
          </Space>
        }
      >
        <Table
          columns={columns}
          dataSource={filteredDocuments.length > 0 ? filteredDocuments : documents}
          rowKey="id"
          pagination={{ pageSize: 10 }}
          loading={searchLoading}
        />
      </Card>
    </motion.div>
  )
}



export default FileManagement
