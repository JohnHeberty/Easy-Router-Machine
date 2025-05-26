-- Criando índices para otimizar consultas espaciais na roads_nodes
CREATE INDEX idx_roads_nodes_node_id ON roads_nodes(node_id);
CREATE INDEX idx_roads_nodes_geometry ON roads_nodes(geometry);

-- Criando índices para otimizar consultas espaciais nas roads
CREATE INDEX idx_roads_geometry ON roads(geometry);
CREATE INDEX idx_roads_node_from ON roads(node_from);
CREATE INDEX idx_roads_node_to ON roads(node_to);