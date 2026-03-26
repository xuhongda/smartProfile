// 文件类型映射表
export const FILE_TYPE_MAPPING = {
  // 文档类型
  'excel': {
    extensions: ['xlsx', 'xls', 'csv'],
    name: 'Excel',
    category: 'document',
    icon: 'FileExcelOutlined',
    color: '#52c41a'
  },
  'word': {
    extensions: ['docx', 'doc'],
    name: 'Word',
    category: 'document',
    icon: 'FileWordOutlined',
    color: '#1890ff'
  },
  'pdf': {
    extensions: ['pdf'],
    name: 'PDF',
    category: 'document',
    icon: 'FileOutlined',
    color: '#fa541c'
  },
  'txt': {
    extensions: ['txt', 'md', 'markdown'],
    name: '文本',
    category: 'document',
    icon: 'FileTextOutlined',
    color: '#faad14'
  },
  'ppt': {
    extensions: ['pptx', 'ppt'],
    name: 'PowerPoint',
    category: 'document',
    icon: 'FileOutlined',
    color: '#f759ab'
  },
  // 图片类型
  'image': {
    extensions: ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'],
    name: '图片',
    category: 'image',
    icon: 'FileOutlined',
    color: '#13c2c2'
  },
  // 视频类型
  'video': {
    extensions: ['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv'],
    name: '视频',
    category: 'video',
    icon: 'FileOutlined',
    color: '#722ed1'
  },
  // 音频类型
  'audio': {
    extensions: ['mp3', 'wav', 'ogg', 'flac', 'aac'],
    name: '音频',
    category: 'audio',
    icon: 'FileOutlined',
    color: '#eb2f96'
  },
  // 压缩文件
  'archive': {
    extensions: ['zip', 'rar', '7z', 'tar', 'gz'],
    name: '压缩文件',
    category: 'archive',
    icon: 'FileOutlined',
    color: '#fa8c16'
  },
  // 代码文件
  'code': {
    extensions: ['py', 'js', 'ts', 'html', 'css', 'java', 'c', 'cpp', 'go', 'php'],
    name: '代码',
    category: 'code',
    icon: 'FileOutlined',
    color: '#597ef7'
  }
}

// 获取文件类型信息
export const getFileTypeInfo = (filename) => {
  if (!filename) {
    return { type: 'unknown', name: '未知', category: 'unknown', icon: 'FileOutlined', color: '#8c8c8c' }
  }
  
  const fileExt = filename.split('.').pop().toLowerCase()
  
  for (const [type, info] of Object.entries(FILE_TYPE_MAPPING)) {
    if (info.extensions.includes(fileExt)) {
      return { type, ...info }
    }
  }
  
  return { type: 'unknown', name: '未知', category: 'unknown', icon: 'FileOutlined', color: '#8c8c8c' }
}

// 获取文件类型图标
export const getFileTypeIcon = (fileType) => {
  // 由于在非JSX文件中无法使用JSX语法，我们返回图标的类型和颜色
  const iconMap = {
    'excel': { type: 'FileExcelOutlined', color: '#52c41a' },
    'word': { type: 'FileWordOutlined', color: '#1890ff' },
    'txt': { type: 'FileTextOutlined', color: '#faad14' },
    'pdf': { type: 'FileOutlined', color: '#fa541c' },
    'ppt': { type: 'FileOutlined', color: '#f759ab' },
    'image': { type: 'FileOutlined', color: '#13c2c2' },
    'video': { type: 'FileOutlined', color: '#722ed1' },
    'audio': { type: 'FileOutlined', color: '#eb2f96' },
    'archive': { type: 'FileOutlined', color: '#fa8c16' },
    'code': { type: 'FileOutlined', color: '#597ef7' },
    'unknown': { type: 'FileOutlined', color: '#8c8c8c' }
  }
  
  return iconMap[fileType] || iconMap['unknown']
}

// 高亮关键词
export const highlightKeywords = (text, keyword) => {
  if (!keyword) return text
  
  const regex = new RegExp(keyword, 'gi')
  const parts = text.split(regex)
  const matches = text.match(regex)
  
  // 返回一个数组，包含文本和高亮部分
  return parts.map((part, index) => {
    const result = [part]
    if (index < parts.length - 1) {
      result.push({ type: 'highlight', content: matches[index] })
    }
    return result
  }).flat()
}
