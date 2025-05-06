FIST RUN
	osmconvert64-large.exe brazil-latest.osm.pbf --all-to-nodes --complete-multipolygons --out-statistics --complete-ways --drop-author --drop-version --verbose -o=brazil-latest.osm_fix.pbf
	ERROR

SECOND RUN - 1642 Mb
	osmconvert64-large.exe brazil-latest.osm.pbf --complete-ways --drop-author --drop-version --verbose -o=brazil-latest.osm_fix.pbf
	
THIRT RUN - 1330 Mb
	osmconvert64-large.exe brazil-latest.osm.pbf --all-to-nodes --drop-author --drop-version --verbose --complete-ways --complete-multipolygons --max-objects=500000000 --hash-memory=2048 -o=brazil-latest.osm_fix.pbf
	
FOUR RUN
	osmconvert64-large.exe brazil-latest.osm.pbf --drop-author --drop-version --verbose --complete-ways --complete-multipolygons --max-objects=500000000 --hash-memory=2048 -o=brazil-latest.osm_fix.pbf

	
	

	