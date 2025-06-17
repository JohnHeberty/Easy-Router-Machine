from typing import Dict
import logging
import pandas as pd
import json

from src.adapters.repositories_interface.routes.routes_repository_interface import IRoutesRepository


class RoutesUserCase:
    def __init__(self, route: IRoutesRepository):
        self.route = route
        
    def execute(self, latitude_inicio, longitude_inicio, latitude_fim, longitude_fim)-> Dict[str, Dict]:
        '''Retorna uma rota em geojson para o Usuario'''
        try:

            result_df = self.route.get_route(latitude_inicio, longitude_inicio, latitude_fim, longitude_fim)
            print(result_df)
            geojson_str = result_df['geometry_geojson'].dropna().iloc[0]
            if result_df.empty:
                return {"STATUS": False, "DADOS": None}
            geojson_obj = json.loads(geojson_str)
            json_response = {"STATUS": True, "DADOS": geojson_obj}
            return json_response
        
        except Exception as e:
            logging.error('Erro ao fazer rotas')
            print(str(e))
            return {"STATUS": False, "DADOS": None}
        