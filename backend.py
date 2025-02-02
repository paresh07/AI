from pydantic import BaseModel
from typing import List

#setup pydantic model and schema validation
class ReuestState(BaseModel):
    model_name: str
    model_provider: str
    system_promt:str
    messages:List[str]
    allow_search:bool

#step2: setup aii agent from frontend
from fastapi import FastAPI
from ai_agent import get_response_from_ai_agent
#import requests
allowed_model_names=["llama3-70b-8192","gpt-4o-mini","llama-3.3-70b-versatile","mistral-8x7b-32768"]
app=FastAPI(title="Langgraph AI Agent")

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.post("/chat")
def chat_endpoint(request:ReuestState):
    """api endpoint  to dynamic select multiple model"""
    if request.model_name not in allowed_model_names:
        return {"error": "invalid model name. Kindly select valid Model Name"}
    llm_id=request.model_name
    query=request.messages
    allow_search=request.allow_search
    system_promt=request.system_promt
    provider=request.model_provider

    #create A! agent and get response
    response=get_response_from_ai_agent(llm_id,query,allow_search,system_promt,provider)
    return response
    #step3: run app & explore swagger ui after 9999/docs to open swager
if __name__=="__main__":
    import subprocess
    import threading

    def run_fastapi():
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=9999)

    def run_streamlit():
        command = ['C:\\Users\\parma\\AppData\\Roaming\\Python\\Python313\\Scripts\\streamlit', 'run', 'frontend.py']
        result = subprocess.run(command, capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)

    # Start FastAPI in a separate thread
    fastapi_thread = threading.Thread(target=run_fastapi)
    fastapi_thread.start()

    # Start Streamlit
    run_streamlit()



