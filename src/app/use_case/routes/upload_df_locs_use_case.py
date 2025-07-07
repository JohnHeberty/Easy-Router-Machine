from typing import Dict
import logging
import pandas as pd
import json
import sys
from shapely.geometry import shape
from shapely.wkt import dumps as to_wkt
import io


from src.adapters.repositories_interface.routes.routes_repository_interface import IUploadDfLocsRepository


class UploadDfLocsUserCase:
    def __init__(self, route: IUploadDfLocsRepository):
        self.route = route
        
    def execute(self, nome_local, nome_coluna_tipo, nome_coluna_latitude, nome_coluna_longitude, csv_content, separador_csv)-> Dict[str, Dict]:
        '''Inserir localidades a partir de um arquivo CSV'''
        try:

            data_cadastro = pd.Timestamp.now().strftime('%Y%m%d')
            if separador_csv is None or separador_csv == '':
                separador_csv = ','

            df = pd.read_csv(io.StringIO(csv_content.decode("utf-8")), sep=separador_csv)

            df[nome_coluna_latitude] = df[nome_coluna_latitude].astype(str).str.replace(',', '.')
            df[nome_coluna_longitude] = df[nome_coluna_longitude].astype(str).str.replace(',', '.')
            df[nome_coluna_latitude] = df[nome_coluna_latitude].str.strip()
            df[nome_coluna_longitude] = df[nome_coluna_longitude].str.strip()

            df = df.fillna(value="")

            mask_valid = (
                df[nome_coluna_latitude].apply(self._check_numeric) &
                df[nome_coluna_longitude].apply(self._check_numeric) &
                df[nome_coluna_tipo].apply(self._check_string) &
                df[nome_local].apply(self._check_string)
            )

            if not mask_valid.all():
                linhas_invalidas = df[~mask_valid].to_dict(orient="records")
                return {
                    "STATUS": False,
                    "INFO": ["Existem valores inválidos de latitude ou longitude no arquivo CSV."],
                    "ERRO": "Valores inválidos de latitude ou longitude detectados.",
                    "LINHAS_INVALIDAS": linhas_invalidas
                }
            
            df = df[mask_valid]


            for _, row in df.iterrows():
                tipo = str(row[nome_coluna_tipo]).strip() 
                nome = str(row[nome_local]).strip()

                if nome is None or nome == '' or tipo is None or tipo == '':
                    print("erro na linha, nome ou tipo vazio")
                    continue
                
                lat = row[nome_coluna_latitude]
                lon = row[nome_coluna_longitude]

                wkt_point = f"POINT({lon} {lat})"

                flag = self.route.insert_loc_unique(nome=nome, tipo=tipo, data_cadastro=data_cadastro,geom_point=wkt_point)

                if not flag:
                    return {"STATUS": False, "INFO": ["Ocorreu algum erro inesperado!"]}
                
            return {"STATUS": True, "INFO": ["Dados inseridos com sucesso!"]}
        
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
                float(numero_text.strip())
                return True
            except ValueError as e:
                print(f"Erro ao converter número: {str(e)}")
                return False
            except Exception as e:
                print(f"Erro ao verificar número: {str(e)}")
                return False

    def _check_string(self, numero_text: str):
        """
        Verifica se o texto fornecido é um número. Se for, retorna o valor convertido para string.
        """
        try:
            if numero_text is not None or numero_text != '':
                return True
            
        except Exception as e:
            print(f"Erro ao verificar a string: {str(e)}")
            return False