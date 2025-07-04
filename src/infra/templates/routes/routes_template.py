


router_time = '''
-- https://www.gaia-gis.it/fossil/libspatialite/wiki?name=VirtualRouting
WITH vars AS (
    SELECT 
        {} AS lat_o, 	-- latitude de origem
        {} AS long_o, 	-- longitude de origem

        {} AS lat_d,  	-- latitude de destino
        {} AS long_d,   -- longitude de destino

        0.1 AS Box_LatLong      -- Usado para realizar filtro, se diminir aumenta velocidade mas pode não localizar ponto
),
origem AS (
    SELECT node_id as Node_From
    FROM (
        SELECT node_id, 
               ST_Distance(ST_Point(long_o, lat_o), geometry) AS dist
        FROM roads_nodes, vars
        WHERE
                X(geometry) >= long_o   - Box_LatLong AND X(geometry) <= long_o + Box_LatLong
            AND Y(geometry) >= lat_o    - Box_LatLong AND Y(geometry) <= lat_o  + Box_LatLong
        ORDER BY dist ASC
        LIMIT 1
    )
),
destino AS (
    SELECT node_id as Node_To
    FROM (
        SELECT node_id, 
               ST_Distance(ST_Point(long_d, lat_d), geometry) AS dist
        FROM roads_nodes, vars
        WHERE
                X(geometry) >= long_d   - Box_LatLong AND X(geometry) <= long_d + Box_LatLong
            AND Y(geometry) >= lat_d    - Box_LatLong AND Y(geometry) <= lat_d  + Box_LatLong
        ORDER BY dist ASC
        LIMIT 1
    )
)
SELECT *, AsGeoJSON(nc.Geometry) AS geometry_geojson
FROM router_time nc, origem o, destino d
WHERE
	NodeFrom = o.Node_From AND NodeTo = d.Node_To

'''

postos_na_rota = '''
    SELECT 
        p.id, 
        p.nome,
        p.tipo,
        AsGeoJSON(p.geom) as geojson
    FROM 
        infraestrutura_rodoviaria p
    WHERE 
        ST_Within(
            p.geom,
            ST_Buffer(ST_GeomFromText('{}', 4326), 0.0018) -- buffer ~200m em graus (aprox)
        );
'''


postos_na_rota_backup = '''
    SELECT 
        p.id, 
        p.nome, 
        p.tipo
        AsGeoJSON(p.geom) as geojson
    FROM 
        infraestrutura_rodoviaria p
    WHERE 
        ST_Within( -- funcao de comparação de geometrias
            ST_Transform(p.geom, 3857),  -- primeira geometria
            ST_Buffer(ST_Transform(ST_GeomFromText('{}', 4326), 3857 ), 200 ) -- segunda geometria(buffer)
    );
'''

insert_loc_unique_query = '''
    INSERT INTO infraestrutura_rodoviaria (nome, tipo, data_cadastro, geom)
    VALUES ('{0}', '{1}', '{2}', ST_GeomFromText('{3}', 4326));
'''