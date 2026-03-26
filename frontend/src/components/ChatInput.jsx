import React, { useState, useEffect } from 'react';
import { Input, Button } from 'antd';
import { UpOutlined } from '@ant-design/icons';

const { TextArea } = Input;

const ChatInput = ({ inputValue, setInputValue, chatLoading, handleSendMessage, handleQuickCommand }) => {
  const [placeholder, setPlaceholder] = useState('开始探索．．．　');
  const hasContent = inputValue.trim().length > 0;
  
  useEffect(() => {
    if (inputValue.trim().length === 0) {
      const interval = setInterval(() => {
        setPlaceholder(prev => {
          if (prev === '开始探索．．．　') return '开始探索．．　';
          if (prev === '开始探索．．　') return '开始探索．　';
          if (prev === '开始探索．　') return '开始探索　';
          if (prev === '开始探索　') return '开始探索．　';
          if (prev === '开始探索．　') return '开始探索．．　';
          return '开始探索．．．　';
        });
      }, 500);
      return () => clearInterval(interval);
    }
  }, [inputValue]);
  
  return (
    <div className="chat-input">
      <div className="input-container" style={{ position: 'relative' }}>
        <TextArea
          placeholder={placeholder}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onPressEnter={handleSendMessage}
          rows={2}
          style={{ paddingRight: '40px' }}
        />
        <Button 
          type={hasContent ? "primary" : "default"}
          shape="circle"
          onClick={handleSendMessage}
          loading={chatLoading}
          icon={<UpOutlined />}
          className={hasContent ? "has-content" : ""}
          style={{
            position: 'absolute',
            bottom: '8px',
            right: '8px',
            zIndex: 1
          }}
        />
      </div>
    </div>
  );
};

export default ChatInput;