import streamlit as st
import sqlite3
import pandas as pd
import random
import hashlib
from datetime import date

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Colegio Educk-Art - Plataforma de Desafíos Matemáticos",
    page_icon="📐",
    layout="centered"
)

# ---------------------------------------------------------
# 2. PALETA DE MARCA
# ---------------------------------------------------------
ROJO = "#D20C0B"
ROSA = "#E6007E"
AZUL = "#0099DA"
VERDE = "#009A44"
BLANCO = "#FFFFFF"

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
    border_color = "#555555"
else:
    bg_app = BLANCO
    bg_input = "#222222"
    text_color = "#111111"
    border_color = "#CCCCCC"

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_app} !important;
        color: {text_color} !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    h1, .stTitle {{
        color: {ROJO} !important;
        text-align: center !important;
        font-weight: 700 !important;
    }}
    h2, h3, .stSubheader {{
        color: {AZUL} !important;
    }}
    p, span, label, div {{
        color: {text_color} !important;
    }}
    button[data-baseweb="tab"] div p {{
        color: {AZUL} !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }}
    div[data-baseweb="input"], [data-baseweb="select"] > div {{
        background-color: {bg_input} !important;
        border: 2px solid {border_color} !important;
        border-radius: 8px !important;
    }}
    input, textarea, select, [data-baseweb="select"] * {{
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        background-color: {bg_input} !important;
        font-weight: bold !important;
    }}
    [data-testid="stSidebar"] {{
        background-color: {VERDE} !important;
    }}
    [data-testid="stSidebar"] * {{
        color: {BLANCO} !important;
    }}
    .stButton>button {{
        background-color: {ROJO} !important;
        color: {BLANCO} !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: bold !important;
        padding: 0.5rem 1.2rem !important;
        transition: all 0.3s ease !important;
    }}
    .stButton>button:hover {{
        background-color: {ROSA} !important;
        transform: scale(1.02);
    }}
    .marca-agua {{
        color: {text_color} !important;
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
@st.cache_resource
def conectar_db():
    conn = sqlite3.connect("colegio_math.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS alumnos (
            matricula TEXT PRIMARY KEY,
            nombre TEXT,
            grupo TEXT,
            pin_hash TEXT,
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


def hash_pin(pin: str) -> str:
    return hashlib.sha256(pin.encode("utf-8")).hexdigest()


def pin_valido(pin: str) -> bool:
    return pin.isdigit() and len(pin) == 4


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
            altura_mostrada = random.randint(4, 14) * 2
            altura_real = altura_mostrada // 2
            area = (base * altura_real) // 2
            return {
                "pregunta": f"NEM (Perímetros y Áreas): Calcula el área en cm² de un triángulo con base = {base} cm y altura = {altura_mostrada} cm.",
                "correcta": str(area),
                "pista": "Aplica la fórmula general del área del triángulo: (Base * Altura) / 2. Recuerda que la altura del enunciado ya es el valor completo a usar en la fórmula."
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

    else:  # 3º de Secundaria
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
            volumen = round(3.14 * (r ** 2) * h, 1)
            return {
                "pregunta": f"NEM (Volumen de Cuerpos): Calcula el volumen en cm³ de un cilindro con radio r = {r} cm, altura h = {h} cm (Usa π = 3.14).",
                "correcta": str(volumen),
                "pista": f"Fórmula del volumen: V = π * r² * h. Es decir: 3.14 * ({r}²) * {h}."
            }


def respuesta_es_correcta(resp_usuario: str, correcta_str: str) -> bool:
    resp_norm = resp_usuario.strip().replace(",", ".")
    corr_norm = correcta_str.strip().replace(",", ".")
    try:
        return abs(float(resp_norm) - float(corr_norm)) < 0.01
    except ValueError:
        return resp_norm.lower() == corr_norm.lower()


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
    st.title("Colegio Educk-Art")
    st.subheader("Plataforma de Desafíos Matemáticos (NEM)")

    tab1, tab2, tab3 = st.tabs(["Ingresar Alumno", "Registrarse", "Panel Maestros"])

    with tab1:
        st.write("### Iniciar Sesión")
        mat_login = st.text_input("Matrícula o Usuario:")
        pin_login = st.text_input("PIN (4 dígitos):", type="password", max_chars=4)
        if st.button("Entrar a Jugar"):
            c = conn.cursor()
            c.execute("SELECT * FROM alumnos WHERE matricula = ?", (mat_login,))
            user = c.fetchone()
            if user is None:
                st.error("Matrícula no encontrada. Regístrate primero.")
            elif user["pin_hash"] != hash_pin(pin_login):
                st.error("PIN incorrecto.")
            else:
                st.session_state.usuario = {
                    "matricula": user["matricula"],
                    "nombre": user["nombre"],
                    "grupo": user["grupo"],
                    "t1": user["trimestre1_nivel"],
                    "t2": user["trimestre2_nivel"],
                    "t3": user["trimestre3_nivel"],
                    "ultimo_dia": user["ultimo_dia_jugado"],
                    "intentos": user["intentos_fallidos"],
                }
                st.rerun()

    with tab2:
        st.write("### Registro de Nuevo Alumno")
        nombre_reg = st.text_input("Nombre Completo:")
        mat_reg = st.text_input("Matrícula / ID de Alumno:")
        grupo_reg = st.selectbox("Grado y Grupo:", ["1º A", "1º B", "2º A", "2º B", "3º A", "3º B"])
        pin_reg = st.text_input("Elige un PIN de 4 dígitos:", type="password", max_chars=4)
        pin_reg_confirm = st.text_input("Confirma tu PIN:", type="password", max_chars=4)

        if st.button("Crear Cuenta"):
            if not (nombre_reg and mat_reg):
                st.warning("Llena tu nombre y matrícula.")
            elif not pin_valido(pin_reg):
                st.warning("El PIN debe tener exactamente 4 dígitos numéricos.")
            elif pin_reg != pin_reg_confirm:
                st.warning("Los dos PIN no coinciden.")
            else:
                try:
                    c = conn.cursor()
                    c.execute(
                        "INSERT INTO alumnos (matricula, nombre, grupo, pin_hash) VALUES (?, ?, ?, ?)",
                        (mat_reg, nombre_reg, grupo_reg, hash_pin(pin_reg))
                    )
                    conn.commit()
                    st.success("¡Cuenta creada con éxito! Ahora inicia sesión con tu matrícula y PIN.")
                except sqlite3.IntegrityError:
                    st.error("Esa matrícula ya está registrada.")

    with tab3:
        st.write("### 📊 Panel de Control Académico para Maestros")
        PASSWORD_MAESTRO = "admin123"  # ⚠️ Contraseña de prueba, cámbiala antes de usar en producción

        clave_maestro = st.text_input("Contraseña de Maestro:", type="password")

        if clave_maestro == PASSWORD_MAESTRO:
            df = pd.read_sql_query(
                "SELECT matricula AS Matrícula, nombre AS Nombre, grupo AS Grupo, "
                "trimestre1_nivel-1 AS T1_Niveles, trimestre2_nivel-1 AS T2_Niveles, "
                "trimestre3_nivel-1 AS T3_Niveles, intentos_fallidos AS Intentos_Hoy "
                "FROM alumnos", conn
            )

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
                bloqueados = df[df['Intentos_Hoy'] >= 3]['Matrícula'].tolist()
                mat_desbloquear = st.selectbox(
                    "Seleccionar Alumno bloqueado:",
                    bloqueados if bloqueados else ["Ningún alumno bloqueado hoy"]
                )
                if st.button("Reiniciar Intentos") and mat_desbloquear != "Ningún alumno bloqueado hoy":
                    c = conn.cursor()
                    c.execute("UPDATE alumnos SET intentos_fallidos = 0 WHERE matricula = ?", (mat_desbloquear,))
                    conn.commit()
                    st.success(f"Intentos reiniciados con éxito para la matrícula {mat_desbloquear}.")
                    st.rerun()

                st.write("---")
                st.write("#### 🔑 Restablecer PIN de Alumno")
                mat_reset = st.selectbox(
                    "Seleccionar Alumno:",
                    df['Matrícula'].tolist() if not df.empty else ["Sin alumnos"]
                )
                nuevo_pin = st.text_input("Nuevo PIN de 4 dígitos:", max_chars=4, key="reset_pin")
                if st.button("Restablecer PIN"):
                    if not pin_valido(nuevo_pin):
                        st.warning("El PIN debe tener exactamente 4 dígitos numéricos.")
                    else:
                        c = conn.cursor()
                        c.execute("UPDATE alumnos SET pin_hash = ? WHERE matricula = ?", (hash_pin(nuevo_pin), mat_reset))
                        conn.commit()
                        st.success(f"PIN restablecido para {mat_reset}.")

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
        if respuesta_es_correcta(respuesta_usuario, datos_nivel["correcta"]):
            st.success("🎉 ¡Respuesta correcta! Nivel superado.")
            nuevo_nivel = nivel_actual + 1

            c = conn.cursor()
            c.execute(
                f"UPDATE alumnos SET {col_db} = ?, ultimo_dia_jugado = ?, intentos_fallidos = 0 WHERE matricula = ?",
                (nuevo_nivel, hoy, u['matricula'])
            )
            conn.commit()

            if col_db == "trimestre1_nivel":
                u['t1'] = nuevo_nivel
            elif col_db == "trimestre2_nivel":
                u['t2'] = nuevo_nivel
            elif col_db == "trimestre3_nivel":
                u['t3'] = nuevo_nivel
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
