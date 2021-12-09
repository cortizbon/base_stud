import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import psycopg2 as ps
import numpy as np

#hacer la conexión con la base de datos

passw = st.text_input('Ingrese la contraseña')
if passw != st.secrets['PASSWORD']:
    st.stop()

host_name = st.secrets['HOST_NAME'] 
username = st.secrets['DB_USER'] 
password = st.secrets['DB_PASSWORD'] 

conn = ps.connect(host=host_name, 
            user=username, 
            password=password)

df = pd.read_sql('SELECT * FROM registros2', conn)

st.sidebar.title('Facultad de Economía | Desempeño 2020-2021')
st.sidebar.write('Este es un instrumento desarrollado por el Laboratorio de Econometría para el seguimiento del desempeño académico en la Facultad de Economía.')
st.sidebar.header('Filtros')

#crear los filtros

#filtro_periodo

lista_periodos = df['periodo'].unique().tolist()
#lista_periodos.insert(0, 'Todos')
filtro1 = st.sidebar.multiselect('Seleccione un periodo: ',lista_periodos, default=20201)

#filtro1 = st.sidebar.selectbox('Seleccione un periodo: ', lista_periodos)

if filtro1 != 'Todos':
    query = f'periodo == {filtro1[0]}'
    for k in filtro1[1:]:
        query += f' or periodo == {k}'
    df = df.query(query)
#filtro_depto

lista_deptos = df['depto'].unique().tolist()
lista_deptos.insert(0, 'Todos')
filtro2 = st.sidebar.selectbox('Seleccione un departamento: ', lista_deptos)

if filtro2 != 'Todos':
    df = df[df['depto']==filtro2]

#filtro_materia
lista_materias = df['nom_materia'].unique().tolist()
lista_materias.insert(0, 'Todos')
filtro3 = st.sidebar.selectbox('Seleccione un espacio académico: ', lista_materias)

if filtro3 != 'Todos':
    df = df[df['nom_materia']==filtro3]

#filtro_docente
lista_docentes = df['docente'].unique().tolist()
lista_docentes.insert(0, 'Todos')
filtro4 = st.sidebar.selectbox('Seleccione un docente: ', lista_docentes)

if filtro4 != 'Todos':
    df = df[df['docente']==filtro4]

#filtro_estudiante
lista_estudiantes = df['apellidos_y_nombres'].unique().tolist()
lista_estudiantes.insert(0, 'Todos')
filtro5 = st.sidebar.selectbox('Seleccione un estudiante: ', lista_estudiantes)

if filtro5 != 'Todos':
    df = df[df['apellidos_y_nombres']==filtro5]

st.title('Facultad de Economía | Desempeño académico 2020 - 2021' )



# crear las visualizaciones 
# histograma

st.subheader('Visualización general')
fig,ax = plt.subplots(1,3, figsize=(12,4))

ax[0].set_xlim(-0.1,5.1)
ax[1].set_ylim(-0.1,5.1)
ax[2].set_ylim(-0.1,5.1)

sns.histplot(data=df,x='definitiva', ax=ax[0])


pru = (pd.DataFrame(df[['nota_1','nota_2','nota_3','definitiva']].stack())
       .droplevel(0)
       .reset_index()
       .replace({'nota_1':'1er','nota_2':'2do','nota_3':'3er','definitiva':'Definitiva'})
      .rename(columns={'index':'Corte',0:'Nota'}))

pru1 = pru.query('Corte != "Definitiva"')
pru2 = pru.query('Corte == "Definitiva"')

sns.stripplot(data=pru1, x='Corte', y='Nota', jitter=0.05, ax=ax[1], palette='Blues', linewidth=1)

sns.stripplot(data=pru2, x='Corte', y='Nota', jitter=0.05, ax=ax[2], palette='Blues', linewidth=1)
st.pyplot(fig)

st.subheader('Descriptivo general')
col1, col2, col3, col4 = st.columns(4)

col1.write(df['nota_1'].describe())
col2.write(df['nota_2'].describe())
col3.write(df['nota_3'].describe())
col4.write(df['definitiva'].describe())

st.subheader('Visualización discriminada por periodo')

fig, ax = plt.subplots(1,3, figsize=(12,4))

ax[0].set_xlim(-0.1,5.1)
ax[1].set_ylim(-0.1,5.1)
ax[2].set_ylim(-0.1,5.1)

sns.histplot(data=df,x='definitiva', ax=ax[0], hue='periodo', palette='Blues')

lista_df = []
for i in ['nota_1','nota_2','nota_3','definitiva']:
  prueba = df[[i, 'periodo']]
  prueba['Corte'] = i
  prueba = prueba.rename(columns={i:'Valor'}).replace({'nota_1':'1er','nota_2':'2do','nota_3':'3er','definitiva':'Definitiva'})
  lista_df.append(prueba)

prueba_df = pd.concat(lista_df)
prueba_1 = prueba_df.query('Corte != "Definitiva"')
prueba_2 = prueba_df.query('Corte == "Definitiva"')
sns.stripplot(data=prueba_1, x='Corte',y='Valor',hue='periodo',palette='Blues',linewidth=0.4,ax=ax[1])

sns.stripplot(data=prueba_2, x='Corte',y='Valor',hue='periodo',palette='Blues',linewidth=0.4,ax=ax[2])
st.pyplot(fig)
# descriptivos


# tasa de no aprobacion