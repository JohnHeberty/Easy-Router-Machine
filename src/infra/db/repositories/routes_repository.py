from typing import Optional
import pandas as pd
import logging

from src.adapters.repositories_interface.routes.routes_repository_interface import IRoutesRepository
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