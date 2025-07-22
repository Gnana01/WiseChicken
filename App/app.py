import os
from dotenv import load_dotenv
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import streamlit as st
from wxai_langchain.llm import LangChainInterface
credentials = {
    'apikey': os.getenv("IBM_API_KEY"),
    'url':'https://us-south.ml.cloud.ibm.com'
}

llm = LangChainInterface(credentials=credentials,
                         model='meta-llama/llama-2-70b-chat',
                         params=
                         {
                             'decoding_method':'sample',
                             'max_new_tokens':200,
                             'temperature':0.5
                         },
                         project_id='420fc03c-be27-445f-b625-23f6f409076d'
                         )

st.title("The WiseChicken")

if 'message' not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    st.chat_message(message["role"].markdown(message["content"]))

prompt = st.chat_input("Enter you query here")


if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({'role':"user","content":prompt})
    response = llm(prompt)
#load_dotenv()
#PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
#TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
#
#pc = Pinecone(api_key=PINECONE_API_KEY)
#index_name = "coursera-courses"
#index = pc.Index(index_name)
#
#client = Together(api_key=TOGETHER_API_KEY)
#
#embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
#
#def retrieve_context_from_pinecone(query, top_k=5):
    #query_embedding = embedding_model.encode(query).tolist()
    #response = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
#
    #context_chunks = []
    #for match in response.matches:
        #metadata = match.metadata
        #context_chunks.append(
            #f"Title: {metadata.get('title')}\n"
            #f"Description: {metadata.get('description')}\n"
            #f"URL: {metadata.get('url')}\n"
        #)
    #context_text = "\n\n".join(context_chunks)
    #return context_text
#
#def generate_recommendation(query, context):
    #system_prompt = "You are a helpful assistant that recommends online courses based on user needs using provided context."
#
    #full_prompt = (
        #f"{system_prompt}\n\n"
        #f"Context:\n{context}\n\n"
        #f"User Query:\n{query}\n\n"
        #"Recommend 3 best-matching courses with reasoning in a user-friendly tone."
    #)
#
    #response = client.chat.completions.create(
        #model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        #messages=[
            #{"role": "system", "content": system_prompt},
            #{"role": "user", "content": full_prompt}
        #]
    #)
    #return response.choices[0].message.content
#
#if __name__ == "__main__":
    #user_query = input("Enter your course preference query: ")
#
    #context = retrieve_context_from_pinecone(user_query, top_k=5)
#
    #recommendation = generate_recommendation(user_query, context)
#
    #print("\n🎓 Recommended Courses:\n")
    #print(recommendation)