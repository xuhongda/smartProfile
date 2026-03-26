import React, { useState, useEffect, useRef } from 'react';
import { getPreviewComponent } from './fileTypeMapping';

const FilePreviewContainer = ({ file, url, content }) => {
  const [PreviewComponent, setPreviewComponent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [fileSize, setFileSize] = useState(0);
  const [isLargeFile, setIsLargeFile] = useState(false);
  const [loadingProgress, setLoadingProgress] = useState(0);
  const fileInputRef = useRef(null);

  // 检测文件大小
  const checkFileSize = (file) => {
    if (file && file.size) {
      setFileSize(file.size);
      // 定义大文件阈值（1MB）
      setIsLargeFile(file.size > 1024 * 1024);
    }
  };

  // 模拟流式加载进度
  const simulateLoadingProgress = () => {
    let progress = 0;
    const interval = setInterval(() => {
      progress += 5;
      setLoadingProgress(progress);
      if (progress >= 100) {
        clearInterval(interval);
      }
    }, 100);
    return interval;
  };

  useEffect(() => {
    checkFileSize(file);
  }, [file]);

  useEffect(() => {
    let progressInterval;
    try {
      setLoading(true);
      if (isLargeFile) {
        progressInterval = simulateLoadingProgress();
      }
      // 确保file不为null
      if (file) {
        const component = getPreviewComponent(file);
        setPreviewComponent(component);
        setError(null);
      } else {
        setError('文件信息不存在');
        setPreviewComponent(null);
      }
    } catch (err) {
      console.error('Error getting preview component:', err);
      setError('无法加载预览组件');
      setPreviewComponent(null);
    } finally {
      if (progressInterval) {
        clearInterval(progressInterval);
      }
      setLoading(false);
    }
  }, [file, isLargeFile]);

  if (loading) {
    return (
      <div className="p-4 bg-white rounded-lg shadow-sm">
        <div className="flex justify-center items-center p-12 bg-gray-50 rounded-md border border-gray-200">
          {isLargeFile ? (
            <div className="text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-4"></div>
              <p className="text-gray-600 mb-2">正在加载大文件...</p>
              <div className="w-64 bg-gray-200 rounded-full h-2.5 mx-auto">
                <div 
                  className="bg-blue-600 h-2.5 rounded-full" 
                  style={{ width: `${loadingProgress}%` }}
                ></div>
              </div>
              <p className="text-sm text-gray-500 mt-2">{loadingProgress}%</p>
            </div>
          ) : (
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
          )}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-white rounded-lg shadow-sm">
        <div className="p-8 bg-gray-50 rounded-md border border-gray-200 text-center">
          <p className="text-red-500">{error}</p>
        </div>
      </div>
    );
  }

  if (!PreviewComponent) {
    return (
      <div className="p-4 bg-white rounded-lg shadow-sm">
        <div className="p-8 bg-gray-50 rounded-md border border-gray-200 text-center">
          <p className="text-gray-500">不支持的文件类型</p>
        </div>
      </div>
    );
  }

  // 检查file是否为null
  if (!file) {
    return (
      <div className="p-4 bg-white rounded-lg shadow-sm">
        <div className="p-8 bg-gray-50 rounded-md border border-gray-200 text-center">
          <p className="text-red-500">文件信息不存在</p>
        </div>
      </div>
    );
  }

  // 安全渲染PreviewComponent，添加错误边界
  const SafePreviewComponent = () => {
    try {
      // 确保PreviewComponent存在
      if (!PreviewComponent) {
        return (
          <div className="p-8 bg-gray-50 rounded-md border border-gray-200 text-center">
            <p className="text-red-500">预览组件不存在</p>
          </div>
        );
      }
      
      // 确保file存在
      if (!file) {
        return (
          <div className="p-8 bg-gray-50 rounded-md border border-gray-200 text-center">
            <p className="text-red-500">文件信息不存在</p>
          </div>
        );
      }
      
      return (
        <PreviewComponent 
          file={file} 
          url={url} 
          content={content} 
          isLargeFile={isLargeFile} 
        />
      );
    } catch (err) {
      console.error('Preview component error:', err);
      return (
        <div className="p-8 bg-gray-50 rounded-md border border-gray-200 text-center">
          <p className="text-red-500">预览组件加载失败</p>
          <p className="text-sm text-gray-500 mt-2">{err.message}</p>
        </div>
      );
    }
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow-sm">
      {fileSize > 0 && (
        <div className="mb-4 text-sm text-gray-500">
          文件大小: {formatFileSize(fileSize)}
          {isLargeFile && <span className="ml-2 text-yellow-500">（大文件）</span>}
        </div>
      )}
      <SafePreviewComponent />
    </div>
  );
};

// 格式化文件大小
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

export default FilePreviewContainer;