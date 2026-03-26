import React from 'react'
import { Drawer, Form, Checkbox, Divider, DatePicker, InputNumber, Button, Space } from 'antd'
import '../../styles/Drawers.css'

const { RangePicker } = DatePicker

const FilterDrawer = ({ 
  visible, 
  onClose, 
  filterConditions, 
  handleFileTypeChange, 
  handleFilterChange, 
  handleContentLengthChange, 
  resetFilters, 
  previewFilters, 
  applyFilters 
}) => {
  return (
    <Drawer
      title="筛选条件"
      open={visible}
      onClose={onClose}
      size={400}
      placement="right"
      footer={
        <Space style={{ width: '100%', justifyContent: 'flex-end' }}>
          <Button onClick={resetFilters}>重置</Button>
          <Button onClick={previewFilters}>预览</Button>
          <Button type="primary" onClick={applyFilters}>应用</Button>
        </Space>
      }
    >
      <Form layout="vertical">
        <Form.Item label="文件类型">
          <Space direction="vertical" style={{ width: '100%' }}>
            <Checkbox
              checked={filterConditions.fileTypes.excel}
              onChange={(e) => handleFileTypeChange('excel', e.target.checked)}
            >
              Excel (.xlsx, .xls)
            </Checkbox>
            <Checkbox
              checked={filterConditions.fileTypes.word}
              onChange={(e) => handleFileTypeChange('word', e.target.checked)}
            >
              Word (.docx)
            </Checkbox>
            <Checkbox
              checked={filterConditions.fileTypes.txt}
              onChange={(e) => handleFileTypeChange('txt', e.target.checked)}
            >
              文本 (.txt)
            </Checkbox>
          </Space>
        </Form.Item>
        
        <Divider />
        
        <Form.Item label="上传时间范围">
          <RangePicker
            style={{ width: '100%' }}
            onChange={(dates) => handleFilterChange('dateRange', dates)}
          />
        </Form.Item>
        
        <Divider />
        
        <Form.Item label="内容长度范围（字符）">
          <Space direction="vertical" style={{ width: '100%' }}>
            <Space style={{ width: '100%', justifyContent: 'space-between' }}>
              <span>最小值:</span>
              <InputNumber
                style={{ width: 120 }}
                min={0}
                value={filterConditions.contentLength.min}
                onChange={(value) => handleContentLengthChange('min', value)}
              />
            </Space>
            <Space style={{ width: '100%', justifyContent: 'space-between' }}>
              <span>最大值:</span>
              <InputNumber
                style={{ width: 120 }}
                min={0}
                value={filterConditions.contentLength.max}
                onChange={(value) => handleContentLengthChange('max', value)}
              />
            </Space>
          </Space>
        </Form.Item>
      </Form>
    </Drawer>
  )
}

export default FilterDrawer
