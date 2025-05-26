from modules.osmtools.spatialite import SpatialiteOsmNet, SpatialiteNetwork
from modules.osmtools.osm_convert import OSMConvert
from modules.osmtools.osm_filter import OSMfilter
from modules.geofabrik import ProtobufDownloader

import os

if __name__ == "__main__":

    # BAIXANDO OS DADOS DO GEOFABRICK
    PBD = ProtobufDownloader()
    PBD.run()

    # TRANSFORMANDO PBF PARA O5M PARA REALIZAR FILTROS E DIMINUIR TAMANHO DO PROTOBUF
    OSMC = OSMConvert(
        type_osm_in='pbf',
        type_osm_out='o5m',
    )
    OSMC.input_file             = 'brazil-latest.osm.pbf'
    OSMC.drop_author            = True
    OSMC.drop_version           = True
    OSMC.verbose                = True
    OSMC.complete_ways          = True
    OSMC.complete_multipolygons = True
    OSMC.max_objects            = 500000000
    OSMC.hash_memory            = 4096
    OSMC.run()

    # REALIZANDO FILTRAGEM DE DADOS NO PROTOBUF
    OSMF = OSMfilter(verbose=True)
    OSMF.input_file = 'brazil-latest.osm.o5m'
    OSMF.run()

    # CONVERTENDO O5M FITLRADO PARA PROTOBUF
    OSMC = OSMConvert(
        base_path_in = os.path.join("data","processed"),
        base_path_out = os.path.join("data","processed"),
        type_osm_in='o5m',
        type_osm_out='pbf',
    )
    OSMC.input_file             = 'brazil-latest.osm.filtered.streets.o5m'
    OSMC.drop_author            = False
    OSMC.drop_version           = False
    OSMC.verbose                = False
    OSMC.complete_ways          = False
    OSMC.complete_multipolygons = False
    OSMC.max_objects            = 500000000
    OSMC.hash_memory            = 4096
    OSMC.run()

    # CRIANDO O BANCO COM RODOVIAS E SEUS LINKS COM O PROTOBUF FILTRADO
    SP_OSM_NET = SpatialiteOsmNet()
    os.makedirs(os.path.join("data","processed","streets"), exist_ok=True)
    path_db = os.path.join("data","processed","streets","streets.sqlite")
    args = [
        "-o",
        os.path.join("data","processed","pbf","brazil-latest.osm.filtered.streets.pbf"),
        "-T",
        "roads",
        "-d",
        path_db,
    ]
    SP_OSM_NET.run(args=args)

    # CRIANDO A TABELA DE ROTEIRIZAÇÃO POR TEMPO
    SP_NET = SpatialiteNetwork()
    args = [
        "-d",
        path_db,
        "-T",
        "roads",
        "-f",
        "node_from",
        "-t",
        "node_to",
        "-g",
        "geometry",
        "-c",
        "cost",
        "--a-star-supported",
        "-n",
        "name",
        "-o",
        "table_router_time",
        "-vt",
        "router_time",
        "--overwrite-output"
    ]
    SP_NET.run(args=args)
