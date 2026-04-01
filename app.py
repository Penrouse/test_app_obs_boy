import streamlit as st
from rag_motor import responder

st.set_page_config(
    page_title="Red de Observatorios – Boyacá",
    page_icon="🏛️",
    layout="wide",
)

# ── Paleta por dimensión ──────────────────────────────────────────────────────
DIM_CONFIG = {
    "Todas":     {"color": "#1A3A5C", "accent": "#0D7377",  "icon": "fa-globe"},
    "Económica": {"color": "#145A32", "accent": "#1E8449",  "icon": "fa-chart-line"},
    "Salud":     {"color": "#1A5276", "accent": "#2E86C1",  "icon": "fa-heart-pulse"},
    "Violencia": {"color": "#78281F", "accent": "#C0392B",  "icon": "fa-shield-halved"},
}

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
  .block-container{padding-top:0!important;max-width:100%!important;}
  #MainMenu,footer,header{visibility:hidden;}

  .portal-header{
    background:#0D1B2A;padding:.75rem 2rem;
    display:flex;align-items:center;justify-content:space-between;
    border-bottom:3px solid #0D7377;
  }
  .brand{display:flex;align-items:center;gap:12px;}
  .brand-icon{
    width:42px;height:42px;background:#0D7377;border-radius:8px;
    display:flex;align-items:center;justify-content:center;
  }
  .brand-text p{margin:0;font-size:11px;color:#8FA8BC;text-transform:uppercase;letter-spacing:1px;}
  .brand-text h1{margin:0;font-size:18px;color:#fff;font-weight:700;}
  .portal-nav{display:flex;gap:6px;}
  .portal-nav a{
    color:#8FA8BC;font-size:13px;padding:6px 14px;
    border-radius:6px;text-decoration:none;
  }
  .portal-nav a.active{background:#0D7377;color:#fff;}

  .hero-strip{
    background:#0D1B2A;
    border-bottom:1px solid #1E3A5A;
    padding:1.5rem 2rem;
  }
  .hero-chip{
    display:inline-block;
    background:rgba(13,115,119,.25);color:#5DCAA5;
    border:1px solid #0D7377;font-size:11px;font-weight:600;
    letter-spacing:1px;text-transform:uppercase;
    padding:3px 12px;border-radius:20px;margin-bottom:8px;
  }
  .hero-strip h2{font-size:1.4rem;font-weight:700;color:#fff;margin:0 0 4px;}
  .hero-strip p{font-size:13px;color:#8FA8BC;margin:0;}

  .msg-user{
    background:#0D1B2A;color:#fff;
    border-radius:16px 16px 4px 16px;
    padding:10px 16px;margin:8px 0 8px auto;
    max-width:74%;width:fit-content;font-size:14px;line-height:1.5;
  }
  .msg-bot{
    background:#fff;
    border-left:4px solid var(--acc,#0D7377);
    border-radius:0 16px 16px 16px;
    padding:12px 16px;margin:8px auto 8px 0;
    max-width:84%;font-size:14px;color:#1E3A4A;line-height:1.6;
    box-shadow:0 2px 8px rgba(0,0,0,.06);
  }
  .fuente-tag{
    display:inline-block;
    background:#EDF4F8;color:#1A5276;
    border:1px solid #AED6F1;
    font-size:11px;padding:2px 8px;
    border-radius:10px;margin:2px 2px 0 0;
  }
  .empty-state{
    text-align:center;padding:50px 20px;color:#8FA8BC;
  }

  section[data-testid="stSidebar"]{background:#0D1B2A!important;}
  section[data-testid="stSidebar"] label,
  section[data-testid="stSidebar"] p,
  section[data-testid="stSidebar"] span,
  section[data-testid="stSidebar"] div{color:#C5D8E8!important;}
  section[data-testid="stSidebar"] .stButton button{
    background:#132030!important;border:1px solid #1E3A5A!important;
    color:#C5D8E8!important;font-size:12px!important;text-align:left!important;
  }
  section[data-testid="stSidebar"] .stButton button:hover{
    background:#0D7377!important;color:#fff!important;border-color:#0D7377!important;
  }
  section[data-testid="stSidebar"] hr{border-color:#1E3A5A!important;}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="portal-header">
  <div class="brand">
    <div class="brand-icon">
      <i class="fa-solid fa-landmark" style="color:white;font-size:18px;"></i>
    </div>
    <div class="brand-text">
      <p>Gobernación de Boyacá</p>
      <h1>Red de Observatorios</h1>
    </div>
  </div>
  <nav class="portal-nav">
    <a href="https://observatorios.boyaca.gov.co" target="_blank">Inicio</a>
    <a href="#" class="active">
      <i class="fa-solid fa-robot" style="margin-right:5px;"></i>Asistente IA
    </a>
  </nav>
</div>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-strip">
  <span class="hero-chip">
    <i class="fa-solid fa-database" style="margin-right:4px;"></i>
    Plataforma de datos públicos y análisis territorial
  </span>
  <h2>Asistente inteligente de indicadores</h2>
  <p>Consulta indicadores oficiales en lenguaje natural · Respuestas basadas exclusivamente en datos del Observatorio</p>
</div>
""", unsafe_allow_html=True)

# ── Estado ────────────────────────────────────────────────────────────────────
if "mensajes"  not in st.session_state: st.session_state.mensajes  = []
if "dimension" not in st.session_state: st.session_state.dimension = "Todas"

# ── Selector de dimensión ─────────────────────────────────────────────────────
st.markdown("<div style='padding:1rem 0 .5rem;'>", unsafe_allow_html=True)
cols = st.columns(len(DIM_CONFIG))
labels = {"Todas": "Todas", "Económica": "Económica", "Salud": "Salud", "Violencia": "Violencia"}
for i, (dim, cfg) in enumerate(DIM_CONFIG.items()):
    with cols[i]:
        is_sel = st.session_state.dimension == dim
        border = "3px solid #fff" if is_sel else "3px solid transparent"
        st.markdown(f"""
        <div style="background:{cfg['color']};border-radius:10px;padding:14px 16px;
                    border:{border};margin-bottom:4px;">
          <i class="fa-solid {cfg['icon']}" style="color:white;font-size:20px;"></i>
          <p style="margin:6px 0 0;font-size:12px;font-weight:700;color:white;">{labels[dim]}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Seleccionar", key=f"d_{dim}", use_container_width=True):
            st.session_state.dimension = dim
            st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

dim_actual = st.session_state.dimension
cfg_actual = DIM_CONFIG[dim_actual]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="background:{cfg_actual['color']};border-radius:8px;
                padding:12px 16px;margin-bottom:12px;">
      <p style="margin:0;font-size:10px;text-transform:uppercase;
                letter-spacing:1px;color:rgba(255,255,255,.6);">Dimensión activa</p>
      <p style="margin:4px 0 0;font-size:15px;font-weight:700;color:#fff;">
        <i class="fa-solid {cfg_actual['icon']}" style="margin-right:6px;"></i>{dim_actual}
      </p>
    </div>
    """, unsafe_allow_html=True)

    mostrar_fuentes = st.toggle("Mostrar fuentes", value=True)
    st.markdown("---")
    st.markdown("### 💡 Preguntas de ejemplo")

    ejemplos_por_dimension = {
        "Económica": [
            "¿Cuál fue el PIB de Boyacá en 2024?",
            "¿Cuánto creció el PIB entre 2023 y 2024?",
            "¿Qué sector aporta más al PIB de Boyacá?",
            "¿Cómo evolucionó la agricultura entre 2010 y 2024?",
            "¿Cuál fue el impacto del COVID en el PIB de Boyacá?",
            "¿Cuánto aporta la construcción al PIB?",
            "¿Qué actividad económica creció más en 2024?",
        ],
        "Salud": [
            "¿Cuántas personas están afiliadas al SGSSS en Boyacá?",
            "¿Cuál es la tasa de mortalidad materna en Boyacá?",
            "¿Qué municipio tiene más casos de dengue?",
            "¿Cuántos nacidos vivos hubo en 2025?",
            "¿Cómo está la cobertura de vacunación BCG en Boyacá?",
            "¿Cuántos casos de tuberculosis se registraron?",
            "¿Cuál es la situación del embarazo en adolescentes?",
        ],
        "Violencia": [
            "¿Cuántos feminicidios se registraron en Boyacá en 2025?",
            "¿Qué municipio tiene más casos de violencia de género?",
            "¿Cuántos intentos de suicidio hubo en Boyacá?",
            "¿Cuál es la principal causa de lesiones fatales en Boyacá?",
            "¿Cuántos casos de violencia sexual se reportaron?",
            "¿Qué municipios registraron violencia en entornos educativos?",
            "¿Cuántos casos de conflicto armado se reportaron en 2025?",
        ],
        "Todas": [
            "¿Cuál fue el PIB de Boyacá en 2024?",
            "¿Cuántos feminicidios se registraron en Boyacá en 2025?",
            "¿Cuántas personas están afiliadas al SGSSS en Boyacá?",
            "¿Cuál es la principal causa de lesiones fatales en Boyacá?",
            "¿Cuál fue el impacto del COVID en el PIB de Boyacá?",
            "¿Qué municipio tiene más casos de violencia de género?",
            "¿Qué municipio tiene más casos de dengue?",
            "¿Cuántos intentos de suicidio hubo en Boyacá?",
        ],
    }

    for ej in ejemplos_por_dimension.get(dim_actual, []):
        if st.button(ej, use_container_width=True, key=f"ej_{ej[:25]}"):
            st.session_state["pregunta_rapida"] = ej

    st.markdown("---")
    if st.button("🗑️ Limpiar conversación", use_container_width=True):
        st.session_state.mensajes = []
        st.rerun()

    st.markdown("""
    <div style="text-align:center;padding-top:12px;">
      <p style="font-size:10px;color:#4A6B7A!important;margin:0;">
        Fuentes: DANE · Sec. Salud · Fiscalía<br>Boyacá © 2025
      </p>
    </div>
    """, unsafe_allow_html=True)

# ── Chat ──────────────────────────────────────────────────────────────────────
chat_container = st.container()
with chat_container:
    if not st.session_state.mensajes:
        st.markdown(f"""
        <div class="empty-state">
          <i class="fa-solid fa-comment-dots"
             style="font-size:44px;color:{cfg_actual['accent']};margin-bottom:12px;display:block;"></i>
          <p style="font-size:15px;margin:0;color:#4A6B7A;">
            Haz una pregunta sobre los indicadores del Observatorio de Boyacá
          </p>
          <p style="font-size:12px;margin:6px 0 0;color:#8FA8BC;">
            Dimensión activa: <strong>{dim_actual}</strong>
          </p>
        </div>
        """, unsafe_allow_html=True)

    for msg in st.session_state.mensajes:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="msg-user">{msg["content"]}</div>',
                unsafe_allow_html=True
            )
        else:
            fuentes_html = ""
            if mostrar_fuentes and msg.get("fuentes"):
                tags = "".join(
                    f'<span class="fuente-tag">'
                    f'<i class="fa-solid fa-database" style="font-size:9px;margin-right:3px;"></i>'
                    f'{f["actividad"][:45]}… ({f["anio"]})'
                    f'</span>'
                    for f in msg["fuentes"][:4]
                )
                fuentes_html = f'<div style="margin-top:10px;">{tags}</div>'

            st.markdown(
                f'<div class="msg-bot" style="--acc:{cfg_actual["accent"]}">'
                f'{msg["content"]}{fuentes_html}</div>',
                unsafe_allow_html=True
            )

# ── Input ─────────────────────────────────────────────────────────────────────
pregunta_rapida = st.session_state.pop("pregunta_rapida", None)
pregunta = st.chat_input(
    f"Consulta sobre indicadores de Boyacá · {dim_actual}..."
) or pregunta_rapida

if pregunta:
    st.session_state.mensajes.append({"role": "user", "content": pregunta})
    with st.spinner("Consultando base de conocimiento..."):
        dim_filtro = None if dim_actual == "Todas" else dim_actual
        resultado  = responder(pregunta, dimension=dim_filtro)
    st.session_state.mensajes.append({
        "role":    "assistant",
        "content": resultado["respuesta"],
        "fuentes": resultado["fuentes"],
    })
    st.rerun()
