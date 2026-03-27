import { create } from 'zustand';

const useChatStore = create((set, get) => ({
  // 聊天消息
  messages: [
    {
      id: 1,
      role: 'assistant',
      content: '你好！我是你的智能文档助手。你可以问我关于财务报表、会议纪要或 2025 计划的问题。',
      timestamp: new Date().toISOString()
    }
  ],
  setMessages: (messages) => set({ messages }),
  addMessage: (message) => set((state) => ({
    messages: [...state.messages, message]
  })),
  
  // 聊天输入
  inputValue: '',
  setInputValue: (value) => set({ inputValue: value }),
  
  // 聊天加载状态
  chatLoading: false,
  setChatLoading: (loading) => set({ chatLoading: loading }),
  
  // AI模式
  aiMode: false, // 模拟AI插件是否安装
  setAiMode: (mode) => set({ aiMode: mode }),
  
  // 打字状态
  typingText: '',
  setTypingText: (text) => set({ typingText: text }),
  typingInterval: null,
  setTypingInterval: (interval) => set({ typingInterval: interval }),
  currentMessageId: null,
  setCurrentMessageId: (id) => set({ currentMessageId: id }),
  
  // 清理定时器
  clearTypingInterval: () => {
    const { typingInterval } = get();
    if (typingInterval) {
      clearInterval(typingInterval);
      set({ typingInterval: null });
    }
  }
}));

export default useChatStore;