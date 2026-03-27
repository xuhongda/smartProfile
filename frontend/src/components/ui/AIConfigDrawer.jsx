import React, { useState, useEffect } from 'react'
import { Drawer, Form, Input, Button, Switch, message, List, Alert, Card } from 'antd'
import { SettingOutlined, OrderedListOutlined } from '@ant-design/icons'

const AIConfigDrawer = ({ visible, onClose }) => {
  const [form] = Form.useForm()
  const [models, setModels] = useState([])
  
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
            embeddingModel: config.embeddingModel || 'bge-small-zh-v1.5',
            speechModel: config.speechModel || 'FunASR',
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
          embeddingModel: 'bge-small-zh-v1.5',
          speechModel: 'FunASR',
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
        speechModel: values.speechModel,
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
          speech_model: values.speechModel,
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
      const response = await fetch('/api/ai/test-connection', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          api_base_url: values.apiBaseUrl,
          api_key: values.apiKey
        })
      })
      
      const data = await response.json()
      
      if (data.success) {
        message.success('连接测试成功')
      } else {
        message.error(data.message || '连接测试失败，请检查配置')
      }
    } catch (error) {
      console.error('连接测试失败:', error)
      message.error('连接测试失败，请检查网络或API地址')
    }
  }
  
  // 获取模型列表
  const getModels = async () => {
    try {
      const response = await fetch('/api/model/list')
      const data = await response.json()
      if (data.success) {
        setModels(data.models)
      } else {
        message.error('获取模型列表失败')
      }
    } catch (error) {
      console.error('获取模型列表失败:', error)
      message.error('获取模型列表失败')
    }
  }
  
  // 上传模型
  const handleUploadModel = async (file) => {
    if (!file) {
      message.error('请选择要上传的模型文件夹')
      return
    }
    
    setDownloading(true)
    setDownloadProgress(0)
    setDownloadMessage('开始上传模型...')
    
    try {
      const formData = new FormData()
      // 对于文件夹上传，Ant Design 会将所有文件作为一个数组传递
      if (Array.isArray(file)) {
        file.forEach((f, index) => {
          formData.append('files', f)
        })
      } else {
        formData.append('files', file)
      }
      
      const response = await fetch('/api/model/upload', {
        method: 'POST',
        body: formData
      })
      
      const data = await response.json()
      
      if (data.success) {
        setDownloadMessage(`模型上传成功: ${data.model_name}`)
        setDownloadProgress(100)
        message.success(`模型上传成功，共上传 ${data.uploaded_files?.length || 0} 个文件`)
        // 重新获取模型列表
        getModels()
      } else {
        setDownloadMessage(`上传失败: ${data.error || data.message}`)
        message.error(`上传失败: ${data.error || data.message}`)
      }
    } catch (error) {
      console.error('上传模型失败:', error)
      setDownloadMessage(`上传失败: ${error.message}`)
      message.error('上传模型失败')
    } finally {
      setDownloading(false)
    }
  }
  
  // 打开模型文件夹
  const openModelFolder = async () => {
    try {
      // 获取模型文件夹路径
      const response = await fetch('/api/model/path')
      const data = await response.json()
      
      if (data.success) {
        // 尝试打开模型文件夹
        const modelsPath = data.path
        // 使用 window.open 打开本地文件夹
        window.open(`file://${modelsPath}`)
      } else {
        message.error(`获取模型文件夹路径失败: ${data.message}`)
      }
    } catch (error) {
      console.error('打开模型文件夹失败:', error)
      message.error('打开模型文件夹失败')
    }
  }
  
  // 删除模型
  const handleDeleteModel = async (modelName) => {
    try {
      const response = await fetch(`/api/model/${encodeURIComponent(modelName)}`, {
        method: 'DELETE'
      })
      
      const data = await response.json()
      
      if (data.success) {
        message.success('模型删除成功')
        // 重新获取模型列表
        getModels()
      } else {
        message.error(`删除失败: ${data.error || data.message}`)
      }
    } catch (error) {
      console.error('删除模型失败:', error)
      message.error('删除模型失败')
    }
  }
  
  // 加载模型列表
  useEffect(() => {
    if (visible) {
      getModels()
    }
  }, [visible])
  
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
          label="RAG模型"
          rules={[
            { required: true, message: '请输入RAG模型名称' }
          ]}
        >
          <Input placeholder="例如: bge-small-zh-v1.5" />
        </Form.Item>
        
        <Form.Item
          name="speechModel"
          label="语音模型"
          rules={[
            { required: true, message: '请输入语音模型名称' }
          ]}
        >
          <Input placeholder="例如: FunASR" />
        </Form.Item>
        
        <div style={{ marginBottom: 16 }}>
          <Button onClick={getModels} icon={<OrderedListOutlined />}>
            刷新模型列表
          </Button>
        </div>
        <Alert
          message="操作指引"
          description={
            <div>
              <p>1. 将模型文件夹放在 <span style={{ color: '#1890ff', cursor: 'pointer', textDecoration: 'underline' }} onClick={openModelFolder}>backend/models</span> 目录中</p>
              <p>2. 点击 "刷新模型列表" 按钮，查看已有的模型</p>
              <p>3. 在上方输入框中填入模型名称，系统会自动加载对应模型</p>
              <p>4. 系统启动时会自动检测模型状态</p>
            </div>
          }
          type="info"
          showIcon
          style={{ marginBottom: 16 }}
        />
        <Card title="已上传的模型" style={{ marginTop: 16 }}>
          {models.length > 0 ? (
            <List
              dataSource={models}
              renderItem={(model) => (
                <List.Item>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", width: "100%" }}>
                    <div>
                      <div style={{ fontWeight: "bold" }}>{model.name}</div>
                      <div style={{ fontSize: "12px", color: "#666" }}>
                        大小: {Math.round(model.size / (1024 * 1024))} MB
                      </div>
                    </div>
                    <div style={{ display: "flex", alignItems: "center" }}>
                      <Button 
                        danger 
                        size="small" 
                        onClick={() => handleDeleteModel(model.name)}
                      >
                        删除
                      </Button>
                    </div>
                  </div>
                </List.Item>
              )}
            />
          ) : (
            <div style={{ textAlign: "center", padding: 20, color: "#999" }}>
              暂无上传的模型
            </div>
          )}
        </Card>
        
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