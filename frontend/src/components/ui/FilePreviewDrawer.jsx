import React from 'react'
import { Drawer, Spin, Alert } from 'antd'
import NewFilePreviewContainer from '../preview/NewFilePreviewContainer'
import '../../styles/Drawers.css'

const FilePreviewDrawer = ({ visible, onClose, fileData, fileTypeInfo, getFileTypeIcon, loading }) => {
  // 渲染加载状态
  const renderLoading = () => (
    <div style={{ padding: '40px', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
      <Spin size="large" tip="文件预览加载中..." />
    </div>
  )

  // 渲染错误状态
  const renderError = () => (
    <div style={{ padding: '40px' }}>
      <Alert
        message="文件预览失败"
        description="无法加载文件信息，请稍后重试"
        type="error"
        showIcon
        action={
          <button 
            onClick={onClose}
            style={{
              background: 'none',
              border: '1px solid #ff4d4f',
              color: '#ff4d4f',
              padding: '4px 12px',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            关闭
          </button>
        }
      />
    </div>
  )

  // 渲染预览内容
  const renderContent = () => {
    if (!fileData) {
      return renderError()
    }

    // 构建file对象
    const file = {
      name: fileData.fileName || '未知文件',
      type: fileTypeInfo ? fileTypeInfo.type : '',
      size: 0 // 暂时设置为0，实际应用中可以从后端获取
    }
    
    // 构建文件URL
    const fileUrl = fileData.uri || `http://localhost:8000/uploads/${encodeURIComponent(fileData.fileName || 'unknown')}`

    return (
      <NewFilePreviewContainer 
        file={file} 
        url={fileUrl} 
        content={fileData.content} 
        keyword={fileData.keyword || ''}
      />
    )
  }

  return (
    <Drawer
      title={fileData ? fileData.fileName : '文件预览'}
      open={visible}
      onClose={onClose}
      size="large"
      placement="right"
      styles={{
        body: {
          display: 'flex',
          flexDirection: 'column',
          height: '100%'
        }
      }}
    >
      {loading ? renderLoading() : renderContent()}
    </Drawer>
  )
}

export default FilePreviewDrawer
