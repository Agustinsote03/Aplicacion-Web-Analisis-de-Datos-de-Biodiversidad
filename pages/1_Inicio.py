import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "src"))

st.title("BioAR")

st.header("Propósito de la aplicación")
st.write("""
## Bienvenido/a

En esta aplicación vas a poder explorar y analizar datos de biodiversidad de una forma organizada y sencilla. 
La idea es que puedas trabajar con información biológica real o simulada, utilizando el estándar **Darwin Core**, 
que nos ayuda a ordenar y compartir estos datos de manera uniforme.

Hoy en día, entender la biodiversidad es clave para conocer cómo funcionan los ecosistemas, cómo cambian con el tiempo 
y qué impacto tienen las actividades humanas sobre ellos. Por eso, contar con herramientas que faciliten su análisis 
es muy importante tanto para la investigación como para la conservación del ambiente.

A lo largo de la aplicación vas a encontrar distintas secciones pensadas para ayudarte a explorar estos datos paso a paso.
""")

st.header("Importancia del análisis de biodiversidad")
st.write("""
El análisis de datos de biodiversidad es una herramienta esencial en la investigación ambiental y ecológica. 
Permite comprender cómo interactúan las especies entre sí y con su entorno, así como detectar alteraciones 
en los ecosistemas causadas por factores naturales o por actividades humanas.

Además, facilita la identificación de especies en riesgo, el seguimiento de la pérdida de hábitats y el 
monitoreo de cambios ambientales a largo plazo. Esta información es clave para diseñar estrategias de 
conservación efectivas y políticas de gestión ambiental basadas en evidencia científica.

En un contexto global de cambio climático y pérdida de biodiversidad, el análisis sistemático de estos 
datos se vuelve cada vez más relevante para la preservación de los ecosistemas y el equilibrio ambiental.
""")

st.header("Estandar Darwin Core")
st.subheader("¿Qué es?")
st.write("""
El estándar Darwin Core (DwC) es un conjunto de términos y definiciones diseñado para 
facilitar el intercambio de información sobre biodiversidad.

Su propósito principal es estandarizar la forma en que se describen los registros biológicos,
como la observación de una especie en un lugar y fecha determinados. Esto permite que datos
provenientes de distintas instituciones puedan integrarse, compararse y analizarse de manera consistente.
""")

st.subheader("¿Para qué se utiliza?")
st.write("""
Se utiliza para facilitar el uso práctico de los datos de biodiversidad a nivel global.

Permite:
- Integrar información proveniente de distintas fuentes
- Comparar registros de manera consistente
- Analizar la distribución de especies
- Apoyar investigaciones científicas y decisiones de conservación

De esta manera, los datos pueden ser reutilizados y aprovechados por diferentes organizaciones
sin necesidad de redefinir su estructura.
""")

st.header("Instrucciones básicas de uso")
st.write(""" 
Para utilizar la aplicación:

En la barra lateral (sidebar) podés navegar entre las distintas páginas:
- **Inicio**: información general de la aplicación.
- **Estado del sistema**: muestra el historial de operaciones realizadas.
- **Búsqueda**: buscá registros por texto libre o filtros avanzados.
- **Visualización**: gráficos de distribución, tendencias temporales y comparativas.
- **Gestión de registros**: insertá, actualizá o eliminá registros de los datasets.
- **Datasets**: información técnica y calidad de datos de cada dataset.

A medida que avances en la aplicación, podrás consultar información sobre especies, 
ubicaciones y registros biológicos.
""")


