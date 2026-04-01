import base64, os
import streamlit as st
from rag_motor import responder

st.set_page_config(
    page_title="Red de Observatorios – Boyacá",
    page_icon="🏛️",
    layout="wide",
)

# ── Logo en base64 ────────────────────────────────────────────────────────────
def img_b64(path: str) -> str:
    if os.path.exists(path):
        ext = path.split(".")[-1]
        mime = "svg+xml" if ext == "svg" else ext
        with open(path, "rb") as f:
            return f"data:image/{mime};base64,{base64.b64encode(f.read()).decode()}"
    return ""

LOGO = img_b64("img/gobboy.png")

# ── Paleta por dimensión ──────────────────────────────────────────────────────
DIM = {
    "Todas":     {"bg": "#1A3A5C", "ac": "#0D7377",  "em": "🌐"},
    "Económica": {"bg": "#145A32", "ac": "#1E8449",  "em": "📈"},
    "Salud":     {"bg": "#1A5276", "ac": "#2E86C1",  "em": "🏥"},
    "Violencia": {"bg": "#78281F", "ac": "#C0392B",  "em": "🛡️"},
}

# ── CSS (un bloque único al inicio) ───────────────────────────────────────────
st.markdown("""
<style>
.block-container{padding-top:0!important;max-width:100%!important;}
#MainMenu,footer,header{visibility:hidden;}
.stDeployButton{display:none;}

.obs-header{
  background:#0D1B2A;
  padding:.7rem 1.5rem;
  display:flex;
  align-items:center;
  justify-content:space-between;
  border-bottom:3px solid #0D7377;
  margin-bottom:0;
}
.obs-brand{display:flex;align-items:center;gap:10px;}
.obs-brand-txt p{margin:0;font-size:10px;color:#8FA8BC;text-transform:uppercase;letter-spacing:1px;}
.obs-brand-txt h1{margin:0;font-size:17px;color:#fff;font-weight:700;line-height:1.2;}
.obs-nav{display:flex;gap:6px;}
.obs-nav a{color:#8FA8BC;font-size:12px;padding:5px 12px;border-radius:6px;text-decoration:none;}
.obs-nav a.act{background:#0D7377;color:#fff;}

.obs-hero{
  background:#0D1B2A;
  border-bottom:1px solid #1E3A5A;
  padding:1.2rem 1.5rem;
}
.obs-chip{
  display:inline-block;
  background:rgba(13,115,119,.3);color:#5DCAA5;
  border:1px solid #0D7377;font-size:10px;font-weight:700;
  letter-spacing:1px;text-transform:uppercase;
  padding:3px 10px;border-radius:20px;margin-bottom:8px;
}
.obs-hero h2{font-size:1.3rem;font-weight:700;color:#fff;margin:0 0 4px;}
.obs-hero p{font-size:12px;color:#8FA8BC;margin:0;}

.dim-card{
  border-radius:10px;padding:12px 14px;
  border:2px solid transparent;
  transition:border-color .2s;
}
.dim-card.sel{border-color:#fff!important;}
.dim-card p{margin:6px 0 0;font-size:12px;font-weight:700;color:#fff;}

.msg-u{
  background:#0D1B2A;color:#fff;
  border-radius:16px 16px 4px 16px;
  padding:9px 14px;margin:6px 0 6px auto;
  max-width:74%;width:fit-content;font-size:14px;line-height:1.5;
}
.msg-b{
  background:#fff;
  border-left:4px solid #0D7377;
  border-radius:0 14px 14px 14px;
  padding:11px 15px;margin:6px 0;
  max-width:84%;font-size:14px;color:#1E3A4A;line-height:1.6;
  box-shadow:0 2px 6px rgba(0,0,0,.07);
}
.ftag{
  display:inline-block;
  background:#EDF4F8;color:#1A5276;
  border:1px solid #AED6F1;
  font-size:10px;padding:2px 7px;
  border-radius:10px;margin:2px 2px 0 0;
}
.empty-s{text-align:center;padding:50px 20px;color:#8FA8BC;}

section[data-testid="stSidebar"]{background:#0D1B2A!important;}
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span{color:#C5D8E8!important;}
section[data-testid="stSidebar"] .stButton > button{
  background:#132030!important;
  border:1px solid #1E3A5A!important;
  color:#C5D8E8!important;
  font-size:12px!important;
  text-align:left!important;
  width:100%;
}
section[data-testid="stSidebar"] .stButton > button:hover{
  background:#0D7377!important;
  color:#fff!important;
  border-color:#0D7377!important;
}
section[data-testid="stSidebar"] hr{border-color:#1E3A5A!important;}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
logo_html = (f'<img src="{LOGO}" style="height:38px;filter:brightness(1.1);">'
             if LOGO else
             '<div style="width:38px;height:38px;background:#0D7377;border-radius:6px;'
             'display:flex;align-items:center;justify-content:center;font-size:18px;">🏛️</div>')

st.markdown(f"""
<div class="obs-header">
  <div class="obs-brand">
    {logo_html}
    <div class="obs-brand-txt">
      <p>Gobernación de Boyacá</p>
      <h1>Red de Observatorios</h1>
    </div>
  </div>
  <nav class="obs-nav">
    <a href="https://observatorios.boyaca.gov.co" target="_blank">Inicio</a>
    <a href="#" class="act">🤖 Asistente IA</a>
  </nav>
</div>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="obs-hero">
  <span class="obs-chip">📊 Plataforma de datos públicos y análisis territorial</span>
  <h2>Asistente inteligente de indicadores</h2>
  <p>Consulta indicadores oficiales en lenguaje natural · Respuestas basadas en datos del Observatorio</p>
</div>
""", unsafe_allow_html=True)

# ── Estado de sesión ──────────────────────────────────────────────────────────
if "mensajes"  not in st.session_state: st.session_state.mensajes  = []
if "dimension" not in st.session_state: st.session_state.dimension = "Todas"

# ── Cards de dimensión ────────────────────────────────────────────────────────
st.markdown("<div style='padding:.8rem 0 .4rem;'>", unsafe_allow_html=True)
cols = st.columns(len(DIM))
for col, (dim, cfg) in zip(cols, DIM.items()):
    with col:
        sel = "sel" if st.session_state.dimension == dim else ""
        st.markdown(f"""
        <div class="dim-card {sel}" style="background:{cfg['bg']};border-color:{'#fff' if sel else 'transparent'};">
          <span style="font-size:22px;">{cfg['em']}</span>
          <p>{dim}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Seleccionar", key=f"d_{dim}", use_container_width=True):
            st.session_state.dimension = dim
            st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

dim = st.session_state.dimension
cfg = DIM[dim]

# ── Sidebar ───────────────────────────────────────────────────────────────────
EJEMPLOS = {
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

with st.sidebar:
    st.markdown(f"""
    <div style="background:{cfg['bg']};border-radius:8px;padding:11px 14px;margin-bottom:12px;">
      <p style="margin:0;font-size:10px;text-transform:uppercase;letter-spacing:1px;
                color:rgba(255,255,255,.55);">Dimensión activa</p>
      <p style="margin:4px 0 0;font-size:15px;font-weight:700;color:#fff;">
        {cfg['em']} {dim}
      </p>
    </div>
    """, unsafe_allow_html=True)

    mostrar_fuentes = st.toggle("Mostrar fuentes", value=True)
    st.markdown("---")
    st.markdown("**💡 Preguntas de ejemplo**")

    for ej in EJEMPLOS.get(dim, []):
        if st.button(ej, key=f"ej_{ej[:20]}", use_container_width=True):
            st.session_state["pregunta_rapida"] = ej

    st.markdown("---")
    if st.button("🗑️ Limpiar conversación", use_container_width=True):
        st.session_state.mensajes = []
        st.rerun()

    st.markdown("""
    <p style="font-size:10px;text-align:center;color:#4A6B7A;margin-top:16px;">
      Fuentes: DANE · Sec. Salud · Fiscalía<br>Boyacá © 2025
    </p>
    """, unsafe_allow_html=True)

# ── Chat ──────────────────────────────────────────────────────────────────────
if not st.session_state.mensajes:
    st.markdown(f"""
    <div class="empty-s">
      <div style="font-size:44px;margin-bottom:10px;">{cfg['em']}</div>
      <p style="font-size:15px;color:#4A6B7A;margin:0;">
        Haz una pregunta sobre los indicadores del Observatorio de Boyacá
      </p>
      <p style="font-size:12px;color:#8FA8BC;margin:4px 0 0;">
        Dimensión activa: <strong>{dim}</strong>
      </p>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.mensajes:
    if msg["role"] == "user":
        st.markdown(f'<div class="msg-u">{msg["content"]}</div>',
                    unsafe_allow_html=True)
    else:
        ftags = ""
        if mostrar_fuentes and msg.get("fuentes"):
            ftags = "<div style='margin-top:8px;'>" + "".join(
                f'<span class="ftag">📎 {f["actividad"][:42]}… ({f["anio"]})</span>'
                for f in msg["fuentes"][:4]
            ) + "</div>"
        st.markdown(
            f'<div class="msg-b" style="border-left-color:{cfg["ac"]}">'
            f'{msg["content"]}{ftags}</div>',
            unsafe_allow_html=True,
        )

# ── Input ─────────────────────────────────────────────────────────────────────
pregunta_rapida = st.session_state.pop("pregunta_rapida", None)
pregunta = st.chat_input(f"Consulta sobre indicadores de Boyacá · {dim}...") or pregunta_rapida

if pregunta:
    st.session_state.mensajes.append({"role": "user", "content": pregunta})
    with st.spinner("Consultando base de conocimiento..."):
        resultado = responder(pregunta, dimension=None if dim == "Todas" else dim)
    st.session_state.mensajes.append({
        "role": "assistant",
        "content": resultado["respuesta"],
        "fuentes": resultado["fuentes"],
    })
    st.rerun()
