from .tokenizer_service import TokenizerService
from .file_parser_service import FileParserService
from .database_service import DatabaseService
from .document_manager_service import DocumentManagerService
from .search_service import SearchService
from .file_type_service import FileTypeService
from .generic_ai_client import GenericAIClient
from .model_manager_service import ModelManagerService
from core.utils.container import Container
from core.utils.config import config

# 创建依赖注入容器
container = Container()

# 初始化服务
database_service = DatabaseService(config.get('database.url'))
tokenizer_service = TokenizerService()
file_type_service = FileTypeService()
file_parser_service = FileParserService()
document_manager_service = DocumentManagerService(database_service)
generic_ai_client = GenericAIClient()
search_service = SearchService(tokenizer_service, database_service)
model_manager_service = ModelManagerService(config)

# 注册服务到容器
container.register('config', config)
container.register('database_service', database_service)
container.register('tokenizer_service', tokenizer_service)
container.register('file_type_service', file_type_service)
container.register('file_parser_service', file_parser_service)
container.register('document_manager_service', document_manager_service)
container.register('generic_ai_client', generic_ai_client)
container.register('search_service', search_service)
container.register('model_manager_service', model_manager_service)

__all__ = [
    "TokenizerService",
    "FileParserService",
    "DatabaseService",
    "DocumentManagerService",
    "SearchService",
    "FileTypeService",
    "GenericAIClient",
    "ModelManagerService",
    "container"
]
