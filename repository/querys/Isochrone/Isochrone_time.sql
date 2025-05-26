WITH vars AS (
    SELECT 
        -16.796131 AS lat_o, 	-- latitude de origem
        -49.279878 AS long_o, 	-- longitude de origem

        2.0 AS Box_LatLong      -- Usado para realizar filtro, se diminir aumenta velocidade mas pode não localizar ponto
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
)

-- Agora você deve fazer a junção adequada entre as tabelas
SELECT ST_ConcaveHull(ST_Collect(Geometry)) as Buffer
FROM NetworkTime nc, origem o
WHERE
	NodeFrom = o.Node_From AND Cost <= 1000