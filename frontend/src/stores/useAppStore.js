import { create } from 'zustand';

const useAppStore = create((set) => ({
  // 应用状态
  activeMenu: 'home',
  setActiveMenu: (menu) => set({ activeMenu: menu }),
  
  // AI配置抽屉状态
  aiConfigVisible: false,
  setAiConfigVisible: (visible) => set({ aiConfigVisible: visible }),
  
  // AI增强状态
  aiEnhancement: false,
  setAiEnhancement: (enabled) => set({ aiEnhancement: enabled }),
  aiResponse: null,
  setAiResponse: (response) => set({ aiResponse: response }),
}));

export default useAppStore;