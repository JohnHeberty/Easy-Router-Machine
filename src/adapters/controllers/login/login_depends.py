from src.infra.db.repositories.connection_repository import DatabaseRepository
from src.infra.db.repositories.user_repository import UserRepository
from src.app.use_case.login.filiais_use_case import FilialUseCase
from src.adapters.task_service.task import TaskService

# Instancia do task do manager task
def create_task_service() -> TaskService:
    '''Cria e retorna uma instância de TaskService com DatabaseRepository.'''
    return TaskService(DatabaseRepository())


### Instancias dos Repositorios
def get_login_repository() -> UserRepository:
    '''Cria e retorna o Repositório de login com o worker já instanciado.'''
    task_service = create_task_service()
    return UserRepository(task_service.get_worker())


## Instancias uso de caso
def get_filial_use_case()-> FilialUseCase:
    '''Instancia e retorna o caso de uso para Filials.'''
    return FilialUseCase(get_login_repository())