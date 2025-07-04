from typing import Optional
import pandas as pd
import logging

from src.adapters.repositories_interface.routes.routes_repository_interface import IRoutesRepository
from src.adapters.repositories_interface.routes.routes_repository_interface import IInsertLocRepository

from src.infra.db.interfaces.manager_task_interface import IManagerTask
from src.infra.templates.routes.routes_template import *

class RoutesRepository(IRoutesRepository):
    def __init__(self, manager_task: IManagerTask) -> None:
        self.manager = manager_task        

    def get_route(self, lat_init, log_init, lat_fim, log_fim):
        '''Retorna uma rota dado latitude e longitude do inicio e fim '''
        try:
            query = router_time.format(lat_init, log_init, lat_fim, log_fim)
            data = self.manager.add_task(query, True)
            data.event.wait()
            dados = data.result
            return dados
        except Exception as e:
            logging.error(f'Erro ao fazer rota: {str(e)}')
            print(str(e))
            return pd.DataFrame
        
    def get_locales_route(self, linestring) -> pd.DataFrame:
        '''Retorna os postos de combustíveis mais próximos com base na latitude e longitude fornecidas'''
        try:
            query = postos_na_rota.format(linestring)
            data = self.manager.add_task(query, True, 1)
            data.event.wait()
            dados = data.result
            return dados
        except Exception as e:
            logging.error(f'Erro ao obter locais de passagem da rota: {str(e)}')
            print(str(e))
            return pd.DataFrame({"STATUS": False, "DADOS": [], "ERRO": str(e)})

class InsertLocRepository(IInsertLocRepository):
    def __init__(self, manager_task: IManagerTask) -> None:
        self.manager = manager_task  

    def insert_loc_unique(self, nome, tipo, data_cadastro, geom_point) -> pd.DataFrame:
        '''Insere uma localidade no banco de dados'''
        try:
            query = insert_loc_unique_query.format(nome, tipo, data_cadastro, geom_point)
            data = self.manager.add_task(query, False, 1)
            data.event.wait()
            flag = data.result

            return flag
        
        except Exception as e:
            logging.error(f'Erro ao inserir local: {str(e)}')
            print(str(e))
            return False