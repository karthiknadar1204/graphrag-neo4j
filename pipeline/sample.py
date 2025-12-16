from neo4j_graphrag.experimental.pipeline import Pipeline,Component,DataModel
import asyncio

pipeline=Pipeline()

class comp1output(DataModel):
    value: str

class comp2output(DataModel):
    value: str

class comp1(Component):
    async def run(self) -> comp1output:
        return comp1output(value="output from comp1")
    
class comp2(Component):
    async def run(self,input) -> comp2output:
        return comp2output(value=f"{input}+ output from comp2")
    
async def runPipeline():
    pipeline.add_component(comp1(),"comp1")
    pipeline.add_component(comp2(),"comp2")
    pipeline.connect("comp1","comp2",{"input":"comp1.value"})
    result=await pipeline.run(data={})
    return result.result

if __name__=="__main__":
    print(asyncio.run(runPipeline())["comp2"]["value"])