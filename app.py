import openai
import gspread
import re
from config import api_key
from oauth2client.service_account import ServiceAccountCredentials
import json
import streamlit as st


# Initial Configuration
openai.api_key = api_key      
# # #API Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('course-copilot-425602-78432e6747e5.json', scope)

#streamlit secret credentials



# openai.api_key = st.secrets["gpt_key"]['api_key']

# json_creds_str = st.secrets["google_creds"]["json"]
# json_creds = json.loads(json_creds_str)
# print("JSON string from secrets:", json_creds_str)
# json_creds = json.loads(json_creds_str)J
# creds = ServiceAccountCredentials.from_json_keyfile_dict(json_creds, scope)

client = gspread.authorize(creds)
spreadsheet = client.open('Pipeline para creación de cursos')

sheet1 = spreadsheet.sheet1
sheet2 = spreadsheet.get_worksheet(1) 
sheet3 = spreadsheet.get_worksheet(2) 
sheet4 = spreadsheet.get_worksheet(3) 
sheet5 = spreadsheet.get_worksheet(4) 


course_name = " "
target_audience = " "
specific_topics = " "
course_level = " "
course_focus = " "
next_learning_unit = " "



def main():

    def generate_chatgpt(prompt, model="gpt-4o",temperature =0.7):
        response = openai.chat.completions.create(
          model= model,
          messages=[{"role": "system", "content": "Start"}, {"role": "user", "content": prompt}],
          temperature = temperature
      )
        return response.choices[0].message.content


    def generate_course_entry_profile(course_name, target_audience, specific_topics, course_level,course_focus):
   
        # Definir el prompt para la generación de texto
        prompt = (
            f"Como experto diseñador de programas académicos especializado en tecnología, "
            f"tu tarea es mejorar el perfil de ingreso para el curso de {course_name} "
            f"tomando como base a estudiantes {target_audience} definido para este curso. "
            f"Este curso tiene un nivel {course_level}. El perfil de ingreso ideal para este curso es..., no se deben usar caracteres especiales o formatos específicos para el texto."
            f" ten en cuenta {course_focus} y los {specific_topics}"
        )

        return generate_chatgpt(prompt)

    def search_and_analyze_courses(course_name, course_level,profile):
        print(f"Realizando investigación de cursos similares a {course_name} de nivel {course_level}...")

        prompt = f"Como experto diseñador de programas ac adémicos especializado en tecnología, tu tarea es desarrollar un nuevo curso titulado {course_name} dirigido a {profile}. Para garantizar que el curso sea competitivo y cumpla con las expectativas del público objetivo, realiza una investigación comparativa de tres cursos relacionados disponibles en plataformas de educación en línea, tomando en cuenta el {course_level} Formato:   'Nombre: [nombre], Año: [año], Objetivos: [objetivo1, objetivo2, objetivo3]', Descripcion Breve: [descripcion-breve], Temario Detallado [temario-detallado]  , Retorna [número] Nombre: [nombre], Año: [año], Objetivos: [objetivo1, objetivo2, objetivo3].  Descripcion Breve: [descripcion-breve], Temario Detallado [temario-detallado] , no se deben usar caracteres especiales o formatos específicos para el texto. solo es permitido []"
        response = generate_chatgpt(prompt)
        courses =response
    
        sections = re.split(r'\n\d',courses)
        if sections[0]  == ' ':
                sections = sections[1:]

        return sections


    def generate_course_objectives(course_name, course_level, course_focus, profile, specific_topics,course):
        prompt = (
            f"Basándote en las áreas de oportunidad identificadas y en los {specific_topics} si es que existen, y los cursos {course} "
            f"para el curso de {course_name} con un nivel {course_level} y un enfoque {course_focus}, "
            f"orientado a {profile} procede a definir un objetivo claro y conciso del curso. "
            f"Estos objetivos deben estructurarse de manera que reflejen las metas educativas del programa y cómo se alinean con las necesidades del {profile}. "
            f"El nombre del objetivo tiene que captar la esencia del curso, y la descripción del objetivo describe en habilidades. No se deben usar caracteres especiales o formatos específicos para el texto. Solo está permitido []."
            f"\n\nNombre[nombre del Objetivo], Descripción[descripcion del objetivo]\n"
        )
        return generate_chatgpt(prompt)


    def generate_course_secondary_objectives(course_name, course_level, course_focus, profile, specific_topics, principal_objective,course):
        prompt = (
            f"Basándote en las áreas de oportunidad identificadas y en los {specific_topics} si es que existen, y en los cursos {course}"
            f"para el curso de {course_name} con un nivel {course_level} y un enfoque {course_focus}, y en el objetivo principal {principal_objective} "
            f"orientado a {profile} procede a definir 5 objetivos claros y concisos del curso. "
            f"Estos objetivos deben estructurarse de manera que reflejen las metas educativas del programa y cómo se alinean con las necesidades del {profile}. "
            f"El nombre del objetivo tiene que captar la esencia del curso, y la descripción del objetivo describe en habilidades. No se deben usar caracteres especiales o formatos específicos para el texto. Solo está permitido []. Es obligatorio que el numero retorne con el formato Numero[numero del objetivo]"
            f"\n\nNumero[numero del objetivo],Nombre[nombre del Objetivo], Descripción[descripcion del objetivo]\n"
        )
        return generate_chatgpt(prompt)


    #Graduate Profile
    def generate_graduate_profile(course_name, target_audience, specific_topics, next_learning_unit, principal_objetive, secondary_objetives):

        prompt = (
            f"Basándote en la descripción del curso que es {course_name}y los objetivos  que son {principal_objetive} y {secondary_objetives} tanto generales como específicos definidos previamente y en los {specific_topics}, "
            f"procede a crear un perfil de egreso para los estudiantes que completen el curso de {course_name}, "
            f"enfocado especialmente en aquellos {target_audience}. "
            f"Considera que idealmente el siguiente paso en su camino de aprendizaje es tener las bases para continuar su aprendizaje en {next_learning_unit}, "
            f"sin embargo no lo menciones explícitamente. "
            f"- Redacta un párrafo que sea claro, conciso e impactante, reflejando el valor que los estudiantes aportarán a sus empresas o su crecimiento profesional tras completar el curso. "
            f"Este debe resumir las capacidades, la mentalidad y la preparación con la que contarán los egresados, destacando su preparación para enfrentar los desafíos tecnológicos actuales."
            )
        return generate_chatgpt(prompt)
    
        # ==========================[Generating Key Skills]=================================
    # Key Skills 

    def generate_key_skills(course_name, target_audience, graduate_profile):
    
        prompt = (
            f"En todas las habilidades basate tambien en {graduate_profile}. Para cada una de las 5 habilidades principales del curso {course_name}, enfocado en {target_audience}, "
            f"genera un detalle que incluya:\n"
            f"→ Nombre de la Habilidad: Breve y directo.\n"
            f"→ Dos Key Points: En forma de bullet points, destaca dos aspectos cruciales que evidencian por qué cada habilidad es esencial y cómo contribuye al perfil profesional del egresado en el entorno laboral dinámico de hoy.\n\n"
            f"Retorna el siguiente formato obligatorio  para cada habilidad:, no excluyas ningun []  No se deben usar caracteres especiales o formatos específicos para el texto. Solo está permitido []\n"
            f"Numero[numero de la habilidad], Nombre[nombre de la habilidad], Descripcion [key1, key2], "
        )
        
        return generate_chatgpt(prompt)

     # ==========================[Generating Course Syllabus]=================================

    def generate_course_syllabus(course_name, entry_profile, course_focus, main_objective, course):
   
        # Determining the number of classes and their distribution based on course focus
        if course_focus == "teórico":
            total_classes = 24
            weekly_distribution = "4 clases por semana de 1 hora cada clase, con 3 conceptos clave por clase."
        elif course_focus == "técnico":
            total_classes = 12
            weekly_distribution = "2 clases por semana de 2 horas cada clase, 1 hora teoría y 1 hora de contenido técnico con ejercicios prácticos."

        # Sylabus Prompt
        prompt = (
            f"Como diseñador de programas académicos especializado en tecnología y con experiencia en la creación de cursos de ciencia de datos y negocios para empresas internacionales, basate en los cursos {course} "
            f"tu misión es concretar un temario completo y detallado para el curso de {course_name}, orientado especialmente a {entry_profile} utilizando como base el perfil de egreso previamente generado, "
            f"el objetivo principal y objetivos secundarios, tu tarea consiste en diseñar un temario que cumpla con las especificaciones detalladas y las necesidades de la audiencia. Este temario debe estructurarse considerando los siguientes requisitos:\n"
            f"1. Duración Total del Curso: 6 semanas de enseñanza teórica y práctica, enfocando cada semana en el avance de un proyecto final.\n"
            f"2. Total de clases: {total_classes}, distribución semanal: {weekly_distribution}\n" 
            f"Al estructurar el temario, considera lo siguiente:\n"
            f"- La importancia de incorporar fundamentos teóricos sólidos junto con aplicaciones prácticas que reflejen situaciones reales del curso.\n"
            f"- La necesidad de adaptar los contenidos y metodologías de enseñanza para facilitar el aprendizaje del {entry_profile}, el {main_objective} y el enfoque {course_focus}.\n"
            f"- La creación de un ambiente de aprendizaje que promueva la interacción, la resolución de problemas, y el desarrollo de un proyecto final que consolide el aprendizaje de todo el curso y habilidades adquiridas durante el curso.\n"
            f"Nombre Semana: Tiene que ser un nombre de la semana, máximo 6 palabras,\n"
            f"Clase: Tiene que ser un titulo llamativo que refleje el contenido de la clase,\n"
            f"Conceptos: de clase: Los conceptos separados por comas de la clase,\n"
            f"Descripcion de la clase: Una breve descripcion que refleje los conceptos y el contenido de la clase y que outline saldrán los alumnos de esa clase,\n"
            f"Objetivos de la clase: 3 conceptos separados con comas de lo que se espera que los alumnos aprendan en la clase\n"
            f"Retorna el siguiente formato obligatorio para cada habilidad:, no excluyas ningun []  No se deben usar caracteres especiales o formatos específicos para el texto. Solo está permitido [] Semana[Nombre[Nombre de la semana], Clase1[[Conceptos de clase], Descripcion[Descripcion de la clase], Objetivos[Objetivos de la clase]],Clase2[[Conceptos de clase],Descripcion[Descripcion de la clase],Objetivos[Objetivos de la clase]]\n. empieza a contar la clase desde 1 por cada semana, respeta mucho el formato y el nivel de [] . "
            f"Ten en cuenta {total_classes} clases en total."
        )

        return generate_chatgpt(prompt)
    
    
    # ==========================[Income Profile]=================================
    st.title('Generating Income Profile .... 🤖')
    profile = generate_course_entry_profile(course_name, target_audience, specific_topics, course_level, course_focus)
     # Actualiza la hoja de Google Sheets
   
    st.write(profile)

    st.info('Writting in Google Sheets .... ✍️ ')
    sheet1.update_cell(2, 1, profile)
    st.success('Done! ✅')
    # ==========================[Generating Courses]=================================

    print('Generating Courses  .... 🤖')
    st.info('Generating Courses  .... 🤖')

    course = search_and_analyze_courses(course_name, course_level,profile)
    print ('Writting in Google Sheets .... ✍️ ')
    st.info('Writting in Google Sheets .... ✍️')

    for i, section in enumerate(course, start=0):
        sheet2.update_cell(i+2, 1, section)


    print ('Done! ✅')
    st.success('Done! ✅')


    # ==========================[Generating Principal Objectives]=================================

    print('Generating  Principal Objetive .... 🤖')
    st.info('Generating  Principal Objetive .... 🤖')

    principal_objetive = generate_course_objectives(course_name, course_level, course_focus, profile, specific_topics, course)

    print ('Writting in Google Sheets .... ✍️ ')
    st.info('Writting in Google Sheets .... ✍️')

    # Search Objetivo in the text
    match = re.search(r'Nombre\[(.*?)\]', principal_objetive)
    if match:
        name = match.group(1)
        sheet3.update_cell(2, 1, name)

    match = re.search(r'Descripción\[(.*?)\]', principal_objetive)
    if match:
        description = match.group(1)
        sheet3.update_cell(3, 1, description)

        print ('Done! ✅')
        st.success('Done! ✅')


    # ======================Generating Objetives=====================

    print('Generating  Objectives .... 🤖')
    st.info('Generating  Objectives .... 🤖')

    secondary_objetives = generate_course_secondary_objectives(course_name, course_level, course_focus, profile, specific_topics, principal_objetive,course)

    print('Escribiendo en Google Sheets .... ✍️')
    st.info('Escribiendo en Google Sheets .... ✍️')

    # Dividir el texto en líneas
    lines = secondary_objetives.strip().split('\n')

    # Verificar que las líneas se están dividiendo correctamente
    print(f"Total de líneas a procesar: {len(lines)}")

    # Iterar sobre las líneas
    for i, line in enumerate(lines, start=3):
        print(f"Procesando línea {i}")  # Impresión de depuración
        number_match = re.search(r'Numero\[(.*?)\]', line)
        name_match = re.search(r'Nombre\[(.*?)\]', line)
        description_match = re.search(r'Descripci[oó]n\[(.*?)\]', line)

        if number_match and name_match and description_match:
            print(f"Actualizando Google Sheets para la línea {i}")  # Más impresiones de depuración
            sheet3.update_cell(i, 3, name_match.group(1))
            sheet3.update_cell(i, 4, description_match.group(1))
        else:
            print(f"No se encontraron coincidencias en la línea {i}")  # Ayuda a identificar líneas problemáticas

    print ('Done! ✅')
    st.success('Done! ✅')

    # =========================Printing Graduate Profile=========================

    print('Generating Graduate Profile .... 🤖')
    st.info('Generating Graduate Profile .... 🤖')
    graduate_profile = generate_graduate_profile(course_name, target_audience, specific_topics, next_learning_unit, principal_objetive, secondary_objetives)


    print ('Writting in Google Sheets .... ✍️ ')
    st.info('Writting in Google Sheets .... ✍️')


    sheet4.update_cell(1, 2, graduate_profile)


    print('Done! ✅')
    st.success('Done! ✅')   

    # =========================Printing Key Skills=========================

    print('Generating Principal Habilities .... 🤖')
    st.info('Generating Principal Habilities .... 🤖')

    key_skills = generate_key_skills(course_name, target_audience, graduate_profile)

    print('Writting in Google Sheets .... ✍️')
    st.info('Writting in Google Sheets .... ✍️')


    # Extraer habilidades clave del texto
    patron_habilidad = r"Numero\[\d+\], Nombre\[(.*?)\], Descripcion \[(.*?)\]"
    habilidades = re.findall(patron_habilidad, key_skills)

    fila_inicio = 3  # La fila donde comenzaremos a escribir
    for nombre, descripcion in habilidades:
        # Actualiza las celdas en Google Sheets para el nombre y la descripción
        sheet4.update_cell(fila_inicio, 1, nombre)  # Escribe el nombre en la columna 1
        sheet4.update_cell(fila_inicio, 2, descripcion)  # Escribe la descripción en la columna 2
        fila_inicio += 1  # Incrementa la fila para la próxima habilidad

    st.success('Done! ✅')

    # =========================Printing Course Syllabus=========================

    print('Generating Course Syllabus .... 🤖')
    st.info('Generating Course Syllabus .... 🤖')

    syllabus = generate_course_syllabus(course_name, profile, course_focus, principal_objetive, course)

    print (syllabus)

    print ('Writting in Google Sheets .... ✍️ ')
    st.info('Writting in Google Sheets .... ✍️')

    # Dividir el texto del syllabus en semanas, comenzando desde el primer elemento no vacío
    semanas = re.split(r'Semana\[', syllabus)[1:]

    # Fila inicial para la primera semana
    fila_actual = 2

    # Preparar un batch de actualizaciones
    batch_updates = []

    for semana in semanas:
        # Obtener el nombre de la semana, asumiendo que la estructura siempre tiene 'Nombre[' antes de 'Clase1'
        match = re.search(r'Nombre\[(.*?)\],', semana)
        nombre_semana = match.group(1).strip() if match else 'Desconocido'

        # Agregar la fila de título de 'Semana' y el nombre de la semana al batch
        batch_updates.append({
            'range': f'A{fila_actual}:B{fila_actual}',
            'values': [['Semana', nombre_semana]]
        })

        # Incrementar fila_actual para colocar información de las clases
        fila_clase = fila_actual + 1

        # Extraer cada clase con su descripción y objetivos
        clases = re.findall(r'Clase\d+\[\[(.*?)\], Descripcion\[(.*?)\], Objetivos\[(.*?)\]\]', semana)
        clase_data = []
        for nombre_clase, descripcion, objetivos in clases:
            # Añadir la información de cada clase al arreglo de clase_data
            clase_data.append([nombre_clase.strip(), descripcion.strip(), objetivos.strip()])
            
            # Incrementar fila_clase para la siguiente clase
            fila_clase += 1

        # Añadir las clases al batch        
        batch_updates.append({
            'range': f'C{fila_actual + 1}:E{fila_clase - 1}',
            'values': clase_data    
        })

        # Actualizar fila_actual para la siguiente semana, asegurando un espacio de 5 filas entre semanas
        fila_actual = fila_clase + 10

    # Ejecutar todas las actualizaciones en un batch
    sheet5.batch_update(batch_updates)

    print ('Done! ✅')

    # ==========================[Aplicación]=================================

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

if st.button('Comenzar'):

    st.subheader("The copilot start .... 🤖")
    st.info("The next link have your new lesson 🚀")
    st.write("https://docs.google.com/spreadsheets/d/1EmJObSLuOedjwUAFJHG3_LWHyVrILSjQB_sqtSd86lM/edit?usp=sharing")

    main()
    st.success("The copilot finish .... 🤖")

 





