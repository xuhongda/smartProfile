# 后端项目组件化架构设计

## 1. 组件架构图

```
┌─────────────────┐
│  FastAPI框架层  │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  框架适配器层   │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  依赖注入容器   │
└─────────────────┘
         │
         ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  文件解析组件   │  │  搜索服务组件   │  │  文档管理组件   │
└─────────────────┘  └─────────────────┘  └─────────────────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  分词处理组件   │
                  └─────────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  数据库操作组件  │
                  └─────────────────┘
```

## 2. 核心组件设计

### 2.1 文件解析组件 (FileParser)
- **职责**: 解析不同类型的文件（Excel、Word、Text）
- **接口**:
  - `parse_file(file_content: bytes, filename: str) -> FileParseResult`
  - `supports_file_type(filename: str) -> bool`
- **依赖**: pandas, python-docx, chardet

### 2.2 搜索服务组件 (SearchService)
- **职责**: 提供全文搜索功能
- **接口**:
  - `search(query: str, page: int = 1, page_size: int = 10) -> SearchResult`
  - `get_search_count(query: str) -> int`
- **依赖**: 分词处理组件, 数据库操作组件

### 2.3 文档管理组件 (DocumentManager)
- **职责**: 管理文档的CRUD操作
- **接口**:
  - `create_document(filename: str, file_type: str, content: str) -> Document`
  - `update_document(doc_id: int, content: str, file_type: str) -> Document`
  - `delete_document(doc_id: int) -> bool`
  - `get_document(doc_id: int) -> Document`
  - `get_documents(page: int = 1, page_size: int = 10) -> DocumentList`
- **依赖**: 数据库操作组件

### 2.4 分词处理组件 (Tokenizer)
- **职责**: 处理中文分词
- **接口**:
  - `tokenize_text(text: str) -> str`
  - `tokenize_query(query: str) -> str`
  - `is_chinese(text: str) -> bool`
- **依赖**: jieba

### 2.5 数据库操作组件 (Database)
- **职责**: 处理数据库连接和操作
- **接口**:
  - `get_session() -> Session`
  - `init_database()`
  - `bulk_insert(model, data_list)`
  - `bulk_update(model, data_list, primary_key='id')`
- **依赖**: SQLAlchemy

### 2.6 依赖注入容器 (Container)
- **职责**: 管理组件间的依赖关系
- **接口**:
  - `register(name, instance)`
  - `resolve(name)`
  - `get_all()`

### 2.7 框架适配器 (FrameworkAdapter)
- **职责**: 连接FastAPI框架和业务组件
- **接口**:
  - `adapt_request(request_data) -> BusinessModel`
  - `adapt_response(business_result) -> APIResponse`

## 3. 数据模型设计

### 3.1 业务模型
- **FileParseResult**:
  - `filename: str`
  - `file_type: str`
  - `content: str`
  - `content_length: int`

- **SearchResult**:
  - `query: str`
  - `total: int`
  - `page: int`
  - `page_size: int`
  - `total_pages: int`
  - `results: List[SearchItem]`

- **SearchItem**:
  - `id: int`
  - `filename: str`
  - `file_type: str`
  - `content: str`
  - `snippet: str`
  - `file_path: str`
  - `created_at: datetime`
  - `updated_at: datetime`

- **Document**:
  - `id: int`
  - `filename: str`
  - `file_type: str`
  - `content: str`
  - `content_length: int`
  - `created_at: datetime`
  - `updated_at: datetime`

- **DocumentList**:
  - `total: int`
  - `page: int`
  - `page_size: int`
  - `total_pages: int`
  - `documents: List[Document]`

### 3.2 API响应模型
- **APIResponse**:
  - `success: bool`
  - `message: str`
  - `data: Any`

## 4. 组件间通信机制

- **依赖注入**: 通过依赖注入容器获取所需组件
- **接口调用**: 组件间通过定义的接口进行通信
- **事件机制**: 支持组件间的事件通知（可选）

## 5. 配置管理

- **配置文件**: `config.py` 存储配置信息
- **环境变量**: 支持通过环境变量覆盖配置
- **依赖注入**: 配置通过依赖注入方式提供给组件

## 6. 测试策略

- **单元测试**: 针对每个组件的独立测试
- **集成测试**: 测试组件间的协作
- **API测试**: 测试API接口行为

## 7. 实现注意事项

- **业务逻辑不依赖框架**: 业务组件不得直接引用FastAPI特定的API
- **依赖注入**: 使用依赖注入而非硬编码方式获取资源
- **接口规范**: 严格遵循定义的接口规范
- **错误处理**: 统一的错误处理机制
- **日志记录**: 组件级别的日志记录

## 8. 迁移策略

1. 实现核心业务组件
2. 实现依赖注入容器
3. 重构FastAPI框架层
4. 编写测试用例
5. 验证功能一致性
6. 优化和清理