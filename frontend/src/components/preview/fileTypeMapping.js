import TextPreview from './TextPreview';
import ImagePreview from './ImagePreview';
import PDFPreview from './PDFPreview';
import WordPreview from './WordPreview';
import ExcelPreview from './ExcelPreview';
import VideoPreview from './VideoPreview';
import AudioPreview from './AudioPreview';

// 文件类型映射系统
const fileTypeMapping = {
  // 文本文件
  'text/plain': TextPreview,
  'text/html': TextPreview,
  'text/css': TextPreview,
  'text/javascript': TextPreview,
  'application/json': TextPreview,
  'application/xml': TextPreview,
  
  // 图片文件
  'image/jpeg': ImagePreview,
  'image/png': ImagePreview,
  'image/gif': ImagePreview,
  'image/webp': ImagePreview,
  'image/svg+xml': ImagePreview,
  
  // PDF文件
  'application/pdf': PDFPreview,
  
  // Word文档
  'application/msword': WordPreview,
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': WordPreview,
  
  // Excel表格
  'application/vnd.ms-excel': ExcelPreview,
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ExcelPreview,
  
  // 视频文件
  'video/mp4': VideoPreview,
  'video/webm': VideoPreview,
  'video/ogg': VideoPreview,
  'video/avi': VideoPreview,
  'video/mov': VideoPreview,
  'video/wmv': VideoPreview,
  
  // 音频文件
  'audio/mp3': AudioPreview,
  'audio/wav': AudioPreview,
  'audio/ogg': AudioPreview,
  'audio/m4a': AudioPreview,
  'audio/flac': AudioPreview
};

// 根据文件扩展名获取MIME类型
const extensionToMimeType = {
  '.txt': 'text/plain',
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'text/javascript',
  '.json': 'application/json',
  '.xml': 'application/xml',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.png': 'image/png',
  '.gif': 'image/gif',
  '.webp': 'image/webp',
  '.svg': 'image/svg+xml',
  '.pdf': 'application/pdf',
  '.doc': 'application/msword',
  '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  '.xls': 'application/vnd.ms-excel',
  '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  
  // 视频文件扩展名
  '.mp4': 'video/mp4',
  '.webm': 'video/webm',
  '.ogg': 'video/ogg',
  '.avi': 'video/avi',
  '.mov': 'video/mov',
  '.wmv': 'video/wmv',
  
  // 音频文件扩展名
  '.mp3': 'audio/mp3',
  '.wav': 'audio/wav',
  '.ogg': 'audio/ogg',
  '.m4a': 'audio/m4a',
  '.flac': 'audio/flac'
};

// 获取文件扩展名
const getFileExtension = (filename) => {
  const lastDotIndex = filename.lastIndexOf('.');
  if (lastDotIndex === -1) return '';
  return filename.substring(lastDotIndex).toLowerCase();
};

// 根据文件信息获取对应的预览组件
const getPreviewComponent = (file) => {
  // 优先使用file.type
  if (file.type) {
    // 直接映射文件类型
    if (file.type === 'excel') {
      return ExcelPreview;
    } else if (file.type === 'word') {
      return WordPreview;
    } else if (fileTypeMapping[file.type]) {
      return fileTypeMapping[file.type];
    }
  }
  
  // 其次根据文件扩展名推断
  const extension = getFileExtension(file.name);
  const mimeType = extensionToMimeType[extension];
  if (mimeType && fileTypeMapping[mimeType]) {
    return fileTypeMapping[mimeType];
  }
  
  // 默认使用文本预览组件
  return TextPreview;
};

export { fileTypeMapping, getPreviewComponent, getFileExtension, extensionToMimeType };