import os

from dotenv import load_dotenv
from deep_translator import GoogleTranslator
import pandas as pd
import streamlit as st

from langchain_groq.chat_models import ChatGroq
from pandasai import Agent

# Cargar variables de entorno
load_dotenv(override=True)



llm = ChatGroq(
    model_name="llama-3.1-70b-versatile", 
    api_key = os.environ["GROQ_API_KEY"])

st.title('Bot el Consultor 🕵️')


uploaded_file = st.file_uploader("Carga tu archivo excel", type=['xlsx'])


if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)
    st.write(data.head(5))

    agent = Agent([data], config={"llm": llm}, memory_size=10)


    prompt = st.text_area('Escribe tu pregunta: ')
    query = GoogleTranslator(source='spanish', target="english").translate(text=prompt)

    if st.button('Generar'):

        if prompt:
            with st.spinner("Generando respuesta..."):
                st.markdown("Respuesta: ")
                st.write(agent.chat(query))

                # Get Clarification Questions
                questions = agent.clarification_questions(query)

                st.markdown('<h2 style="color:green;">¿Quieres saber cómo llegue a la respuesta? <br> Este fue mi planteamiento: </h2>', unsafe_allow_html=True)
                for question in questions:
                    
                    st.write(GoogleTranslator(source='english', target="spanish").translate(text=question))

                # Explain how the chat response is generated
                response = agent.explain()
                st.write(GoogleTranslator(source='english', target="spanish").translate(text=response))