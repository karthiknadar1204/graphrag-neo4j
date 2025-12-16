from neo4j_graphrag.experimental.pipeline import Pipeline,Component,DataModel
from neo4j_graphrag.experimental.components.types import Neo4jGraph,TextChunks
from neo4j_graphrag.experimental.components.text_splitters.fixed_size_splitter import FixedSizeSplitter
from neo4j_graphrag.experimental.components.entity_relation_extractor import LLMEntityRelationExtractor
import asyncio
import json
import os
from neo4j_graphrag.llm import OpenAILLM
from neo4j import GraphDatabase
from neo4j_graphrag.experimental.components.kg_writer import Neo4jWriter

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, "input.txt")

with open(input_file, "r") as f1:
    text = f1.read()

pipeline=Pipeline()

class splitCompOutput(DataModel):
        value: TextChunks

class entExtCompOutput(DataModel):
    value: Neo4jGraph

class comp3output(DataModel):
    value: str

class comp1(Component):
    async def run(self) -> splitCompOutput:
        fs=FixedSizeSplitter(chunk_size=8000,chunk_overlap=100)
        st= await fs.run(text=text)
        #print(st)
        return splitCompOutput(value=st)
    
class comp2(Component):
    async def run(self,chunks:TextChunks) -> entExtCompOutput:
        extractor=LLMEntityRelationExtractor(llm=OpenAILLM(model_name="gpt-4o",api_key="",model_params={"max_tokens":8000,"response_format":{"type":"json_object"}}))
        graph=await extractor.run(chunks=chunks)
        return entExtCompOutput(value=graph)
    
class comp3(Component):
    async def run(self,graph:Neo4jGraph) -> entExtCompOutput:
        driver=GraphDatabase.driver(uri="neo4j+s://1dc52763.databases.neo4j.io",auth=("neo4j","4phiiAm3WYrPzIb7ptt9WuafQbWk-Ncr88PeqXKHRMI"))
        writer=Neo4jWriter(driver=driver)
        await writer.run(graph)
        graph_data={
            "nodes":[
                {
                    "id":node["id"],
                    "label":node["label"],
                    "properties":node["properties"]

                }
                for node in graph["nodes"]
            ],
            "relationships":[
                {
                    "type":rel["type"],
                    "start_node_id":rel["start_node_id"],
                    "end_node_id":rel["end_node_id"],
                    "properties":rel["properties"]

                }
                for rel in graph["relationships"]
            ]
        }
        graph_file = os.path.join(script_dir, "graph.json")
        with open(graph_file, "w") as f:
            json.dump(graph_data, f, indent=2)

        print("graph added successfully")
        return entExtCompOutput(value=graph)
        
    


    
async def runPipeline():
    pipeline.add_component(comp1(),"comp1")
    pipeline.add_component(comp2(),"comp2")
    pipeline.add_component(comp3(),"comp3")
    pipeline.connect("comp1","comp2",{"chunks":"comp1.value"})
    pipeline.connect("comp2","comp3",{"graph":"comp2.value"})
    result=await pipeline.run(data={})
    return result.result

if __name__=="__main__":
    graph=asyncio.run(runPipeline())
    print(graph)