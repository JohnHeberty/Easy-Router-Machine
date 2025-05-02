from ..singleton import Singleton  # noqa: F401
from loguru import logger
from typing import Type
import os

# LoggerFactory utilizando o Singleton via metaclass
class LoggerFactory(metaclass=Singleton):
    """
    Fábrica de loggers que utiliza o padrão Singleton.
    Garante que uma única instância seja criada.
    Evitando loggers duplicados e mantendo a configuração consistente.
    """
    def __init__(self, logs_dir: str = os.path.join("data", "logs"), default_level: str = "DEBUG") -> None:
        self.logs_dir: str = logs_dir
        os.makedirs(self.logs_dir, exist_ok=True)
        self.default_level: str = default_level
        self.loggers: dict[str, Type[logger]] = {}

    def _configure_file_sink(self, class_name: str, level: str) -> None:
        """
        Configura o sink de arquivo para registrar mensagens de log em arquivos separados por nível.
        Adiciona um sink para cada nível de log filtrando somente mensagens do logger referente.
        """
        log_filepath: str = os.path.join(self.logs_dir, f"log_{class_name}_{level.lower()}.log")
        # Remove o sink padrão do loguru para evitar duplicação de mensagens
        logger.remove()
        # Configura o sink do console para exibir mensagens de log
        logger.add(
            log_filepath,
            level=level,
            format="{time:YYYY-MM-DD HH:mm:ss} - {extra[logger_name]} - {level} - {message}",
            rotation="10 MB",
            encoding="utf-8",
            filter=lambda record, lvl=level: record["extra"].get("logger_name") == class_name and record["level"].name == lvl
        )

    def _configure_console_sink(self, class_name: str) -> None:
        """
        Configura o sink do console para exibir mensagens de log.
        Adiciona um sink que imprime mensagens no console com filtro para este logger.
        """
        # Remove o sink padrão do loguru para evitar duplicação de mensagens
        logger.remove()
        # Configura o sink do console para exibir mensagens de log
        logger.add(
            lambda msg: print(msg, end=""),
            level=self.default_level,
            format="{time:YYYY-MM-DD HH:mm:ss} - {extra[logger_name]} - {level} - {message}",
            filter=lambda record: record["extra"].get("logger_name") == class_name
        )

    def get_logger(self, class_name: str) -> Type[logger]:
        """
        Retorna o logger configurado de forma única para a classe especificada.
        Se já existir, retorna o mesmo logger previamente configurado.
        """
        if class_name in self.loggers: 
            return self.loggers[class_name]

        # Configura sinks para cada nível
        levels: list[str] = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        for level in levels:
            self._configure_file_sink(class_name, level)

        # Configura sink para o console
        self._configure_console_sink(class_name)
        
        # Cria o logger e o vincula ao nome da classe
        bound_logger = logger.bind(logger_name=class_name)
        self.loggers[class_name] = bound_logger
        return bound_logger

# Exemplo de uso
# if __name__ == "__main__":
#     logger_factory = LoggerFactory()
#     logger1 = logger_factory.get_logger("MinhaClasseExemplo")
#     logger2 = logger_factory.get_logger("OutraClasseExemplo")
#
#     logger1.debug("Mensagem de debug de MinhaClasseExemplo")
#     logger1.info("Mensagem de informação de MinhaClasseExemplo")
#     logger2.warning("Mensagem de aviso de OutraClasseExemplo")
#     logger2.error("Mensagem de erro de OutraClasseExemplo")
