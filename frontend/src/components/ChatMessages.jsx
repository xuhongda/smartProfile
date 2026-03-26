import React, { useEffect, useRef } from 'react';
import { Card, Button, Tooltip } from 'antd';
import { EyeOutlined } from '@ant-design/icons';

const ChatMessages = ({ messages, typingText, highlightKeywords, handleFilePreview }) => {
  const messagesEndRef = useRef(null);

  // 自动滚动到底部
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // 当消息更新时自动滚动到底部
  useEffect(() => {
    scrollToBottom();
  }, [messages, typingText]);

  return (
    <div className="chat-messages" style={{ padding: '16px' }}>
      {messages.map(message => (
        <div 
          key={message.id} 
          className={`message ${message.role}`}
          style={{
            display: 'flex',
            marginBottom: '16px',
            justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start'
          }}
        >
          <div 
            className="message-content"
            style={{
              maxWidth: '70%',
              padding: '12px',
              borderRadius: '16px',
              backgroundColor: message.role === 'user' ? '#1890ff' : '#f0f0f0',
              color: message.role === 'user' ? '#fff' : '#333'
            }}
          >
            {message.isThinking ? (
              <div className="thinking">
                <span>{message.content}</span>
              </div>
            ) : (
              <>
                <p style={{ margin: 0 }}>{message.content}</p>
                {message.sources && message.sources.length > 0 && (
                  <div className="message-sources" style={{ marginTop: '8px' }}>
                    <h4 style={{ margin: '0 0 8px 0', fontSize: '12px' }}>参考来源：</h4>
                    {message.sources.map(source => (
                      <Card 
                        key={source.id} 
                        size="small" 
                        className="source-card"
                        style={{
                          marginBottom: '8px',
                          backgroundColor: message.role === 'user' ? 'rgba(255, 255, 255, 0.2)' : 'rgba(255, 255, 255, 0.8)'
                        }}
                      >
                        <div className="source-info">
                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                            <span className="source-filename" style={{ fontSize: '12px' }}>{source.filename}</span>
                            <Button 
                              size="small" 
                              type="link" 
                              icon={<EyeOutlined />}
                              onClick={() => handleFilePreview(source)}
                              style={{ color: message.role === 'user' ? '#fff' : '#1890ff' }}
                            >
                              预览
                            </Button>
                          </div>
                          <p className="source-snippet" style={{ fontSize: '12px', margin: 0 }}>
                            {source.keyword ? highlightKeywords(source.snippet, source.keyword) : source.snippet}
                          </p>
                        </div>
                      </Card>
                    ))}
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      ))}
      {typingText && (
        <div 
          className="message assistant"
          style={{
            display: 'flex',
            marginBottom: '16px',
            justifyContent: 'flex-start'
          }}
        >
          <div 
            className="message-content"
            style={{
              maxWidth: '70%',
              padding: '12px',
              borderRadius: '16px',
              backgroundColor: '#f0f0f0',
              color: '#333'
            }}
          >
            <p style={{ margin: 0 }}>{typingText}</p>
          </div>
        </div>
      )}
      {/* 占位元素，确保输入框始终在底部 */}
      {messages.length === 0 && !typingText && (
        <div style={{ flex: 1 }} />
      )}
      {/* 用于自动滚动的参考元素 */}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatMessages;