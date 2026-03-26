import React, { useState, useEffect } from 'react';
import * as XLSX from 'xlsx';

const ExcelPreview = ({ file, url, isLargeFile }) => {
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
  const [sheets, setSheets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [showFullContent, setShowFullContent] = useState(false);
  const [displayedSheets, setDisplayedSheets] = useState([]);

  useEffect(() => {
    const fetchAndParseExcel = async () => {
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

        const workbook = XLSX.read(arrayBuffer, { type: 'array' });
        
        // 检查workbook是否有效
        if (!workbook || !workbook.SheetNames || workbook.SheetNames.length === 0) {
          throw new Error('Excel文件解析失败');
        }

        const sheetData = workbook.SheetNames.map(sheetName => {
          const worksheet = workbook.Sheets[sheetName];
          // 对于大文件，限制加载的行数
          const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
          return { name: sheetName, data: jsonData };
        });
        
        setSheets(sheetData);
        // 对于大文件，只显示第一个工作表的前50行
        if (isLargeFile && sheetData.length > 0) {
          const limitedSheet = {
            ...sheetData[0],
            data: sheetData[0].data.slice(0, 50)
          };
          setDisplayedSheets([limitedSheet]);
        } else {
          setDisplayedSheets(sheetData);
        }
        setError(null);
        setLoadingProgress(100);
      } catch (err) {
        console.error('Error parsing Excel document:', err);
        setError(`无法预览Excel文档: ${err.message}`);
      } finally {
        setLoading(false);
      }
    };

    if (url) {
      fetchAndParseExcel();
    } else {
      setError('文件URL不存在');
      setLoading(false);
    }
  }, [url, isLargeFile]);

  // 切换显示完整内容
  const toggleFullContent = () => {
    setShowFullContent(!showFullContent);
    if (!showFullContent) {
      setDisplayedSheets(sheets);
    } else if (isLargeFile && sheets.length > 0) {
      const limitedSheet = {
        ...sheets[0],
        data: sheets[0].data.slice(0, 50)
      };
      setDisplayedSheets([limitedSheet]);
    }
  };

  if (loading) {
    return (
      <div className="p-4 bg-white rounded-lg shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-medium text-gray-800">{file.name}</h3>
          <span className="text-sm text-gray-500">{file.type || 'application/vnd.ms-excel'}</span>
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
          <span className="text-sm text-gray-500">{file.type || 'application/vnd.ms-excel'}</span>
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
        <span className="text-sm text-gray-500">{file.type || 'application/vnd.ms-excel'}</span>
      </div>
      <div className={`bg-gray-50 p-4 rounded-md border border-gray-200 overflow-auto transition-all duration-300 ${showFullContent ? 'max-h-[80vh]' : 'max-h-96'}`}>
        {displayedSheets.map((sheet, index) => (
          <div key={index} className="mb-6">
            <h4 className="text-md font-medium text-gray-700 mb-2">{sheet.name}</h4>
            <div className="overflow-x-auto">
              <table className="min-w-full border border-gray-300">
                <tbody>
                  {sheet.data.map((row, rowIndex) => (
                    <tr key={rowIndex} className={rowIndex % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                      {row.map((cell, cellIndex) => (
                        <td key={cellIndex} className="border border-gray-300 px-3 py-2 text-sm">
                          {cell || ''}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {isLargeFile && !showFullContent && sheet.data.length === 50 && (
              <p className="text-sm text-gray-500 mt-2">仅显示前50行...</p>
            )}
          </div>
        ))}
        {isLargeFile && sheets.length > 1 && !showFullContent && (
          <p className="text-sm text-gray-500 mt-2">仅显示第一个工作表...</p>
        )}
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

export default ExcelPreview;