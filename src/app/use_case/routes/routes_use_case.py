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
            result_df = self.route.get_route(self.check_numeric(latitude_inicio), 
                                             self.check_numeric(longitude_inicio), 
                                             self.check_numeric(latitude_fim), 
                                             self.check_numeric(longitude_fim))
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
            return {"STATUS": False, "DADOS": [], "ERRO": str(e)}
        
    def check_numeric(self, numero_text: str):
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
