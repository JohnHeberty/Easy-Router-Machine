from src.infra.db.interfaces.connection_repository_interface import IDatabaseRepository
from src.infra.manager_task.manager_task import ManagerTask
from src.infra.manager_task.singleton import SingletonMeta

class TaskService(metaclass=SingletonMeta):
    '''Inicia uma unica task apos a primeira instância'''
    def __init__(self, database_repository: IDatabaseRepository):
        self.managerTask = ManagerTask(database_repository)
        
    def get_worker(self) -> any:
        '''Retorna a instancia do ManagerTask'''
        return self.managerTask