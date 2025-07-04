from src.infra.db.repositories.connection_repository import DatabaseRepository
from src.infra.db.repositories.routes_repository import RoutesRepository 
from src.infra.db.repositories.routes_repository import InsertLocRepository
from src.app.use_case.routes.routes_use_case import RoutesUserCase
from src.app.use_case.routes.insert_loc_use_case import InsertLocUserCase
from src.adapters.task_service.task import TaskService

# Instancia do task do manager task
def create_task_service() -> TaskService:
    '''Cria e retorna uma instância de TaskService com DatabaseRepository.'''
    return TaskService(DatabaseRepository())


### Instancias dos Repositorios
def get_routes_repository() -> RoutesRepository:
    '''Cria e retorna o Repositório de routes com o worker já instanciado.'''
    task_service = create_task_service()
    return RoutesRepository(task_service.get_worker())

def get_insert_loc_repository() -> InsertLocRepository:
    '''Cria e retorna o Repositório de insert_locs com o worker já instanciado.'''
    task_service = create_task_service()
    return InsertLocRepository(task_service.get_worker())



## Instancias uso de caso
def get_routes_use_case()-> RoutesUserCase:
    '''Instancia e retorna o caso de uso para routes.'''
    return RoutesUserCase(get_routes_repository())



def get_insert_loc_user_case() -> InsertLocUserCase:
    '''Instancia e retorna o caso de uso para inserir locais.'''
    return InsertLocUserCase(get_insert_loc_repository())