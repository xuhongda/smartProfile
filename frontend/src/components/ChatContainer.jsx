import React, { useRef, useEffect } from 'react';
import ChatHeader from './ChatHeader';
import ChatMessages from './ChatMessages';
import ChatInput from './ChatInput';

const ChatContainer = ({ 
  messages, 
  inputValue, 
  setInputValue, 
  chatLoading, 
  typingText, 
  aiMode, 
  setAiMode, 
  handleSendMessage, 
  handleFilePreview, 
  highlightKeywords,
  handleQuickCommand
}) => {
  const chatMessagesRef = useRef(null);

  // 自动滚动到底部
  useEffect(() => {
    if (chatMessagesRef.current) {
      chatMessagesRef.current.scrollTop = chatMessagesRef.current.scrollHeight;
    }
  }, [messages, typingText]);

  // 组件挂载时滚动到底部
  useEffect(() => {
    const timer = setTimeout(() => {
      if (chatMessagesRef.current) {
        chatMessagesRef.current.scrollTop = chatMessagesRef.current.scrollHeight;
      }
    }, 100);

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="chat-container" style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <div className="chat-card" style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <ChatHeader aiMode={aiMode} setAiMode={setAiMode} />
        <div 
          ref={chatMessagesRef} 
          className="chat-messages" 
          style={{ 
            flex: 1, 
            overflowY: 'scroll', 
            minHeight: 0,
            maxHeight: 'calc(100vh - 200px)',
            scrollbarWidth: 'thin',
            scrollbarColor: '#c1c1c1 #f1f1f1',
            position: 'relative'
          }}
        >
          <ChatMessages 
            messages={messages} 
            typingText={typingText} 
            highlightKeywords={highlightKeywords} 
            handleFilePreview={handleFilePreview} 
          />
        </div>
        <div style={{ borderTop: '1px solid #f0f0f0', flexShrink: 0 }}>
          <ChatInput 
            inputValue={inputValue} 
            setInputValue={setInputValue} 
            chatLoading={chatLoading} 
            handleSendMessage={handleSendMessage}
            handleQuickCommand={handleQuickCommand}
          />
        </div>
      </div>
    </div>
  );
};

export default ChatContainer;