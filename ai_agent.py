#Step1-- set api key setup
import os
from dotenv import load_dotenv

# Load the variables from the .env file
load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
TAVILY_API_KEY=os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

#step2--setup llm and tools
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages.ai import AIMessage

openai_llm=ChatOpenAI(model="gpt-4o-mini")
groq_llm=ChatGroq(model="llama-3.3-70b-versatile")

search_tool=TavilySearchResults(max_results=2)

#step3-setup AI agent with search tool functionality
from langgraph.prebuilt import create_react_agent

system_prompt="Act as an AI chatbot who is smart and friendly"

def get_response_from_ai_agent(llm_id,query,allow_search,system_prompt,provider):
    if provider=="Groq":
        llm=ChatGroq(model=llm_id)
    elif provider=="OpenAI":
        llm=ChatOpenAI(model=llm_id)
    
    tools=[TavilySearchResults(max_results=2)] if allow_search else []
    agent=create_react_agent(
        model=groq_llm,
        tools=tools,#[search_tool],
        state_modifier=system_prompt
        )

    #query="Tell me about trend in crypto market"
    state={"messages":query}
    response=agent.invoke(state)
    #for only last final result rather than getting all logical thinking
    messages=response.get("messages")
    ai_messagess=[message.content for message in messages if isinstance(message,AIMessage)]
    return ai_messagess[-1]
