#step1-setup ui with streamlit 
import streamlit as st
st.set_page_config(page_title="Langgraph Agent AI",layout="centered")
st.title("AI chatbot agent")
st.write("Create and interact with AI agents!")

system_prompt=st.text_area("Define your AI agent:", height=70,placeholder="type your system prompt here...")
MODEL_NAME_GROQ=["llama-3.3-70b-versatile","mistral-8x7b-32768"]
MODEL_NAME_OPENAI=["gpt-4o-mini"]

provider=st.radio("select Provider:", {"Groq","OpenAI"})

if provider=="Groq":
    selected_model=st.selectbox("Select Groq Model:", MODEL_NAME_GROQ)
elif provider=="OpenAI":
    selected_model=st.selectbox("Select Groq Model:", MODEL_NAME_OPENAI)

allow_web_search=st.checkbox("Allow Web Search")

user_query=st.text_area("Enter your Query:", height=150,placeholder="Ask Anything")

API_URL="http://127.0.0.1:9999/chat"

if st.button("Ask Agent!"):
    if user_query.strip():
        #step2-connect with bakend via url
        import requests
        payload={
            "model_name": selected_model,
            "model_provider": provider,
            "system_promt":system_prompt,
            "messages":[user_query],
            "allow_search":allow_web_search
            }
        
        response=requests.post(API_URL,json=payload)

        if response.status_code==200:
            response_data=response.json()
        #get response from bacekend nd show here
            if "error" in response_data:
                st.error(response_data["error"])
            else:
                st.subheader("Agent Response")
                st.markdown(f"**Final response:** {response_data}")


# for checking UI run -- C:\Users\parma\AppData\Roaming\Python\Python313\Scripts\streamlit run frontend.py

