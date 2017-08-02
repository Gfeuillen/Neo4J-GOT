docker run \
    --publish=7474:7474 --publish=7687:7687 \
    --volume=/home/gfeuillen/my_projects/GOT/neo4j/data:/var/lib/neo4j/data \
    --volume=/home/gfeuillen/my_projects/GOT/neo4j/conf:/var/lib/neo4j/conf \
    --volume=/home/gfeuillen/my_projects/GOT/neo4j/import:/var/lib/neo4j/import \
    neo4j