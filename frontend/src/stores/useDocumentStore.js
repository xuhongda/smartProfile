import { create } from 'zustand';
import { handleUpload, handleSearch, fetchDocuments, fetchStatistics, handleDeleteDocument, handleFilePreview } from '../utils/api';
import useAppStore from './useAppStore';

const useDocumentStore = create((set, get) => ({
  // 文档列表
  documents: [],
  setDocuments: (documents) => set({ documents }),
  
  // 搜索相关
  searchKeyword: '',
  setSearchKeyword: (keyword) => set({ searchKeyword: keyword }),
  searchResults: [],
  setSearchResults: (results) => set({ searchResults: results }),
  searchLoading: false,
  setSearchLoading: (loading) => set({ searchLoading: loading }),
  
  // 文件类型筛选
  fileTypeFilter: { excel: true, word: true, txt: true },
  setFileTypeFilter: (filter) => set({ fileTypeFilter: filter }),
  
  // 排序方式
  sortBy: 'relevance',
  setSortBy: (sort) => set({ sortBy: sort }),
  
  // 统计数据
  statistics: null,
  setStatistics: (statistics) => set({ statistics }),
  
  // AI增强状态
  aiEnhancement: false,
  setAiEnhancement: (enabled) => set({ aiEnhancement: enabled }),
  aiResponse: null,
  setAiResponse: (response) => set({ aiResponse: response }),
  
  // 上传状态
  uploading: false,
  setUploading: (uploading) => set({ uploading }),
  uploadProgress: 0,
  setUploadProgress: (progress) => set({ uploadProgress: progress }),
  
  // 筛选功能
  filterVisible: false,
  setFilterVisible: (visible) => set({ filterVisible: visible }),
  filterConditions: {
    fileTypes: { excel: true, word: true, txt: true },
    dateRange: null,
    contentLength: {
      min: null,
      max: null
    }
  },
  setFilterConditions: (conditions) => set({ filterConditions: conditions }),
  filteredDocuments: [],
  setFilteredDocuments: (documents) => set({ filteredDocuments: documents }),
  previewFilterVisible: false,
  setPreviewFilterVisible: (visible) => set({ previewFilterVisible: visible }),
  previewFilterResults: [],
  setPreviewFilterResults: (results) => set({ previewFilterResults: results }),
  
  // 文件预览
  filePreviewVisible: false,
  setFilePreviewVisible: (visible) => set({ filePreviewVisible: visible }),
  filePreviewData: null,
  setFilePreviewData: (data) => set({ filePreviewData: data }),
  filePreviewLoading: false,
  setFilePreviewLoading: (loading) => set({ filePreviewLoading: loading }),
  
  // 筛选逻辑
  filteredDocs: (documents, filterConditions) => {
    return documents.filter(doc => {
      // 筛选文件类型
      if (!filterConditions.fileTypes[doc.file_type]) {
        return false;
      }
      
      // 筛选时间范围
      if (filterConditions.dateRange) {
        const [start, end] = filterConditions.dateRange;
        const docDate = new Date(doc.created_at);
        if (docDate < start || docDate > end) {
          return false;
        }
      }
      
      // 筛选内容长度
      if (filterConditions.contentLength.min !== null && doc.content_length < filterConditions.contentLength.min) {
        return false;
      }
      if (filterConditions.contentLength.max !== null && doc.content_length > filterConditions.contentLength.max) {
        return false;
      }
      
      return true;
    });
  },
  
  // 处理文件上传
  handleFileUpload: async (options) => {
    const { file, onSuccess, onError, onProgress } = options;
    const { setUploading, setUploadProgress } = get();
    // 上传前重置预览状态
    set({ filePreviewData: null, filePreviewVisible: false });
    
    return handleUpload(
      file, 
      onSuccess, 
      onError, 
      onProgress, 
      setUploading, 
      setUploadProgress, 
      get().fetchDocumentsData, 
      get().fetchStatisticsData
    );
  },
  
  // 处理搜索
  handleSearchQuery: async (keyword) => {
    const { aiEnhancement, setAiResponse, setSearchLoading, setSearchKeyword, setSearchResults } = get();
    // 检查是否包含 @AI 前缀
    const hasAiPrefix = keyword.trim().startsWith('@AI');
    // 确定是否启用 AI 增强
    const enableAi = aiEnhancement || hasAiPrefix;
    // 如果有 @AI 前缀，移除前缀
    const cleanKeyword = hasAiPrefix ? keyword.trim().substring(3).trim() : keyword;
    
    return handleSearch(
      cleanKeyword, 
      setSearchLoading, 
      setSearchKeyword, 
      setSearchResults, 
      useAppStore.getState().setActiveMenu,
      enableAi,
      setAiResponse
    );
  },
  
  // 获取文档列表
  fetchDocumentsData: async () => {
    return fetchDocuments((documents) => set({ documents }));
  },
  
  // 获取统计数据
  fetchStatisticsData: async () => {
    const { documents } = get();
    return fetchStatistics(documents, (statistics) => set({ statistics }));
  },
  
  // 处理文件预览
  handleFilePreviewLocal: async (source, getFileTypeInfo) => {
    const { documents, searchKeyword, setFilePreviewLoading, setFilePreviewData, setFilePreviewVisible } = get();
    // 预览前重置预览状态
    set({ filePreviewData: null });
    
    return handleFilePreview(
      source, 
      documents, 
      setFilePreviewLoading, 
      setFilePreviewData, 
      setFilePreviewVisible, 
      getFileTypeInfo, 
      searchKeyword
    );
  },
  
  // 处理删除文档
  handleDeleteDocumentLocal: async (docId, filename) => {
    const { searchResults, setSearchResults } = get();
    return handleDeleteDocument(
      docId, 
      filename, 
      get().fetchDocumentsData, 
      get().fetchStatisticsData, 
      searchResults, 
      setSearchResults
    );
  },
  
  // 处理筛选条件变化
  handleFilterChange: (field, value) => {
    set((state) => ({
      filterConditions: {
        ...state.filterConditions,
        [field]: value
      }
    }));
  },
  
  // 处理文件类型筛选变化
  handleFileTypeChange: (type, checked) => {
    set((state) => ({
      filterConditions: {
        ...state.filterConditions,
        fileTypes: {
          ...state.filterConditions.fileTypes,
          [type]: checked
        }
      }
    }));
  },
  
  // 处理内容长度筛选变化
  handleContentLengthChange: (field, value) => {
    set((state) => ({
      filterConditions: {
        ...state.filterConditions,
        contentLength: {
          ...state.filterConditions.contentLength,
          [field]: value
        }
      }
    }));
  },
  
  // 重置筛选条件
  resetFilters: () => {
    set({
      filterConditions: {
        fileTypes: { excel: true, word: true, txt: true },
        dateRange: null,
        contentLength: {
          min: null,
          max: null
        }
      }
    });
  },
  
  // 应用筛选
  applyFilters: () => {
    const { documents, filterConditions, setFilteredDocuments, setFilterVisible } = get();
    const filtered = get().filteredDocs(documents, filterConditions);
    setFilteredDocuments(filtered);
    setFilterVisible(false);
  },
  
  // 预览筛选结果
  previewFilters: () => {
    const { documents, filterConditions, setPreviewFilterResults, setPreviewFilterVisible } = get();
    const filtered = get().filteredDocs(documents, filterConditions);
    setPreviewFilterResults(filtered);
    setPreviewFilterVisible(true);
  }
}));

export default useDocumentStore;