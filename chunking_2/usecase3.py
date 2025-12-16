import asyncio
from neo4j_graphrag.experimental.components.entity_relation_extractor import LLMEntityRelationExtractor
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.experimental.components.types import TextChunks,TextChunk
from neo4j_graphrag.generation.prompts import ERExtractionTemplate
from neo4j import GraphDatabase
from neo4j_graphrag.experimental.components.kg_writer import Neo4jWriter


prompt=ERExtractionTemplate(
    template="""
You are an expert in extracting entities and relationships from cricket-related text.

## Text to analyze:
{text}

## Instructions:
Extract all entities and their relationships. Focus on:
- Players (use label "Person")
- Teams (use label "Team") 
- Countries (use label "Country")
- Tournaments/Leagues (use label "Tournament")

## Required JSON Output Format:
Return a JSON object with this EXACT structure:

{{
  "nodes": [
    {{
      "id": "0",
      "label": "Person",
      "properties": {{"name": "Player Name"}}
    }},
    {{
      "id": "1", 
      "label": "Team",
      "properties": {{"name": "Team Name"}}
    }}
  ],
  "relationships": [
    {{
      "type": "PLAYS_FOR",
      "start_node_id": "0",
      "end_node_id": "1"
    }}
  ]
}}

CRITICAL RULES:
1. Each node MUST have: "id" (unique string), "label", and "properties"
2. Each relationship MUST have: "type", "start_node_id", "end_node_id"
3. Use "start_node_id" and "end_node_id" (NOT "from" and "to")
4. Node IDs must be simple strings like "0", "1", "2", etc.
5. Relationship types should be in UPPER_SNAKE_CASE (e.g., PLAYS_FOR, REPRESENTS)

Return ONLY valid JSON, no markdown code blocks or explanations.
""",
expected_inputs=["text"]
)

# NEO4J_URI=neo4j+s://1dc52763.databases.neo4j.io
# NEO4J_USERNAME=neo4j
# NEO4J_PASSWORD=4phiiAm3WYrPzIb7ptt9WuafQbWk-Ncr88PeqXKHRMI
# NEO4J_DATABASE=neo4j
# AURA_INSTANCEID=1dc52763
# AURA_INSTANCENAME=Free instance
async def extract_entity():
    driver=GraphDatabase.driver(
      "neo4j+s://1dc52763.databases.neo4j.io",
      auth=("neo4j","4phiiAm3WYrPzIb7ptt9WuafQbWk-Ncr88PeqXKHRMI")
   )

    #create entity relationship extractor
    extractor=LLMEntityRelationExtractor(
        llm=OpenAILLM(model_name="gpt-4o",api_key=os.getenv("OPENAI_API_KEY"),model_params={"max_tokens":5000,"response_format":{"type":"json_object"}}),
        prompt_template=prompt
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
    writer=Neo4jWriter(driver=driver)
    await writer.run(graph)
    

if __name__ == "__main__":
    asyncio.run(extract_entity())