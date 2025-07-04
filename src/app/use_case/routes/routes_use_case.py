from typing import Dict
import logging
import pandas as pd
import json
import sys
from shapely.geometry import shape
from shapely.wkt import dumps as to_wkt



from src.adapters.repositories_interface.routes.routes_repository_interface import IRoutesRepository


class RoutesUserCase:
    def __init__(self, route: IRoutesRepository):
        self.route = route
        
    def execute(self, latitude_inicio, longitude_inicio, latitude_fim, longitude_fim)-> Dict[str, Dict]:
        '''Retorna uma rota em geojson para o Usuario'''
        try:
            
            result_df = self.route.get_route(self._check_numeric(latitude_inicio), 
                                             self._check_numeric(longitude_inicio), 
                                             self._check_numeric(latitude_fim), 
                                             self._check_numeric(longitude_fim))
            geojson_str = result_df['geometry_geojson'].dropna().iloc[0]
            if result_df.empty:
                return {"STATUS": False, "DADOS": None}
            geojson_obj = json.loads(geojson_str)
            df_locales = self._consultar_locales_proximos(geojson_obj)

            df_postos = df_locales[df_locales['tipo'] == 'posto_combustivel']
            df_prf = df_locales[df_locales['tipo'] == 'posto_prf']

            json_postos = self._transformar_df_geojson(df_postos)
            json_prf = self._transformar_df_geojson(df_prf)

            json_response = {"STATUS": True, "DADOS": {"rota_geojson": geojson_obj, "postos_combustivel": json_postos, "postos_prf": json_prf }}

            return json_response
        
        except Exception as e:
            logging.error('Erro ao fazer rotas')
            print(str(e))
            return {"STATUS": False, "DADOS": [], "ERRO": str(e)}
        
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

    def _consultar_locales_proximos(self, geojson) -> pd.DataFrame:
        """
        Obtém os locais mais próximos com base na rota (geojson) fornecidos.
        """
        try:
            rota_geom = shape(geojson)
            wkt_line = to_wkt(rota_geom)
            df_result = self.route.get_locales_route(linestring=wkt_line)
            df_locales = pd.DataFrame(df_result, columns=['id', 'nome', 'tipo', 'geojson'])
            return df_locales
        except Exception as e:
            logging.error('Erro ao obter postos de combustíveis')
            print(str(e))
            return pd.DataFrame({"STATUS": False, "DADOS": [], "ERRO": str(e)})
        
    def _transformar_df_geojson(self, df: pd.DataFrame) -> Dict[str, Dict]:
        """
        Transforma um DataFrame em um dicionário.
        """
        # Converte a coluna 'geojson' de string para dicionário
        df['geojson'] = df['geojson'].apply(json.loads)

        # Converte o DataFrame para JSON
        json_result = df.to_dict(orient='records')

        return json_result