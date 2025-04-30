import logging
import os

class LoggerFactory:
    """
    Responsabilidade: Criar loggers configurados para armazenar logs em arquivos separados para cada nível
    (DEBUG, INFO, WARNING, ERROR, CRITICAL) e exibir no console.
    Segue princípios do SOLID, em especial o princípio da responsabilidade única.
    """
    def __init__(self, logs_dir: str = os.path.join("data", "logs"), default_level: int = logging.DEBUG):
        self.logs_dir = logs_dir
        os.makedirs(self.logs_dir, exist_ok=True)
        self.default_level = default_level

    def _create_file_handler_for_level(self, log_filepath: str, level: int) -> logging.Handler:
        file_handler = logging.FileHandler(log_filepath, encoding="utf-8")
        file_handler.setLevel(level)
        # Filtra para registrar apenas mensagens deste nível exato.
        file_handler.addFilter(lambda record: record.levelno == level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        return file_handler

    def _create_console_handler(self) -> logging.Handler:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.default_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        return console_handler

    def get_logger(self, class_name: str) -> logging.Logger:
        """
        Retorna um logger configurado para a classe especificada.
        São adicionados handlers de arquivo separados para cada nível de log e um handler para console.
        Se o logger já tiver handlers configurados, eles serão limpos para evitar duplicação.
        """
        logger = logging.getLogger(class_name)
        logger.setLevel(self.default_level)

        if logger.hasHandlers():
            logger.handlers.clear()

        # Adiciona handlers para cada nível
        levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
        for level in levels:
            level_name = logging.getLevelName(level)
            log_filepath = os.path.join(self.logs_dir, f"log_{class_name}_{level_name}.log")
            logger.addHandler(self._create_file_handler_for_level(log_filepath, level))
            
        # Adiciona handler para o console
        logger.addHandler(self._create_console_handler())
        return logger

# # Exemplo de uso:
# if __name__ == "__main__":
#     logger_factory = LoggerFactory()
#     logger = logger_factory.get_logger("MinhaClasseExemplo")
#     logger.debug("Mensagem de debug")
#     logger.info("Mensagem de informação")
#     logger.warning("Mensagem de aviso")
#     logger.error("Mensagem de erro")
#     logger.critical("Mensagem crítica")