from abc import ABC, abstractmethod
import json
import pandas as pd

class IRoutesRepository(ABC):

    @abstractmethod    
    def get_route(self, lat_init, log_init, lat_fim, log_fim) -> pd.DataFrame:
        '''Retorna uma rota'''

    def get_locales_route(self, linestring) -> pd.DataFrame:
        '''Retorna os postos de combustíveis mais próximos com base na latitude e longitude fornecidas'''

class IInsertLocRepository(ABC):

    @abstractmethod    
    def insert_loc_unique(self, nome, tipo, data_cadastro, geom_point) -> pd.DataFrame:
        '''Insere uma localidade no banco de dados'''

class IUploadDfLocsRepository(ABC):

    @abstractmethod    
    def insert_loc_unique(self, nome, tipo, data_cadastro, geom_point) -> pd.DataFrame:
        '''Insere uma localidade no banco de dados'''