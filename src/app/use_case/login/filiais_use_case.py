from typing import Dict
import logging

from src.adapters.repositories_interface.login.user_repository_interface import IUserRepository

# EXEMPLOO
class FilialUseCase:
    def __init__(self, login: IUserRepository):
        self.login = login
        
    def execute(self)-> Dict[str, Dict]:
        '''Retoorna todas as Filiais para o Usuario'''
        try:

            result = self.login.get_filiais()
            
            if result == {}:
                return {"STATUS": True, "DADOS": None}
            
            return {"STATUS": True, "DADOS": result}
        except Exception as e:
            logging.error('Erro ao consultar filiais')
            return {"STATUS": False, "DADOS": None}