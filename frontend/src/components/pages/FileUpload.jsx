import React from 'react'
import { Card, Button, Upload, Progress, Space } from 'antd'
import { UploadOutlined } from '@ant-design/icons'
import { motion } from 'framer-motion'
import '../../styles/Content.css'

const FileUpload = ({ uploading, uploadProgress, handleUpload }) => {
  return (
    <motion.div
      key="upload"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
    >
      <Card title="文件上传" variant="outlined" className="upload-card">
        <div className="upload-container">
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
      </Card>
    </motion.div>
  )
}

export default FileUpload
