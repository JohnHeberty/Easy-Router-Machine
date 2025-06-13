from abc import abstractmethod, ABC
from typing import Optional
import psycopg2 # type: ignore

class IDBConnectionHandler(ABC):
    def get_conn() ->Optional[psycopg2.extensions.connection]:
        '''Retorna conexão com o banco'''