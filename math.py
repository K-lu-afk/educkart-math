import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# ---------------------------------------------------------
# 1. CONFIGURACIÓN Y ESTILOS CSS PERSONALIZADOS (EDUCK ART)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Plataforma de Acertijos - Colegio Educk Art",
    page_icon="📐",
    layout="centered"
)

# Estilos visuales: Verde (#009A44), Azul (#0099DA), Rosa (#E6007E), Blanco (#FFFFFF)
st.markdown("""
    <style>
    /* Fondo principal blanco */
    .stApp {
        background-color: #FFFFFF;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Encabezados */
    h1 {
        color: #E6007E !important;
        text-align: center;
        font-weight: 700;
    }
    
    h2, h3, .stSubheader {
        color: #0099DA !important;
    }
    
    /* Barra lateral */
    [data-testid="stSidebar"] {
        background-color: #009A44 !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    
    /* Corrección de cajas de entrada (Forzar texto claro y visible) */
    div[data-baseweb="input"] {
        background-color: #F0F2F6 !important;
        border-radius: 8px !important;
    }
    input {
        color: #000000 !important;
    }
    
    /* Botones */
    .stButton>button {
        background-color: #E6007E !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: bold !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        background-color: #0099DA !important;
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# Logo oficial (utilizando logo.png de tu repositorio o fallback)
LOGO_URL = "logo.png"

# ---------------------------------------------------------
# 2. BASE DE DATOS SQLITE
# ---------------------------------------------------------
def conectar_db():
    conn = sqlite3.connect("colegio_math.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS alumnos (
            matricula TEXT PRIMARY KEY,
            nombre TEXT,
            grupo TEXT,
            trimestre1_nivel INTEGER DEFAULT 1,
            trimestre2_nivel INTEGER DEFAULT 1,
            trimestre3_nivel INTEGER DEFAULT 1,
            ultimo_dia_jugado TEXT DEFAULT '',
            intentos_fallidos INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    return conn

conn = conectar_db()

# ---------------------------------------------------------
# 3. BANCO DE ACERTIJOS
# ---------------------------------------------------------
banco_por_grado = {
    "1º": {
        "Trimestre 1": {
            1: {"pregunta": "1º Sec: Resuelve la jerarquía de operaciones: 6 + 4 * (9 - 3) / 2", "correcta": "18", "pista": "Primero resuelve el paréntesis (9-3)=6, luego multiplica y divide."},
            2: {"pregunta": "1º Sec: ¿Cuál es el Mínimo Común Múltiplo (MCM) de 8 y 12?", "correcta": "24", "pista": "Busca el menor número divisible entre 8 y 12."},
            3: {"pregunta": "1º Sec: Calcula el área en cm² de un triángulo con base = 14 cm y altura = 6 cm.", "correcta": "42", "pista": "Fórmula: (Base * Altura) / 2."}
        },
        "Trimestre 2": {
            1: {"pregunta": "1º Sec: Resuelve la ecuación: 3x + 5 = 20. ¿Cuánto vale x?", "correcta": "5", "pista": "Resta 5 a 20 y luego divide entre 3."}
        },
        "Trimestre 3": {
            1: {"pregunta": "1º Sec: ¿Cuántos grados suman los ángulos internos de cualquier triángulo?", "correcta": "180", "pista": "Es una regla fundamental de la geometría."}
        }
    },
    "2º": {
        "Trimestre 1": {
            1: {"pregunta": "2º Sec: Si x⁴ * x³ = xⁿ, ¿cuál es el valor del exponente n?", "correcta": "7", "pista": "En la multiplicación de misma base, los exponentes se suman."}
        },
        "Trimestre 2": {
            1: {"pregunta": "2º Sec: Un triángulo rectángulo tiene catetos a = 6 y b = 8. ¿Cuánto mide la hipotenusa c?", "correcta": "10", "pista": "Aplica Pitágoras: c² = 6² + 8² = 36 + 64 = 100."}
        },
        "Trimestre 3": {
            1: {"pregunta": "2º Sec: Calcula el área de un cuadrado cuyo lado mide 12 cm.", "correcta": "144", "pista": "Lado por lado (12 * 12)."}
        }
    },
    "3º": {
        "Trimestre 1": {
            1: {"pregunta": "3º Sec: En la ecuación x² - 25 = 0, ¿cuál es el valor de la raíz positiva de x?", "correcta": "5", "pista": "Despeja x² = 25 y saca la raíz cuadrada."}
        },
        "Trimestre 2": {
            1: {"pregunta": "3º Sec: En un triángulo rectángulo con Cateto Opuesto = 4 e Hipotenusa = 5, calcula Sen(θ) en decimal.", "correcta": "0.8", "pista": "Seno = Opuesto / Hipotenusa = 4 / 5."}
        },
        "Trimestre 3": {
            1: {"pregunta": "3º Sec: Resuelve x² - 9x + 20 = 0. ¿Cuál es la raíz mayor?", "correcta": "5", "pista": "Busca dos números que multiplicados den 20 y sumados den 9 (4 y 5)."}
        }
    }
}

# ---------------------------------------------------------
# MÚSICA DE YOUTUBE Y MARCA DE AGUA
# ---------------------------------------------------------
st.sidebar.markdown("🎵 **Música de Fondo (YouTube):**")
opcion_musica = st.sidebar.radio(
    "Selecciona Pista:",
    ["Zelda - Ocarina of Time", "Resident Evil - Save Room Lofi"],
    label_visibility="collapsed"
)

# Enlaces exactos enviados
if opcion_musica == "Zelda - Ocarina of Time":
    url_yt = "https://youtu.be/gVJzgXehZW8"
else:
    url_yt = "https://youtu.be/S9cCNem6Tjk"

st.sidebar.video(url_yt)
st.sidebar.write("---")
st.sidebar.caption("⚡ *Hecho por Ilich Bauman Guerrero*")

if "usuario" not in st.session_state:
    st.session_state.usuario = None

# ---------------------------------------------------------
# 4. INICIO DE SESIÓN Y REGISTRO DE ALUMNOS
# ---------------------------------------------------------
if st.session_state.usuario is None:
    st.title("Colegio Educk Art")
    st.subheader("Plataforma de Desafíos Matemáticos")
    
    tab1, tab2, tab3 = st.tabs(["Ingresar Alumno", "Registrarse", "Panel Maestros"])
    
    with tab1:
        st.write("### Iniciar Sesión")
        mat_login = st.text_input("Matrícula o Usuario:")
        if st.button("Entrar a Jugar"):
            c = conn.cursor()
            c.execute("SELECT * FROM alumnos WHERE matricula = ?", (mat_login,))
            user = c.fetchone()
            if user:
                st.session_state.usuario = {
                    "matricula": user[0],
                    "nombre": user[1],
                    "grupo": user[2],
                    "t1": user[3],
                    "t2": user[4],
                    "t3": user[5],
                    "ultimo_dia": user[6],
                    "intentos": user[7] if len(user) > 7 else 0
                }
                st.rerun()
            else:
                st.error("Matrícula no encontrada. Regístrate primero.")
                
    with tab2:
        st.write("### Registro de Nuevo Alumno")
        nombre_reg = st.text_input("Nombre Completo:")
        mat_reg = st.text_input("Matrícula / ID de Alumno:")
        grupo_reg = st.selectbox("Grado y Grupo:", ["1º A", "1º B", "2º A", "2º B", "3º A", "3º B"])
        if st.button("Crear Cuenta"):
            if nombre_reg and mat_reg:
                try:
                    c = conn.cursor()
                    c.execute("INSERT INTO alumnos (matricula, nombre, grupo) VALUES (?, ?, ?)",
                              (mat_reg, nombre_reg, grupo_reg))
                    conn.commit()
                    st.success("¡Cuenta creada con éxito! Ahora inicia sesión.")
                except sqlite3.IntegrityError:
                    st.error("Esa matrícula ya está registrada.")
            else:
                st.warning("Llena todos los campos.")

    with tab3:
        st.write("### 📊 Panel de Control Académico para Maestros")
        clave_maestro = st.text_input("Contraseña de Maestro:", type="password")
        
        if clave_maestro == "admin123":
            df = pd.read_sql_query("SELECT matricula AS Matrícula, nombre AS Nombre, grupo AS Grupo, trimestre1_nivel-1 AS T1_Niveles, trimestre2_nivel-1 AS T2_Niveles, trimestre3_nivel-1 AS T3_Niveles, intentos_fallidos AS Intentos_Hoy FROM alumnos", conn)
            
            if df.empty:
                st.info("Aún no hay alumnos registrados en la base de datos.")
            else:
                df['Niveles_Totales'] = df['T1_Niveles'] + df['T2_Niveles'] + df['T3_Niveles']
                df['Calificación_Sugerida'] = (5.0 + (df['Niveles_Totales'] / 90.0) * 5.0).round(1)

                st.write("---")
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Alumnos", len(df))
                col2.metric("Promedio General", f"{df['Calificación_Sugerida'].mean():.1f}")
                col3.metric("Niveles Completados", int(df['Niveles_Totales'].sum()))
                
                st.write("---")
                st.write("#### 🔎 Filtros de Búsqueda")
                
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    filtro_grado = st.selectbox("Filtrar por Grado:", ["Todos", "1º", "2º", "3º"])
                with col_f2:
                    filtro_grupo = st.selectbox("Filtrar por Grupo Específico:", ["Todos", "1º A", "1º B", "2º A", "2º B", "3º A", "3º B"])
                
                busqueda = st.text_input("🔍 Buscar por Nombre o Matrícula:")

                df_filtrado = df.copy()
                if filtro_grado != "Todos":
                    df_filtrado = df_filtrado[df_filtrado['Grupo'].str.startswith(filtro_grado)]
                if filtro_grupo != "Todos":
                    df_filtrado = df_filtrado[df_filtrado['Grupo'] == filtro_grupo]
                if busqueda:
                    df_filtrado = df_filtrado[
                        df_filtrado['Nombre'].str.contains(busqueda, case=False) | 
                        df_filtrado['Matrícula'].str.contains(busqueda, case=False)
                    ]

                st.write(f"**Resultados ({len(df_filtrado)} alumnos):**")
                st.dataframe(df_filtrado, use_container_width=True)

                csv = df_filtrado.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Descargar Reporte en Excel (CSV)",
                    data=csv,
                    file_name="reporte_calificaciones_educkart.csv",
                    mime="text/csv"
                )

                st.write("---")
                st.write("#### 🛠️ Desbloquear Intentos de Alumno")
                mat_desbloquear = st.selectbox("Seleccionar Alumno bloqueado:", df[df['Intentos_Hoy'] >= 3]['Matrícula'].tolist() if len(df[df['Intentos_Hoy'] >= 3]) > 0 else ["Ningún alumno bloqueado hoy"])
                if st.button("Reiniciar Intentos") and mat_desbloquear != "Ningún alumno bloqueado hoy":
                    c = conn.cursor()
                    c.execute("UPDATE alumnos SET intentos_fallidos = 0 WHERE matricula = ?", (mat_desbloquear,))
                    conn.commit()
                    st.success(f"Intentos reiniciados con éxito para la matrícula {mat_desbloquear}.")
                    st.rerun()

        elif clave_maestro != "":
            st.error("Contraseña incorrecta.")
            
    st.write("---")
    st.caption("✨ *Hecho por Ilich Bauman Guerrero*")
    st.stop()

# ---------------------------------------------------------
# 5. PLATAFORMA DE JUEGO (ALUMNO LOGUEADO)
# ---------------------------------------------------------
u = st.session_state.usuario
grado_alumno = u['grupo'][:2]

st.sidebar.write(f"👤 **Alumno:** {u['nombre']}")
st.sidebar.write(f"🏫 **Grupo:** {u['grupo']}")

if st.sidebar.button("Cerrar Sesión"):
    st.session_state.usuario = None
    st.rerun()

st.title("📐 Desafío Matemático")

trimestre_sel = st.selectbox("Selecciona el Trimestre a trabajar:", ["Trimestre 1", "Trimestre 2", "Trimestre 3"])

if trimestre_sel == "Trimestre 1":
    nivel_actual = u['t1']
    col_db = "trimestre1_nivel"
elif trimestre_sel == "Trimestre 2":
    if u['t1'] <= 30:
        st.warning("🔒 Debes completar los 30 niveles del Trimestre 1 para desbloquear este trimestre.")
        st.stop()
    nivel_actual = u['t2']
    col_db = "trimestre2_nivel"
else:
    if u['t2'] <= 30:
        st.warning("🔒 Debes completar los 30 niveles del Trimestre 2 para desbloquear este trimestre.")
        st.stop()
    nivel_actual = u['t3']
    col_db = "trimestre3_nivel"

st.sidebar.metric(f"Progreso {trimestre_sel}", f"Nivel {min(nivel_actual, 30)} / 30")

if nivel_actual > 30:
    st.balloons()
    st.success(f"🏆 ¡Has completado los 30 niveles del {trimestre_sel}!")
    st.stop()

hoy = str(date.today())
if u['ultimo_dia'] == hoy:
    st.warning("⏳ **¡Ya completaste tu nivel de hoy!**")
    st.info("Vuelve mañana para desbloquear el siguiente nivel.")
    st.stop()

if u['intentos'] >= 3:
    st.error("🚫 **Has agotado tus 3 intentos de hoy para este nivel.**")
    st.info("Consulta la duda con tu profesor(a) en clase y vuelve a intentarlo mañana.")
    st.stop()

# ---------------------------------------------------------
# 6. EVALUACIÓN Y AVISO DE CUADERNO
# ---------------------------------------------------------
st.subheader(f"🟢 {grado_alumno} Secundaria | {trimestre_sel} | Nivel {nivel_actual} de 30")

st.warning("📝 **¡Atención!** Saca tu cuaderno de matemáticas y realiza el procedimiento paso a paso antes de responder.")

preguntas_grado = banco_por_grado.get(grado_alumno, {}).get(trimestre_sel, {})
datos_nivel = preguntas_grado.get(nivel_actual, {
    "pregunta": f"Escribe el resultado numérico exacto para el desafío de {grado_alumno} Secundaria del nivel {nivel_actual}.",
    "correcta": "10",
    "pista": "Resuelve la operación en tu cuaderno paso a paso antes de escribir la respuesta."
})

st.write(f"**Desafío:** {datos_nivel['pregunta']}")
st.caption(f"⚠️ Intentos fallidos hoy: {u['intentos']} / 3")

with st.form(key=f"form_abierto_{trimestre_sel}_{nivel_actual}"):
    respuesta_usuario = st.text_input("Escribe tu resultado final (solo el valor numérico):")
    
    if st.form_submit_button("Validar Respuesta"):
        resp_limpia = respuesta_usuario.strip().lower()
        corr_limpia = datos_nivel["correcta"].strip().lower()
        
        if resp_limpia == corr_limpia:
            st.success("🎉 ¡Respuesta correcta! Nivel superado.")
            nuevo_nivel = nivel_actual + 1
            
            c = conn.cursor()
            c.execute(f"UPDATE alumnos SET {col_db} = ?, ultimo_dia_jugado = ?, intentos_fallidos = 0 WHERE matricula = ?", 
                      (nuevo_nivel, hoy, u['matricula']))
            conn.commit()
            
            if col_db == "trimestre1_nivel": u['t1'] = nuevo_nivel
            elif col_db == "trimestre2_nivel": u['t2'] = nuevo_nivel
            elif col_db == "trimestre3_nivel": u['t3'] = nuevo_nivel
            u['ultimo_dia'] = hoy
            u['intentos'] = 0
            
            st.rerun()
        else:
            nuevos_intentos = u['intentos'] + 1
            u['intentos'] = nuevos_intentos
            
            c = conn.cursor()
            c.execute("UPDATE alumnos SET intentos_fallidos = ? WHERE matricula = ?", (nuevos_intentos, u['matricula']))
            conn.commit()
            
            if nuevos_intentos >= 3:
                st.error("❌ Respuesta incorrecta. Has alcanzado el límite de 3 intentos.")
                st.rerun()
            else:
                st.error(f"❌ Respuesta incorrecta. Te quedan {3 - nuevos_intentos} intento(s).")

if st.checkbox("💡 Ver Pista"):
    st.info(datos_nivel["pista"])

st.write("---")
st.caption("✨ *Hecho por Ilich Bauman Guerrero*")