from src.infra.db.repositories.connection_repository import DatabaseRepository
from src.app.use_case.login.user_register_use_case import UserRegisterUseCase
from src.app.use_case.login.user_login_use_case import UserLoginUseCase
from src.infra.db.repositories.user_repository import UserRepository
from src.app.use_case.login.filiais_use_case import FilialUseCase
from src.adapters.task_service.cache_depends import get_cache
from src.adapters.task_service.task import TaskService

def create_task_service() -> TaskService:
    '''Cria e retorna uma instância de TaskService com DatabaseRepository.'''
    return TaskService(DatabaseRepository())


def get_login_repository() -> UserRepository:
    '''Cria e retorna o Repositório de login com o worker já instanciado.'''
    task_service = create_task_service()
    return UserRepository(task_service.get_worker(), get_cache(db=0))


def get_login_use_case() -> UserLoginUseCase:
    '''Instancia e retorna o caso de uso para login.'''
    return UserLoginUseCase(get_login_repository())


def get_register_use_case() -> UserRegisterUseCase:
    '''Instancia e retorna o caso de uso para registro.'''
    return UserRegisterUseCase(get_login_repository())


def get_filial_use_case()-> FilialUseCase:
    '''Instancia e retorna o caso de uso para Filials.'''
    return FilialUseCase(get_login_repository(), get_cache(db=0))
