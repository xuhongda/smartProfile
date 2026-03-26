import React from 'react'
import { Drawer, Badge, Space, Table, Empty } from 'antd'
import { EyeOutlined, DeleteOutlined } from '@ant-design/icons'
import '../../styles/Drawers.css'

const FilterPreviewDrawer = ({ 
  visible, 
  onClose, 
  results, 
  getFileTypeIcon 
}) => {
  const columns = [
    {
      title: '文件',
      dataIndex: 'filename',
      key: 'filename',
      render: (text, record) => (
        <Space>
          {getFileTypeIcon && getFileTypeIcon(record.file_type)}
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
    }
  ]

  return (
    <Drawer
      title="筛选预览"
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
      <div style={{ marginBottom: 16 }}>
        <Space>
          <Badge count={results.length} showZero />
          <span>个文件符合筛选条件</span>
        </Space>
      </div>
      
      {results.length > 0 ? (
        <Table
          columns={columns}
          dataSource={results}
          rowKey="id"
          pagination={{ pageSize: 5 }}
        />
      ) : (
        <Empty description="没有符合条件的文件" />
      )}
    </Drawer>
  )
}

export default FilterPreviewDrawer
