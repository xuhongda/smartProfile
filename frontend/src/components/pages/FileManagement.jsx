import React from 'react'
import { Card, Table, Button, Space, Tooltip, Badge, Upload, Progress } from 'antd'
import { EyeOutlined, DeleteOutlined, FilterOutlined, ReloadOutlined, FileOutlined, FileExcelOutlined, FileWordOutlined, FileTextOutlined, UploadOutlined } from '@ant-design/icons'
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
  handleDeleteDocument,
  uploading,
  uploadProgress,
  handleUpload
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
              onClick={() => handleDeleteDocument(record.uuid || record.id, record.filename)}
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
        <div className="upload-container mb-6">
          <p className="upload-description">
            支持上传 Excel (.xlsx, .xls)、Word (.docx) 和文本 (.txt) 文件
          </p>
          
          <div className="upload-area">
            <Upload
              name="file"
              accept=".xlsx,.xls,.docx,.txt"
              showUploadList={false}
              customRequest={handleUpload}
              maxCount={1}
            >
              <div className="upload-button-container">
                {uploading ? (
                  <div className="uploading-status">
                    <Progress percent={uploadProgress} />
                    <p>正在解析并建立索引...</p>
                  </div>
                ) : (
                  <Button 
                    icon={<UploadOutlined />} 
                    type="primary" 
                    size="large"
                  >
                    选择文件或拖拽到此处
                  </Button>
                )}
              </div>
            </Upload>
          </div>
          
          <div className="upload-tips">
            <p>• 文件大小限制：20MB</p>
            <p>• 支持的文件格式：.xlsx, .xls, .docx, .txt</p>
            <p>• 系统会自动提取文件内容并建立搜索索引</p>
          </div>
        </div>
        
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
