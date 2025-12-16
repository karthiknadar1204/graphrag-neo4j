#!/usr/bin/env python3
import asyncio
from neo4j_graphrag.experimental.components.schema import SchemaFromTextExtractor
from neo4j_graphrag.llm import OpenAILLM

async def extract_schema():
    #instantiate the auto schema extractor component
    schema_extractor=SchemaFromTextExtractor(
        llm=OpenAILLM(
            model_name="gpt-4o",
            api_key=os.getenv("OPENAI_API_KEY"),
            model_params={
                "max_tokens":5000,
                "response_format":{"type":"json_object"},
            }
        ),

    )
    extracted_schema=await schema_extractor.run(text="Virat Kohli is an Indian cricketer, who playes for team RCB in IPL")
    return extracted_schema

if __name__ == "__main__":
    result=asyncio.run(extract_schema())
    print(result)