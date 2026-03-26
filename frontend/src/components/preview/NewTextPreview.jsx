import React, { useState, useEffect } from 'react';
import { Spin, Alert, Empty, Button } from 'antd';

const NewTextPreview = ({ file, content, keyword = '' }) => {
  const [previewContent, setPreviewContent] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showFullContent, setShowFullContent] = useState(false);

  // 高亮关键词
  const highlightKeyword = (text, keyword) => {
    if (!keyword) return text;
    
    const escapedKeyword = keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`(${escapedKeyword})`, 'gi');
    return text.replace(regex, '<span style="background-color: #ffeb3b; padding: 0 2px; border-radius: 2px;">$1</span>');
  };

  // 加载和显示文本内容
  const loadTextContent = async () => {
    try {
      setLoading(true);
      setError(null);

      // 检查file是否存在
      if (!file) {
        throw new Error('文件信息不存在');
      }

      // 检查content是否存在
      if (!content) {
        throw new Error('文件内容为空');
      }

      // 处理content，确保它是字符串
      if (typeof content === 'object' && content !== null) {
        try {
          // 如果是对象，尝试转换为JSON字符串
          const jsonString = JSON.stringify(content, null, 2);
          setPreviewContent(highlightKeyword(jsonString, keyword));
        } catch (jsonError) {
          // 如果转换失败，使用toString()
          setPreviewContent(highlightKeyword(String(content), keyword));
        }
      } else {
        // 如果已经是字符串，直接使用
        setPreviewContent(highlightKeyword(String(content), keyword));
      }
    } catch (err) {
      setError(`无法预览文本文件: ${err.message}`);
      console.error('文本预览错误:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTextContent();
  }, [file, content, keyword]);

  // 切换显示完整内容
  const toggleFullContent = () => {
    setShowFullContent(!showFullContent);
  };

  // 渲染加载状态
  if (loading) {
    return (
      <div style={{ padding: '40px', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <Spin size="large" tip="正在加载文本文件..." />
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
        <Empty description="文本内容为空" />
      </div>
    );
  }

  // 渲染预览内容
  return (
    <div style={{ padding: '20px' }}>
      <div style={{ marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h3 style={{ margin: 0, fontSize: '16px', fontWeight: '500' }}>{file.name}</h3>
        <span style={{ fontSize: '14px', color: '#666' }}>文本文件</span>
      </div>
      <div 
        style={{
          backgroundColor: '#f5f5f5',
          padding: '20px',
          borderRadius: '4px',
          border: '1px solid #e8e8e8',
          overflow: 'auto',
          maxHeight: showFullContent ? '70vh' : '400px',
          transition: 'max-height 0.3s ease',
          fontFamily: 'monospace',
          fontSize: '14px',
          lineHeight: '1.5'
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

export default NewTextPreview;