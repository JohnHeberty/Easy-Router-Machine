# router-disbral
Esse projeto trata-se de um service de destinado a roterização de rotas


## Instalação (Windows/linux)

Siga os passos abaixo para instalar e executar o projeto em um ambiente Python(windows ou linux ):

1. **Clone o repositório**
    ```bash
    git clone https://github.com/CCA-2024/router-service.git
    ```

2. **Crie um ambiente virtual (opcional, mas recomendado)**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    ```

3. **Instale as dependências**
    ```bash
    pip install -r requirements.txt
    ```

5. **Configure o arquivo .env**
    5.1 Dado o arquivo de exemplo: " server.env.sample ", faça as configurações necessárias
    5.2 Renomeie o arquivo para " .env "

6. **Execute o serviço**
    ```bash
    python fastapi dev main_api.py --port 8003
    ```
7. **Acesso a documentação do service**
Para acessar a documentação interativa da API, utilize o Swagger UI disponível em:

```
http://<ip-maquina>:<porta-escolhida>/v0/docs
```
Exemplo com a porta 8003 e ip: localhost : http://localhost:8003/router-service/v0/docs 

Abra esse endereço no seu navegador após iniciar o serviço.
Obs: 
-Certifique-se de ter o Python 3.8 ou superior instalado.
-Quando se estiver usando prefixo nas variáveis de ambiente, certifique-se está escrevendo de maneira correta após o ip "/v0/docs"

## Instalação (Docker)

Siga os passos abaixo para executar o projeto utilizando Docker:

1. **Clone o repositório**
    ```bash
    git clone https://github.com/CCA-2024/router-service.git
    cd geo-service
    ```

2. **Configure o arquivo .env**
    2.1 Dado o arquivo de exemplo: " docker.env.sample ", faça as configurações necessárias
    2.2 Renomeie o arquivo para " .env "

3. **Execute o docker compose**
    ```bash
    docker compose up -d --build .
    ```
4. **Acesso a documentação do service**
Para acessar a documentação interativa da API, utilize o Swagger UI disponível em:

```
http://<ip-maquina>:<porta-escolhida>/v0/docs
```
Exemplo com a porta 8003 e ip: localhost : http://localhost:8003/router-service/v0/docs 

Abra esse endereço no seu navegador após iniciar o serviço.
Obs: 
-Quando se estiver usando prefixo nas variáveis de ambiente, certifique-se está escrevendo de maneira correta após o ip "/v0/docs"
Obs: Certifique-se de ter o Docker instalado em sua máquina.

