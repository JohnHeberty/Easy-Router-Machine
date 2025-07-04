from typing import Dict
import logging
import pandas as pd
import json
import sys
from shapely.geometry import shape
from shapely.wkt import dumps as to_wkt



from src.adapters.repositories_interface.routes.routes_repository_interface import IInsertLocRepository


class InsertLocUserCase:
    def __init__(self, route: IInsertLocRepository):
        self.route = route
        
    def execute(self, nome, tipo, latitude, longitude)-> Dict[str, Dict]:
        '''Retorna uma rota em geojson para o Usuario'''
        try:
            self._check_numeric(latitude), 
            self._check_numeric(longitude)

            lat = float(latitude)
            lon = float(longitude)
            wkt_point = f"POINT({lon} {lat})"

            data_cadastro = pd.Timestamp.now().strftime('%Y%m%d')
            flag = self.route.insert_loc_unique(nome=nome, tipo=tipo, data_cadastro=data_cadastro,geom_point=wkt_point)

            if flag:
                return {"STATUS": True, "INFO": ["Local inserido com sucesso!"]}
            else:
                return {"STATUS": False, "INFO": ["Ocorreu algum erro inesperado!"]}
        
        except Exception as e:
            logging.error('Erro ao fazer rotas')
            print(str(e))
            return {"STATUS": False, "INFO": [], "ERRO": str(e)}
        
    def _check_numeric(self, numero_text: str):
        """
        Verifica se o texto fornecido é um número. Se for, retorna o valor convertido para string.
        """
        if numero_text is not None:
            try:
                float(numero_text)
                return str(numero_text)
            except ValueError:
                raise ValueError("Coloque uma latitude/longitude verdadeira!")
        raise ValueError("Coloque uma latitude/longitude verdadeira!")

