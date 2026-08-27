import streamlit as st
import sqlite3
import pandas as pd
import random
from datetime import date

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Colegio Educk Art - Plataforma de Desafíos Matemáticos",
    page_icon="📐",
    layout="centered"
)

# ---------------------------------------------------------
# 2. SELECTOR DE TEMA (CLARO / OSCURO)
# ---------------------------------------------------------
st.sidebar.markdown("🎨 **Apariencia:**")
modo_tema = st.sidebar.radio(
    "Selecciona Tema:",
    ["☀️ Modo Luz", "🌙 Modo Oscuro"],
    label_visibility="collapsed"
)

if modo_tema == "🌙 Modo Oscuro":
    bg_app = "#1E1E1E"          
    bg_input = "#2D2D2D"        
    text_color = "#FFFFFF"      
    text_pestanas = "#0099DA"   
    text_autor = "#FFFFFF"      
    border_color = "#555555"
else:
    bg_app = "#FFFFFF"          
    bg_input = "#333333"  # Fondo oscuro elegante para resaltar el texto blanco      
    text_color = "#111111"      
    text_pestanas = "#009A44"   
    text_autor = "#000000"      
    border_color = "#CCCCCC"

st.markdown(f"""
    <style>
    /* Fondo e interfaz general */
    .stApp {{
        background-color: {bg_app} !important;
        color: {text_color} !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    h1, .stTitle {{
        color: #E6007E !important;
        text-align: center !important;
        font-weight: 700 !important;
    }}
    
    h2, h3, .stSubheader {{
        color: #0099DA !important;
    }}
    
    p, span, label, div {{
        color: {text_color} !important;
    }}

    /* Pestañas superiores */
    button[data-baseweb="tab"] div p {{
        color: {text_pestanas} !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }}
    
    /* Cajas de entrada de texto */
    div[data-baseweb="input"] {{
        background-color: {bg_input} !important;
        border: 2px solid {border_color} !important;
        border-radius: 8px !important;
    }}
    
    /* TEXTO SIEMPRE BLANCO EN LAS CAJAS DE ENTRADA */
    input {{
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        background-color: transparent !important;
        font-weight: bold !important;
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: #009A44 !important;
    }}
    
    [data-testid="stSidebar"] * {{
        color: #FFFFFF !important;
    }}
    
    /* Botones */
    .stButton>button {{
        background-color: #E6007E !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: bold !important;
        padding: 0.5rem 1.2rem !important;
        transition: all 0.3s ease !important;
    }}
    
    .stButton>button:hover {{
        background-color: #0099DA !important;
        transform: scale(1.02);
    }}
    
    /* Marca de Agua */
    .marca-agua {{
        color: {text_autor} !important;
        text-align: center;
        font-weight: bold;
        font-size: 0.95rem;
        margin-top: 25px;
        padding: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. BASE DE DATOS SQLITE
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
# 4. GENERADOR DINÁMICO DE EJERCICIOS NEM POR GRADO/TRIMESTRE
# ---------------------------------------------------------
def generar_ejercicio_nem(grado, trimestre, nivel, matricula):
    semilla = f"{matricula}_{date.today()}_{nivel}"
    random.seed(semilla)
    
    if grado == "1º":
        if trimestre == "Trimestre 1":
            a = random.randint(-15, -2)
            b = random.randint(-12, -1)
            ans = a + b
            return {
                "pregunta": f"NEM (Números Enteros): Resuelve la operación con signo: ({a}) + ({b})",
                "correcta": str(ans),
                "pista": "Al sumar dos números negativos, sus magnitudes se suman y el resultado mantiene el signo negativo."
            }
        elif trimestre == "Trimestre 2":
            x = random.randint(2, 12)
            a = random.randint(2, 6)
            b = random.randint(3, 15)
            c = a * x + b
            return {
                "pregunta": f"NEM (Ecuaciones de Primer Grado): Resuelve para x: {a}x + {b} = {c}",
                "correcta": str(x),
                "pista": f"Resta {b} a {c} y luego divide el resultado entre {a}."
            }
        else:
            base = random.randint(6, 20)
            altura = random.randint(4, 14)
            area = (base * altura) // 2
            return {
                "pregunta": f"NEM (Perímetros y Áreas): Calcula el área en cm² de un triángulo con base = {base} cm y altura = {altura*2} cm.",
                "correcta": str(base * altura),
                "pista": "Aplica la fórmula general del área del triángulo: (Base * Altura) / 2."
            }

    elif grado == "2º":
        if trimestre == "Trimestre 1":
            exp1 = random.randint(3, 8)
            exp2 = random.randint(2, 7)
            ans = exp1 + exp2
            return {
                "pregunta": f"NEM (Leyes de los Exponentes): Si simplificas x^{{{exp1}}} * x^{{{exp2}}} = xⁿ, ¿cuál es el valor exacto del exponente n?",
                "correcta": str(ans),
                "pista": "Recuerda la regla fundamental: al multiplicar potencias con la misma base, los exponentes se suman."
            }
        elif trimestre == "Trimestre 2":
            k = random.randint(2, 5)
            a = 3 * k
            b = 4 * k
            c = 5 * k
            return {
                "pregunta": f"NEM (Teorema de Pitágoras): Un triángulo rectángulo tiene catetos a = {a} cm y b = {b} cm. ¿Cuánto mide la hipotenusa c?",
                "correcta": str(c),
                "pista": f"Aplica la fórmula c = √(a² + b²). Calcula {a}² + {b}² y obtén la raíz cuadrada."
            }
        else:
            trabajadores_1 = random.choice([2, 3, 4])
            horas_1 = random.choice([12, 24, 36])
            trabajadores_2 = trabajadores_1 * 2
            horas_2 = horas_1 // 2
            return {
                "pregunta": f"NEM (Variación Inversa): Si {trabajadores_1} obreros tardan {horas_1} horas en terminar una obra, ¿cuántas horas tardarán {trabajadores_2} obreros?",
                "correcta": str(horas_2),
                "pista": "En la proporcionalidad inversa, si la cantidad de personas se duplica, el tiempo requerido se reduce a la mitad."
            }

    else: # 3º de Secundaria
        if trimestre == "Trimestre 1":
            raiz = random.randint(4, 12)
            cuadrado = raiz ** 2
            return {
                "pregunta": f"NEM (Ecuaciones Cuadráticas): Resuelve x² - {cuadrado} = 0. Escribe la raíz positiva de x.",
                "correcta": str(raiz),
                "pista": f"Despeja x² = {cuadrado} y obtén la raíz cuadrada exacta."
            }
        elif trimestre == "Trimestre 2":
            mult = random.randint(1, 4)
            co = 3 * mult
            ca = 4 * mult
            hip = 5 * mult
            seno = round(co / hip, 2)
            return {
                "pregunta": f"NEM (Razones Trigonométricas): En un triángulo rectángulo con Cateto Opuesto = {co} e Hipotenusa = {hip}, calcula Sen(θ) en valor decimal exacto.",
                "correcta": str(seno),
                "pista": "Fórmula trigonométrica: Sen(θ) = Cateto Opuesto / Hipotenusa."
            }
        else:
            r = random.randint(2, 5)
            h = random.randint(4, 10)
            volumen = round(3.14 * (r**2) * h, 1)
            return {
                "pregunta": f"NEM (Volumen de Cuerpos): Calcula el volumen en cm³ de un cilindro con radio r = {r} cm, altura h = {h} cm (Usa π = 3.14).",
                "correcta": str(volumen),
                "pista": f"Fórmula del volumen: V = π * r² * h. Es decir: 3.14 * ({r}²) * {h}."
            }

# ---------------------------------------------------------
# MÚSICA DE FONDO (YOUTUBE)
# ---------------------------------------------------------
st.sidebar.write("---")
st.sidebar.markdown("🎵 **Música Ambient (YouTube):**")
opcion_musica = st.sidebar.radio(
    "Pistas recomendadas:",
    ["Zelda - Ocarina of Time", "Resident Evil - Save Room Lofi"],
    label_visibility="collapsed"
)

url_yt = "https://youtu.be/gVJzgXehZW8" if opcion_musica == "Zelda - Ocarina of Time" else "https://youtu.be/S9cCNem6Tjk"

st.sidebar.video(url_yt)
st.sidebar.write("---")
st.sidebar.caption("⚡ *Hecho por Ilich Bauman Guerrero*")

if "usuario" not in st.session_state:
    st.session_state.usuario = None

# ---------------------------------------------------------
# 5. INICIO DE SESIÓN Y REGISTRO DE ALUMNOS
# ---------------------------------------------------------
if st.session_state.usuario is None:
    st.title("Colegio Educk Art")
    st.subheader("Plataforma de Desafíos Matemáticos (NEM)")
    
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
    st.markdown('<p class="marca-agua">✨ Hecho por Ilich Bauman Guerrero</p>', unsafe_allow_html=True)
    st.stop()

# ---------------------------------------------------------
# 6. PLATAFORMA DE JUEGO (ALUMNO LOGUEADO)
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

# ---------------------------------------------------------
# RESTRICCIÓN DIARIA (1 NIVEL POR DÍA)
# ---------------------------------------------------------
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
# 7. EVALUACIÓN Y AVISO DE CUADERNO
# ---------------------------------------------------------
st.subheader(f"🟢 {grado_alumno} Secundaria | {trimestre_sel} | Nivel {nivel_actual} de 30")

st.warning("📝 **¡Atención!** Saca tu cuaderno de matemáticas y realiza el procedimiento paso a paso antes de responder.")

datos_nivel = generar_ejercicio_nem(grado_alumno, trimestre_sel, nivel_actual, u['matricula'])

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
st.markdown('<p class="marca-agua">✨ Hecho por Ilich Bauman Guerrero</p>', unsafe_allow_html=True)