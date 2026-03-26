import React, { useState, useEffect } from 'react';
import { Spin, Alert, Empty } from 'antd';
import { getFileExtension } from './fileTypeMapping';

// 导入新的预览组件
import NewWordPreview from './NewWordPreview';
import NewExcelPreview from './NewExcelPreview';
import NewTextPreview from './NewTextPreview';

const NewFilePreviewContainer = ({ file, url, content, keyword = '' }) => {
  const [previewComponent, setPreviewComponent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [fileType, setFileType] = useState('');

  // 确定文件类型并选择对应的预览组件
  const determinePreviewComponent = () => {
    if (!file) {
      setError('文件信息不存在');
      setLoading(false);
      return;
    }

    try {
      // 优先使用file.type
      let type = file.type;
      
      // 如果没有file.type，根据文件名扩展名推断
      if (!type) {
        const extension = getFileExtension(file.name);
        switch (extension) {
          case '.doc':
          case '.docx':
            type = 'word';
            break;
          case '.xls':
          case '.xlsx':
            type = 'excel';
            break;
          case '.txt':
          case '.md':
          case '.json':
          case '.xml':
          case '.html':
            type = 'text';
            break;
          default:
            type = 'unknown';
        }
      }

      setFileType(type);

      // 根据文件类型选择预览组件
      switch (type) {
        case 'word':
          setPreviewComponent(
            <NewWordPreview file={file} url={url} content={content} keyword={keyword} />
          );
          break;
        case 'excel':
          setPreviewComponent(
            <NewExcelPreview file={file} url={url} content={content} keyword={keyword} />
          );
          break;
        case 'text':
        case 'txt':
          setPreviewComponent(
            <NewTextPreview file={file} content={content} keyword={keyword} />
          );
          break;
        default:
          setError(`不支持的文件类型: ${type}`);
      }
    } catch (err) {
      setError(`预览组件加载失败: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    determinePreviewComponent();
  }, [file, url, content]);

  // 渲染加载状态
  if (loading) {
    return (
      <div style={{ padding: '40px', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <Spin size="large" tip="正在准备预览..." />
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

  // 渲染预览组件
  if (previewComponent) {
    return previewComponent;
  }

  // 渲染空状态
  return (
    <div style={{ padding: '40px' }}>
      <Empty description="无法预览该文件" />
    </div>
  );
};

export default NewFilePreviewContainer;