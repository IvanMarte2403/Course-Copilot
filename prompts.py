import streamlit as st
import subprocess






# Título de la aplicación
st.title("Entrada de datos para el curso")

# Crear inputs de texto para cada variable y guardar los valores ingresados por el usuario
course_name = st.text_input("Nombre del curso", "Sistemas de recomendación con Machine Learning")

target_audience = st.text_area("Audiencia objetivo", "Personas con conocimiento en programación con Python que buscan profundizar su conocimiento en machine learning y crear un sistema de recomendación para su empresa, tienen un trabajo en una empresa top de México, cuentan con 4 horas a la semana para estudiar de lunes a viernes")

specific_topics = st.text_input("Temas específicos", "Ejemplos y casos de uso de sistemas de recomendación")

course_level = st.selectbox(
    "Nivel del curso",
    ("Básico", "Intermedio", "Avanzado", "Experto")
)

course_focus = st.text_input("Enfoque del curso", "técnico")

next_learning_unit = st.text_input("Siguiente unidad de aprendizaje", "IA Generativa")

if st.button('Guardar'):
    st.write("Nombre del curso:", course_name)
    st.write("Audiencia objetivo:", target_audience)
    st.write("Temas específicos:", specific_topics)
    st.write("Nivel del curso:", course_level)
    st.write("Enfoque del curso:", course_focus)
    st.write("Siguiente unidad de aprendizaje:", next_learning_unit)
    st.write("The copilot start .... 🤖")
    subprocess.run(["python", "course_copilot.py"])
    st.write("The next link have your new lesson 🚀")
    st.write("https://docs.google.com/spreadsheets/d/1EmJObSLuOedjwUAFJHG3_LWHyVrILSjQB_sqtSd86lM/edit?usp=sharing")
