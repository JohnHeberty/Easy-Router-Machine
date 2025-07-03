


table_infraestrutura_rodoviaria = """
    SELECT InitSpatialMetadata();

    -- Criação da tabela infraestrutura_rodoviaria no banco de dados de locais
    CREATE TABLE infraestrutura_rodoviaria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT,
                nome TEXT,
                data_cadastro TEXT
                 
    );
    SELECT AddGeometryColumn('infraestrutura_rodoviaria', 'geom', 4326, 'POINT', 'XY');


"""