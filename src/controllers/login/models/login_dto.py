from pydantic import BaseModel

class UserLoginDTO(BaseModel):
    matricula   : str
    senha       : str
    filial      : str 
    versionApp  : str 
    dispositivo : str 
    
class UserRgisterDTO(BaseModel):
    matricula       : str
    senha           : str
    filial          : str
    data            : str