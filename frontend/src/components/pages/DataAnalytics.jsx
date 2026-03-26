import React from 'react'
import { Card, Row, Col, Statistic } from 'antd'
import { FileOutlined, FileExcelOutlined, FileWordOutlined, FileTextOutlined } from '@ant-design/icons'
import { motion } from 'framer-motion'

const DataAnalytics = ({ statistics }) => {
  return (
    <motion.div
      key="analytics"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
    >
      <Card title="数据分析" variant="outlined" className="analytics-card">
        <Row gutter={[16, 16]}>
          <Col span={6}>
            <Statistic 
              title="总文件数" 
              value={statistics?.total_documents || 0} 
              prefix={<FileOutlined />} 
            />
          </Col>
          <Col span={6}>
            <Statistic 
              title="Excel文件" 
              value={statistics?.file_type_distribution?.excel || 0} 
              prefix={<FileExcelOutlined style={{ color: '#52c41a' }} />} 
            />
          </Col>
          <Col span={6}>
            <Statistic 
              title="Word文件" 
              value={statistics?.file_type_distribution?.word || 0} 
              prefix={<FileWordOutlined style={{ color: '#1890ff' }} />} 
            />
          </Col>
          <Col span={6}>
            <Statistic 
              title="文本文件" 
              value={statistics?.file_type_distribution?.txt || 0} 
              prefix={<FileTextOutlined style={{ color: '#faad14' }} />} 
            />
          </Col>
        </Row>
        
        <Row style={{ marginTop: 24 }} gutter={[16, 16]}>
          <Col span={24}>
            <Card title="文件类型分布" size="small" variant="outlined">
              <div className="chart-container">
                {statistics && (
                  <div className="file-type-distribution">
                    {Object.entries(statistics.file_type_distribution || {}).map(([type, count]) => (
                      <div key={type} className="distribution-item">
                        <div className="distribution-label">
                          {type === 'excel' ? 'Excel' : type === 'word' ? 'Word' : '文本'}
                        </div>
                        <div className="distribution-bar">
                          <div 
                            className="distribution-fill"
                            style={{
                              width: `${(count / statistics.total_documents) * 100}%`,
                              backgroundColor: type === 'excel' ? '#52c41a' : type === 'word' ? '#1890ff' : '#faad14'
                            }}
                          />
                        </div>
                        <div className="distribution-count">{count}</div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </Card>
          </Col>
        </Row>
      </Card>
    </motion.div>
  )
}

export default DataAnalytics
