import React, { useState, useEffect } from 'react';
import { Spin, Alert, Empty, Button } from 'antd';
import * as XLSX from 'xlsx';

const NewExcelPreview = ({ file, url, content }) => {
  const [sheets, setSheets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showFullContent, setShowFullContent] = useState(false);
  const [activeSheet, setActiveSheet] = useState(0);

  // 加载Excel文档内容
  const loadExcelDocument = async () => {
    try {
      setLoading(true);
      setError(null);

      // 检查file是否存在
      if (!file) {
        throw new Error('文件信息不存在');
      }

      // 优先使用content（后端返回的JSON）
      if (content) {
        // 处理后端返回的JSON数据
        if (Array.isArray(content)) {
          // 后端返回的是单个工作表的数据
          setSheets([{
            name: 'Sheet1',
            data: content
          }]);
        } else if (typeof content === 'object' && content !== null) {
          // 后端返回的是多个工作表的数据
          const sheetData = Object.entries(content).map(([name, data]) => ({
            name,
            data
          }));
          setSheets(sheetData);
        } else {
          throw new Error('无效的Excel数据格式');
        }
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

      const arrayBuffer = await response.arrayBuffer();
      if (!arrayBuffer || arrayBuffer.byteLength === 0) {
        throw new Error('文件内容为空');
      }

      // 使用xlsx解析Excel文档
      const workbook = XLSX.read(arrayBuffer, { type: 'array' });
      if (!workbook || !workbook.SheetNames || workbook.SheetNames.length === 0) {
        throw new Error('Excel文件解析失败');
      }

      // 处理每个工作表
      const sheetData = workbook.SheetNames.map(sheetName => {
        const worksheet = workbook.Sheets[sheetName];
        const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
        return { name: sheetName, data: jsonData };
      });

      setSheets(sheetData);
    } catch (err) {
      setError(`无法预览Excel文档: ${err.message}`);
      console.error('Excel预览错误:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadExcelDocument();
  }, [file, url, content]);

  // 切换显示完整内容
  const toggleFullContent = () => {
    setShowFullContent(!showFullContent);
  };

  // 渲染Excel表格
  const renderExcelTable = (data) => {
    if (!data || !Array.isArray(data) || data.length === 0) {
      return <Empty description="表格内容为空" />;
    }

    // 检查数据格式
    if (data.length > 0 && typeof data[0] === 'object' && data[0] !== null) {
      // 数据是对象数组，需要转换为二维数组
      const headers = Object.keys(data[0]);
      const rows = [headers, ...data.map(row => headers.map(header => row[header]))];
      
      return (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <tbody>
            {rows.map((row, rowIndex) => (
              <tr key={rowIndex} style={{ backgroundColor: rowIndex % 2 === 0 ? 'white' : '#f9f9f9' }}>
                {row.map((cell, cellIndex) => (
                  <td key={cellIndex} style={{ padding: '8px', border: '1px solid #e8e8e8' }}>
                    {cell || ''}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      );
    } else {
      // 数据已经是二维数组
      return (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <tbody>
            {data.map((row, rowIndex) => (
              <tr key={rowIndex} style={{ backgroundColor: rowIndex % 2 === 0 ? 'white' : '#f9f9f9' }}>
                {Array.isArray(row) ? (
                  row.map((cell, cellIndex) => (
                    <td key={cellIndex} style={{ padding: '8px', border: '1px solid #e8e8e8' }}>
                      {cell || ''}
                    </td>
                  ))
                ) : (
                  <td style={{ padding: '8px', border: '1px solid #e8e8e8' }}>
                    {row || ''}
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      );
    }
  };

  // 渲染加载状态
  if (loading) {
    return (
      <div style={{ padding: '40px', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <Spin size="large" tip="正在加载Excel文档..." />
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
  if (!sheets || sheets.length === 0) {
    return (
      <div style={{ padding: '40px' }}>
        <Empty description="Excel文档为空" />
      </div>
    );
  }

  // 渲染预览内容
  const currentSheet = sheets[activeSheet];
  return (
    <div style={{ padding: '20px' }}>
      <div style={{ marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h3 style={{ margin: 0, fontSize: '16px', fontWeight: '500' }}>{file.name}</h3>
        <span style={{ fontSize: '14px', color: '#666' }}>Excel文档</span>
      </div>

      {/* 工作表切换 */}
      {sheets.length > 1 && (
        <div style={{ marginBottom: '20px' }}>
          <div style={{ marginBottom: '10px', fontSize: '14px', fontWeight: '500' }}>工作表:</div>
          <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
            {sheets.map((sheet, index) => (
              <button
                key={index}
                onClick={() => setActiveSheet(index)}
                style={{
                  padding: '4px 12px',
                  border: '1px solid #d9d9d9',
                  borderRadius: '4px',
                  backgroundColor: activeSheet === index ? '#1890ff' : 'white',
                  color: activeSheet === index ? 'white' : '#333',
                  cursor: 'pointer',
                  fontSize: '14px'
                }}
              >
                {sheet.name}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* 表格内容 */}
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
      >
        {renderExcelTable(currentSheet.data)}
      </div>

      {currentSheet.data.length > 20 && (
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

export default NewExcelPreview;