import React, { useState, useEffect } from 'react';
import { Spin, Alert, Empty, Button } from 'antd';

const NewWordPreview = ({ file, url, content, keyword = '' }) => {
  const [previewContent, setPreviewContent] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showFullContent, setShowFullContent] = useState(false);

  // 高亮关键词
  const highlightKeyword = (html, keyword) => {
    if (!keyword) return html;
    
    const escapedKeyword = keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`(${escapedKeyword})`, 'gi');
    return html.replace(regex, '<span style="background-color: #ffeb3b; padding: 0 2px; border-radius: 2px;">$1</span>');
  };

  // 加载Word文档内容
  const loadWordDocument = async () => {
    try {
      setLoading(true);
      setError(null);

      // 检查file是否存在
      if (!file) {
        throw new Error('文件信息不存在');
      }

      // 优先使用content（后端返回的HTML）
      if (content) {
        setPreviewContent(highlightKeyword(content, keyword));
        return;
      }

      // 检查url是否存在
      if (!url) {
        throw new Error('文件URL不存在');
      }

      // 从URL加载文件（旧方式，作为备用）
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`文件获取失败: ${response.status}`);
      }

      const text = await response.text();
      if (!text) {
        throw new Error('文件内容为空');
      }

      setPreviewContent(highlightKeyword(text, keyword));
    } catch (err) {
      setError(`无法预览Word文档: ${err.message}`);
      console.error('Word预览错误:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadWordDocument();
  }, [file, url, content, keyword]);

  // 切换显示完整内容
  const toggleFullContent = () => {
    setShowFullContent(!showFullContent);
  };

  // 渲染加载状态
  if (loading) {
    return (
      <div style={{ padding: '40px', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <Spin size="large" tip="正在加载Word文档..." />
      </div>
    );
  }

  // 渲染错误状态
  if (error) {
    return (
      <div style={{ padding: '40px' }}>
        <Alert
          message="预览失败"
          description={error}
          type="error"
          showIcon
        />
      </div>
    );
  }

  // 渲染空状态
  if (!previewContent) {
    return (
      <div style={{ padding: '40px' }}>
        <Empty description="文档内容为空" />
      </div>
    );
  }

  // 渲染预览内容
  return (
    <div style={{ padding: '20px' }}>
      <div style={{ marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h3 style={{ margin: 0, fontSize: '16px', fontWeight: '500' }}>{file.name}</h3>
        <span style={{ fontSize: '14px', color: '#666' }}>Word文档</span>
      </div>
      <div 
        style={{
          backgroundColor: '#f5f5f5',
          padding: '20px',
          borderRadius: '4px',
          border: '1px solid #e8e8e8',
          overflow: 'auto',
          maxHeight: showFullContent ? '70vh' : '400px',
          transition: 'max-height 0.3s ease'
        }}
        dangerouslySetInnerHTML={{ __html: previewContent }}
      />
      {previewContent.length > 1000 && (
        <div style={{ marginTop: '16px', textAlign: 'center' }}>
          <Button 
            type="link" 
            onClick={toggleFullContent}
          >
            {showFullContent ? '收起内容' : '查看完整内容'}
          </Button>
        </div>
      )}
    </div>
  );
};

export default NewWordPreview;