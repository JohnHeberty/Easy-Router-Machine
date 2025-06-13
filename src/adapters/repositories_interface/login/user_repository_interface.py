from abc import ABC, abstractmethod


#### REPOSITORIO DESTINADO FUTURAMENTE PARA O LOGIN

class IUserRepository(ABC):

    @abstractmethod    
    def get_filiais(self)-> None:
        '''Retorna todas as filias '''