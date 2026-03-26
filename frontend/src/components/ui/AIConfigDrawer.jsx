import React, { useState, useEffect } from 'react'
import { Drawer, Form, Input, Button, Switch, message, Upload } from 'antd'
import { SettingOutlined, UploadOutlined } from '@ant-design/icons'

const AIConfigDrawer = ({ visible, onClose }) => {
  const [form] = Form.useForm()
  
  // 从本地存储加载配置
  useEffect(() => {
    if (visible) {
      const savedConfig = localStorage.getItem('aiConfig')
      if (savedConfig) {
        try {
          const config = JSON.parse(savedConfig)
          form.setFieldsValue({
            apiBaseUrl: config.apiBaseUrl || '',
            apiKey: config.apiKey || '',
            embeddingModel: config.embeddingModel || '',
            timeout: config.timeout || 5,
            enableAI: config.enableAI || false
          })
        } catch (error) {
          console.error('加载配置失败:', error)
        }
      } else {
        // 设置默认值
        form.setFieldsValue({
          apiBaseUrl: '',
          apiKey: '',
          embeddingModel: '',
          timeout: 5,
          enableAI: false
        })
      }
    }
  }, [visible, form])
  
  // 保存配置
  const handleSave = (values) => {
    try {
      // 保存到本地存储
      localStorage.setItem('aiConfig', JSON.stringify({
        apiBaseUrl: values.apiBaseUrl,
        apiKey: values.apiKey,
        embeddingModel: values.embeddingModel,
        timeout: values.timeout,
        enableAI: values.enableAI
      }))
      
      // 发送配置到后端
      fetch('/api/ai/config', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          api_base_url: values.apiBaseUrl,
          api_key: values.apiKey,
          embedding_model: values.embeddingModel,
          timeout: values.timeout
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          message.success('配置保存成功')
        } else {
          message.error('配置保存失败')
        }
      })
      .catch(error => {
        console.error('保存配置失败:', error)
        message.warning('配置已保存到本地，后端配置可能需要重启服务')
      })
      
      onClose()
    } catch (error) {
      console.error('保存配置失败:', error)
      message.error('保存配置失败')
    }
  }
  
  // 测试连接
  const handleTestConnection = async () => {
    const values = await form.validateFields()
    
    if (!values.apiBaseUrl) {
      message.error('请输入API地址')
      return
    }
    
    try {
      // 测试连接
      const response = await fetch(`${values.apiBaseUrl}/models`, {
        headers: values.apiKey ? {
          'Authorization': `Bearer ${values.apiKey}`
        } : {}
      })
      
      if (response.ok) {
        message.success('连接测试成功')
      } else {
        message.error('连接测试失败，请检查配置')
      }
    } catch (error) {
      console.error('连接测试失败:', error)
      message.error('连接测试失败，请检查网络或API地址')
    }
  }
  
  return (
    <Drawer
      title={<><SettingOutlined /> AI 服务配置</>}
      placement="right"
      onClose={onClose}
      open={visible}
      width={500}
    >
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSave}
      >
        <Form.Item
          name="enableAI"
          label="启用 AI 服务"
        >
          <Switch />
        </Form.Item>
        
        <Form.Item
          name="apiBaseUrl"
          label="API 地址"
          rules={[
            { required: true, message: '请输入 API 地址' },
            { type: 'url', message: '请输入有效的 URL' }
          ]}
        >
          <Input placeholder="例如: http://localhost:11434 或 https://api.openai.com" />
        </Form.Item>
        
        <Form.Item
          name="apiKey"
          label="API 密钥"
        >
          <Input.Password placeholder="如果需要认证，请输入 API 密钥" />
        </Form.Item>
        
        <Form.Item
          name="embeddingModel"
          label="嵌入RAG模型"
        >
          <Upload.Dragger 
            name="embeddingModel" 
            accept=".bin,.onnx,.model"
            showUploadList={false}
            beforeUpload={(file) => {
              form.setFieldsValue({ embeddingModel: file.name });
              return false; // 阻止自动上传
            }}
          >
            <p className="ant-upload-drag-icon">
              <UploadOutlined />
            </p>
            <p className="ant-upload-text">点击或拖拽文件到此区域上传</p>
            <p className="ant-upload-hint">
              支持 .bin, .onnx, .model 格式的模型文件
            </p>
          </Upload.Dragger>
        </Form.Item>
        
        <Form.Item
          name="timeout"
          label="超时时间 (秒)"
          rules={[
            { required: true, message: '请输入超时时间' },
            { type: 'number', min: 1, max: 30, message: '超时时间应在 1-30 秒之间' }
          ]}
        >
          <Input type="number" min={1} max={30} />
        </Form.Item>
        
        <Form.Item>
          <Button type="primary" htmlType="submit" style={{ marginRight: 8 }}>
            保存配置
          </Button>
          <Button onClick={handleTestConnection} style={{ marginRight: 8 }}>
            测试连接
          </Button>
          <Button onClick={onClose}>
            取消
          </Button>
        </Form.Item>
      </Form>
    </Drawer>
  )
}

export default AIConfigDrawer