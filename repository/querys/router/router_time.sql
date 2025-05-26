-- https://www.gaia-gis.it/fossil/libspatialite/wiki?name=VirtualRouting
WITH vars AS (
    SELECT 
        -16.7802859 AS lat_o, 	-- latitude de origem
        -49.2717158 AS long_o, 	-- longitude de origem

        -16.803097 AS lat_d,  	-- latitude de destino
        -49.205362 AS long_d,   -- longitude de destino

        0.5 AS Box_LatLong      -- Usado para realizar filtro, se diminir aumenta velocidade mas pode não localizar ponto
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

-- Agora você deve fazer a junção adequada entre as tabelas
SELECT *
FROM router_time nc, origem o, destino d
WHERE
	NodeFrom = o.Node_From AND NodeTo = d.Node_To