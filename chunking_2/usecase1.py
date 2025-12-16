import asyncio
import os
from neo4j_graphrag.experimental.components.entity_relation_extractor import LLMEntityRelationExtractor
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.experimental.components.types import TextChunks,TextChunk

async def extract_entity():
    #create entity relationship extractor
    extractor=LLMEntityRelationExtractor(
        llm=OpenAILLM(model_name="gpt-4o",api_key=os.getenv("OPENAI_API_KEY"),model_params={"max_tokens":5000,"response_format":{"type":"json_object"}})
    )
    chunks=TextChunks(chunks=[
        TextChunk(
            text="Virat Kohli is an Indian cricketer,who plays for team RCB in IPL",
            index=0
        )
    ]

    )
    graph=await extractor.run(chunks=chunks)
    print("Extracxted graph:")
    print("\n Extracted Node:")
    for node in graph.nodes:
        print(f"    -{node.label}:  {node.properties}")
    print("\nExtracted Relationships:")
    for rel in graph.relationships:
        print(f"    -{rel.type}:    {rel.start_node_id} -> {rel.end_node_id}")

if __name__ == "__main__":
    asyncio.run(extract_entity())