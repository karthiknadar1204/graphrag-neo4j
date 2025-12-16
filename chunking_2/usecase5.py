import asyncio
from neo4j_graphrag.experimental.components.entity_relation_extractor import LLMEntityRelationExtractor
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.experimental.components.types import TextChunks,TextChunk
from neo4j import GraphDatabase
from neo4j_graphrag.experimental.components.kg_writer import Neo4jWriter
from neo4j_graphrag.experimental.components.schema import SchemaFromTextExtractor

async def extract_schema_and_entity():
    driver=GraphDatabase.driver(
      "neo4j+s://1dc52763.databases.neo4j.io",
      auth=("neo4j","4phiiAm3WYrPzIb7ptt9WuafQbWk-Ncr88PeqXKHRMI")
   )
    schema_extractor=SchemaFromTextExtractor(
        llm=OpenAILLM(model_name="gpt-4o",api_key="",model_params={
            "max_tokens":5000,
            "response_format":{"type":"json_object"},
        }
        ),

    )
    extracted_schema=await schema_extractor.run(text="Virat Kohli is an Indian cricketer, who playes for team RCB in IPL")

    #create entity relationship extractor
    extractor=LLMEntityRelationExtractor(
        llm=OpenAILLM(model_name="gpt-4o",api_key="",model_params={"max_tokens":5000,"response_format":{"type":"json_object"}}),
    )
    chunks=TextChunks(chunks=[
        TextChunk(
            text="Virat Kohli is an Indian cricketer,who plays for team RCB in IPL",
            index=0
        )
    ]

    )
   
    graph=await extractor.run(chunks=chunks,schema=extracted_schema)
    print("Extracxted graph:")
    print("\n Extracted Node:")
    for node in graph.nodes:
        print(f"    -{node.label}:  {node.properties}")
    print("\nExtracted Relationships:")
    for rel in graph.relationships:
        print(f"    -{rel.type}:    {rel.start_node_id} -> {rel.end_node_id}")
    writer=Neo4jWriter(driver=driver)
    await writer.run(graph)
    

if __name__ == "__main__":
    asyncio.run(extract_schema_and_entity())