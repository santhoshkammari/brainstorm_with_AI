from fastapi import FastAPI, Query
from researcher_ai.main.query_processor import MultiAgentQueryOrchestrator

app = FastAPI()

@app.get("/process_query/")
def process_query(
    query: str = Query(..., description="The query to process"),
    num_queries: int = Query(3, description="Number of queries to process"),
    response_level: str = Query("low", description="low,medium,high")
):
    processor = MultiAgentQueryOrchestrator(
        response_level=response_level
    )
    result = processor.process_query(query,num_queries=num_queries)
    return {"result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8900)