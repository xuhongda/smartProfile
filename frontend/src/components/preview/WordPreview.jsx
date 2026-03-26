import React, { useState, useEffect } from 'react';
import mammoth from 'mammoth';

const WordPreview = ({ file, url, isLargeFile }) => {
  // 处理file为null的情况
  if (!file) {
    return (
      <div className="p-4 bg-white rounded-lg shadow-sm">
        <div className="p-8 bg-gray-50 rounded-md border border-gray-200 text-center">
          <p className="text-red-500">文件信息不存在</p>
        </div>
      </div>
    );
  }
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [showFullContent, setShowFullContent] = useState(false);

  useEffect(() => {
    const fetchAndParseWord = async () => {
      try {
        setLoading(true);
        
        if (isLargeFile) {
          setLoadingProgress(0);
          // 模拟加载进度
          const progressInterval = setInterval(() => {
            setLoadingProgress(prev => {
              if (prev >= 90) {
                clearInterval(progressInterval);
                return prev;
              }
              return prev + 10;
            });
          }, 200);
        }

        // 检查url是否存在
        if (!url) {
          throw new Error('文件URL不存在');
        }

        const response = await fetch(url);
        
        // 检查响应状态
        if (!response.ok) {
          throw new Error(`文件获取失败: ${response.status}`);
        }

        const arrayBuffer = await response.arrayBuffer();
        
        // 检查arrayBuffer是否为空
        if (!arrayBuffer || arrayBuffer.byteLength === 0) {
          throw new Error('文件内容为空');
        }

        const result = await mammoth.convertToHtml({
          arrayBuffer
        });
        
        // 检查result是否有效
        if (!result || !result.value) {
          throw new Error('文件解析失败');
        }

        setContent(result.value);
        setError(null);
        setLoadingProgress(100);
      } catch (err) {
        console.error('Error parsing Word document:', err);
        setError(`无法预览Word文档: ${err.message}`);
      } finally {
        setLoading(false);
      }
    };

    if (url) {
      fetchAndParseWord();
    } else {
      setError('文件URL不存在');
      setLoading(false);
    }
  }, [url, isLargeFile]);

  // 切换显示完整内容
  const toggleFullContent = () => {
    setShowFullContent(!showFullContent);
  };

  if (loading) {
    return (
      <div className="p-4 bg-white rounded-lg shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-medium text-gray-800">{file.name}</h3>
          <span className="text-sm text-gray-500">{file.type || 'application/msword'}</span>
        </div>
        <div className="flex flex-col items-center justify-center p-12 bg-gray-50 rounded-md border border-gray-200">
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
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-medium text-gray-800">{file.name}</h3>
          <span className="text-sm text-gray-500">{file.type || 'application/msword'}</span>
        </div>
        <div className="p-8 bg-gray-50 rounded-md border border-gray-200 text-center">
          <p className="text-red-500">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-4 bg-white rounded-lg shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-medium text-gray-800">{file.name}</h3>
        <span className="text-sm text-gray-500">{file.type || 'application/msword'}</span>
      </div>
      <div className={`bg-gray-50 p-4 rounded-md border border-gray-200 overflow-auto transition-all duration-300 ${showFullContent ? 'max-h-[80vh]' : 'max-h-96'}`}>
        <div dangerouslySetInnerHTML={{ __html: content }} />
      </div>
      {isLargeFile && (
        <div className="mt-4 text-center">
          <button 
            onClick={toggleFullContent}
            className="text-blue-600 hover:text-blue-800 text-sm font-medium"
          >
            {showFullContent ? '收起内容' : '查看完整内容'}
          </button>
        </div>
      )}
    </div>
  );
};

export default WordPreview;