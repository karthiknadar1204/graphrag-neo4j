from neo4j_graphrag.experimental.components.schema import GraphSchema
from neo4j_graphrag.experimental.utils.schema import schema_visualization

restore_schema=GraphSchema.from_file("my_schema.json")
vg=schema_visualization(restore_schema)
html=vg.render()
with open("my_schema.html","w") as f:
    f.write(html.data)