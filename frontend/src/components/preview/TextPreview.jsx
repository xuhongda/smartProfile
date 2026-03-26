import React, { useState, useEffect, useRef } from 'react';

const TextPreview = ({ file, content, isLargeFile }) => {
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
  const [displayContent, setDisplayContent] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [showFullContent, setShowFullContent] = useState(false);
  const [loadingProgress, setLoadingProgress] = useState(0);
  const textRef = useRef(null);

  // 流式加载大文件内容
  useEffect(() => {
    if (content) {
      if (isLargeFile) {
        setIsLoading(true);
        setLoadingProgress(0);
        
        // 分块加载内容
        const chunkSize = 10000; // 每块10KB
        const totalChunks = Math.ceil(content.length / chunkSize);
        let currentChunk = 0;
        let loadedContent = '';

        const loadChunk = () => {
          if (currentChunk < totalChunks) {
            const start = currentChunk * chunkSize;
            const end = Math.min(start + chunkSize, content.length);
            loadedContent += content.substring(start, end);
            setDisplayContent(loadedContent);
            currentChunk++;
            setLoadingProgress(Math.floor((currentChunk / totalChunks) * 100));
            
            // 使用requestAnimationFrame优化渲染
            requestAnimationFrame(loadChunk);
          } else {
            setIsLoading(false);
          }
        };

        loadChunk();
      } else {
        setDisplayContent(content);
        setIsLoading(false);
      }
    }
  }, [content, isLargeFile]);

  // 切换显示完整内容
  const toggleFullContent = () => {
    setShowFullContent(!showFullContent);
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-medium text-gray-800">{file.name}</h3>
        <span className="text-sm text-gray-500">{file.type || 'text/plain'}</span>
      </div>
      
      {isLoading ? (
        <div className="bg-gray-50 p-4 rounded-md border border-gray-200">
          <div className="flex flex-col items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mb-4"></div>
            <p className="text-gray-600 mb-2">正在加载文件内容...</p>
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div 
                className="bg-blue-600 h-2.5 rounded-full" 
                style={{ width: `${loadingProgress}%` }}
              ></div>
            </div>
            <p className="text-sm text-gray-500 mt-2">{loadingProgress}%</p>
          </div>
        </div>
      ) : (
        <div className="bg-gray-50 p-4 rounded-md border border-gray-200">
          <pre 
            ref={textRef}
            className={`whitespace-pre-wrap font-mono text-sm text-gray-800 overflow-auto transition-all duration-300 ${showFullContent ? 'max-h-[80vh]' : 'max-h-96'}`}
          >
            {displayContent}
          </pre>
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
      )}
    </div>
  );
};

export default TextPreview;