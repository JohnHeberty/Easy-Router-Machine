from abc import ABC, abstractmethod

class IManagerTask(ABC):
    
    @abstractmethod
    def add_task(self, query: str, return_: bool, connection_id: int) ->any:
        '''adciona tarefas na fila para os trabalhadores(workers)'''