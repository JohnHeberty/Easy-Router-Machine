from typing import Optional
import pandas as pd
import logging

from src.adapters.repositories_interface.login.user_repository_interface import IUserRepository
from src.infra.db.interfaces.manager_task_interface import IManagerTask

### EXEMPLO DE USER REPORITOR PARA FILIAIS
class UserRepository(IUserRepository):
    def __init__(self, manager_task: IManagerTask) -> None:
        self.manager = manager_task        

    def get_filiais(self):
        '''Retorna todas as filiais'''
        try:
            return {"FILIAL": 1}
            
        except Exception as e:
            logging.error(f'Erro ao consultar filiais, get_filiais: {e}')
            return {}
