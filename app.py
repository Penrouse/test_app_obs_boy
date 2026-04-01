import streamlit as st
from rag_motor import responder

# ── Configuración de página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Observatorio Boyacá",
    page_icon="📊",
    layout="centered",
)

# ── Estilos ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .header { background:#0D2137; padding:1.5rem 2rem; border-radius:12px; margin-bottom:1.5rem; }
    .header h1 { color:white; font-size:1.6rem; margin:0; }
    .header p  { color:#8FA8BC; font-size:0.9rem; margin:0.3rem 0 0; }
    .fuente-card {
        background:#f0f7f4; border-left:3px solid #0D7377;
        padding:0.6rem 1rem; border-radius:6px;
        font-size:0.82rem; color:#1E3A4A; margin-top:0.4rem;
    }
    .badge {
        display:inline-block; background:#0D7377; color:white;
        padding:2px 10px; border-radius:12px; font-size:0.75rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header">
    <h1>📊 Asistente del Observatorio de Boyacá</h1>
    <p>Pregunta sobre los indicadores económicos del departamento · Respuestas basadas en datos oficiales del DANE</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar: filtros ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuración")
    dimension = st.selectbox(
        "Dimensión",
        options=["Todas", "Económica"],
        help="Filtra la búsqueda por dimensión del observatorio"
    )
    mostrar_fuentes = st.toggle("Mostrar fuentes", value=True)

    st.markdown("---")
    st.markdown("### 💡 Preguntas de ejemplo")
    ejemplos = [
        "¿Cuál fue el PIB de Boyacá en 2024?",
        "¿Cuánto creció el PIB entre 2023 y 2024?",
        "¿Qué sector aporta más al PIB de Boyacá?",
        "¿Cómo evolucionó la agricultura entre 2010 y 2024?",
        "¿Cuál fue el impacto del COVID en el PIB de Boyacá?",
    ]
    for ejemplo in ejemplos:
        if st.button(ejemplo, use_container_width=True):
            st.session_state["pregunta_rapida"] = ejemplo

    st.markdown("---")
    if st.button("🗑️ Limpiar conversación", use_container_width=True):
        st.session_state.mensajes = []
        st.rerun()

# ── Historial de mensajes ─────────────────────────────────────────────────────
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

for msg in st.session_state.mensajes:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and mostrar_fuentes and msg.get("fuentes"):
            with st.expander(f"📎 {len(msg['fuentes'])} fuentes utilizadas"):
                for f in msg["fuentes"][:4]:
                    st.markdown(f"""
                    <div class="fuente-card">
                        <span class="badge">{f['anio']}</span>
                        &nbsp;<strong>{f['actividad']}</strong> · {f['sector']}<br>
                        ${f['valor']:,.1f} miles MM · {f['tipo_precio']}<br>
                        <span style="color:#5F5E5A">{f['fuente']} · similitud: {f['similitud']}</span>
                    </div>
                    """, unsafe_allow_html=True)

# ── Input del usuario ─────────────────────────────────────────────────────────
pregunta_rapida = st.session_state.pop("pregunta_rapida", None)
pregunta = st.chat_input("Escribe tu pregunta sobre los indicadores de Boyacá...") or pregunta_rapida

if pregunta:
    # Mostrar mensaje del usuario
    st.session_state.mensajes.append({"role": "user", "content": pregunta})
    with st.chat_message("user"):
        st.markdown(pregunta)

    # Obtener respuesta
    with st.chat_message("assistant"):
        with st.spinner("Consultando la base de conocimiento..."):
            dim_filtro = None if dimension == "Todas" else dimension
            resultado  = responder(pregunta, dimension=dim_filtro)

        st.markdown(resultado["respuesta"])

        if mostrar_fuentes and resultado["fuentes"]:
            with st.expander(f"📎 {len(resultado['fuentes'])} fuentes utilizadas"):
                for f in resultado["fuentes"][:4]:
                    st.markdown(f"""
                    <div class="fuente-card">
                        <span class="badge">{f['anio']}</span>
                        &nbsp;<strong>{f['actividad']}</strong> · {f['sector']}<br>
                        ${f['valor']:,.1f} miles MM · {f['tipo_precio']}<br>
                        <span style="color:#5F5E5A">{f['fuente']} · similitud: {f['similitud']}</span>
                    </div>
                    """, unsafe_allow_html=True)

    # Guardar en historial
    st.session_state.mensajes.append({
        "role":    "assistant",
        "content": resultado["respuesta"],
        "fuentes": resultado["fuentes"],
    })
