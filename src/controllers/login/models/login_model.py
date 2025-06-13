from pydantic import BaseModel #type: ignore

class UserLoginInfo(BaseModel):
    matricula   : str
    senha       : str
    filial      : str 
    
class UserRegisterInfo(BaseModel):
    matricula       : str
    senha           : str
    filial          : str
    data            : str