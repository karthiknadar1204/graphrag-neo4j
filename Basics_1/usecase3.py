import asyncio
from neo4j_graphrag.experimental.components.schema import SchemaFromTextExtractor
from neo4j_graphrag.llm import OpenAILLM

async def extract_schema():
    #instantiate the auto schema extractor component
    schema_extractor=SchemaFromTextExtractor(
        llm=OpenAILLM(model_name="gpt-4o",api_key="",model_params={
            "max_tokens":5000,
            "response_format":{"type":"json_object"},
        }
        ),
        prompt_template="""You are a Knowledge Graph Architect.

Convert the input text into a MULTI-LEVEL, DOMAIN-AGNOSTIC Neo4j graph schema.

INSTRUCTIONS:
1. Extract ALL explicit and implicit entities.
2. Enforce hierarchy and semantic depth (no flat graphs).
3. Separate:
   - Entities / Actors / Objects
   - Roles / Types
   - Categories / Classes
   - Domains / Concepts
   - Attributes / States / Qualities
4. Normalize concepts (do NOT mix entity, role, and attribute).
5. Infer hidden semantic structure where logically possible.
6. Ensure minimum depth = 3 levels where applicable.
7. Design for scalability and reasoning.
8. Use Neo4j-friendly labels and UPPER_SNAKE_CASE relationship names.
9. Each node_type.properties entry MUST be an object with:
   - name (string)
   - type (string)
   - description (string)
10. Output must be VALID JSON.
11. Output ONLY JSON. No explanation, no markdown, no extra text.

use the below only to generate schema :
"node_types" only will be from the below types , dont use anything else;
1.king
2.food
3.car
4.country

if nothing meaningfull can be extracted from the given input as per the node_types make it empty



property_type must be any of this 'BOOLEAN', 'DATE', 'DURATION', 'FLOAT', 'INTEGER', 'LIST', 'LOCAL_DATETIME', 'LOCAL_TIME', 'POINT', 'STRING', 'ZONED_DATETIME' or 'ZONED_TIME' 

REQUIRED OUTPUT FORMAT:

"{{
  "node_types": [
    {{
      "label": "<NodeLabel>",
      "description": "<Description>",
      "properties": [
        {{
          "name": "<property_name>",
          "type": "<string|number|boolean|datetime|list|map>",
          "description": "<Property description>"
        }}
      ],
    }}
  ],
  "relationship_types": [
    {{
      "label": "<RELATIONSHIP_NAME>",
      "description": "<Description>"
    }}
  ],
  "patterns": [
    ["<SourceNode>", "<RELATIONSHIP>", "<TargetNode>"]
  ]
}}"

INPUT TEXT:
"{text}"
"""
     ,

    )
    extracted_schema=await schema_extractor.run(text="Alexander was king of Greece,he loves to eat pasta and used to drive bmwi7m70")
    return extracted_schema

if __name__ == "__main__":
    result=asyncio.run(extract_schema())
    print(result)