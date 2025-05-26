# Easy-Router-Machine

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Easy-Router-Machine é um projeto para automatizar a criação, atualização e destruição de bancos de dados de roteirização baseados em dados OpenStreetMap (OSM), utilizando ferramentas como Spatialite, osmconvert, osmfilter e integração com o download automatizado de dados do Geofabrik.

## Visão Geral

O objetivo do projeto é permitir que você crie rapidamente um ambiente de roteirização (por exemplo, para rotas de estradas) a partir de dados OSM atualizados, com um pipeline automatizado para:
- Baixar os dados mais recentes do OSM (via Geofabrik)
- Converter, filtrar e preparar os dados
- Criar o banco de dados de roteirização
- Destruir/remover bancos antigos para atualização

## Estrutura do Projeto

```
├── data/
│   ├── external/      # Dados brutos baixados (ex: .osm.pbf)
│   ├── processed/     # Dados processados e bancos gerados
│   └── ...
├── modules/
│   ├── osmtools/      # Integração com binários e ferramentas OSM/Spatialite
│   └── geofabrik/     # Download e manipulação de dados do Geofabrik
├── pipelines/
│   ├── make_router/   # Pipeline para criar o roteirizador
│   └── unmake_router/ # Pipeline para destruir o roteirizador
└── ...
```

## Como funciona o pipeline de roteirização

### 1. Criação do roteirizador (`pipelines/make_router/make_router.py`)

Este pipeline executa as seguintes etapas:
- **Download**: Baixa o arquivo OSM PBF mais recente do Geofabrik.
- **Conversão**: Usa `osmconvert` para transformar o arquivo PBF em O5M (formato mais leve para filtragem).
- **Filtragem**: Usa `osmfilter` para extrair apenas as vias de interesse (ex: rodovias).
- **Nova conversão**: Converte o arquivo filtrado de volta para PBF.
- **Criação do banco**: Usa `spatialite_osm_net` e `spatialite_network` para criar o banco de dados `streets.sqlite` e a tabela de roteirização.

### 2. Destruição do roteirizador (`pipelines/unmake_router/unmake_router.py`)

Este pipeline remove todos os dados e bancos processados, permitindo uma atualização limpa:
- Remove pastas e arquivos em `data/external` e `data/processed`.

### 3. Atualização do roteirizador

Para atualizar o roteirizador com dados mais recentes:
1. Execute o pipeline de destruição (`unmake_router.py`) para limpar dados antigos.
2. Execute o pipeline de criação (`make_router.py`) para baixar e processar os dados novos.

## Como executar

No terminal, execute:

```pwsh
# Para destruir o roteirizador antigo
python pipelines/unmake_router/unmake_router.py

# Para criar o roteirizador atualizado
python pipelines/make_router/make_router.py
```

## Requisitos
- Python 3.10+
- Dependências em `requirements.txt`
- Binários do Spatialite, osmconvert, osmfilter disponíveis em `modules/osmtools/bin/`

## Observações
- O projeto é modular e pode ser adaptado para outros países ou regiões alterando o parâmetro de download do Geofabrik.
- O pipeline é facilmente customizável para diferentes tipos de filtragem ou atributos de roteirização.

## Licença
MIT

---
Desenvolvido por John Heberty / Disbral / CCA

