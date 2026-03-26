import React from 'react';
import { Button } from 'antd';

const ChatHeader = ({ aiMode, setAiMode }) => {
  return (
    <div className="chat-header" style={{ display: 'flex', justifyContent: 'flex-end', padding: '8px 16px', borderBottom: '1px solid #f0f0f0' }}>
      <Button 
        type={aiMode ? "primary" : "default"}
        onClick={() => setAiMode(!aiMode)}
        size="small"
      >
        {aiMode ? "增强模式" : "基础模式"}
      </Button>
    </div>
  );
};

export default ChatHeader;