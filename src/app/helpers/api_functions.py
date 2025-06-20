from src.infra.config.api_config import api_config


def get_prefix_version()-> str:
    """
    Retorna o prefixo para os endpoints baseado na versão. Ex: '/v1'.
    """
    version = api_config["version_api"]
    flag_prefix = api_config["prefix_api"]

    if not version:
        raise ValueError("Insira a versão da API!")
    
    if flag_prefix in ("True", "true", True):
        prefix = version.split('.')[0]
        return f"/router/{prefix}"
    else:
        return ''
    
def get_version()-> str:
    """
    Retorna a versão da api EX: 'v1-4-0''.
    """
    return api_config["version_api"]