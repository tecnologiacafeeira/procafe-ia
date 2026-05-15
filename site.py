import streamlit as st
from analisador import analisar_pdf, gerar_recomendacoes
import base64

st.set_page_config(
    page_title="Fundação Procafé - Diagnóstico Inteligente",
    page_icon="🌱",
    layout="wide"
)


def imagem_base64(caminho):
    with open(caminho, "rb") as arquivo:
        return base64.b64encode(arquivo.read()).decode()


def cor_diagnostico(texto):
    if "Baixo" in texto:
        return '<span class="badge baixo">● Baixo</span>'
    elif "Médio" in texto:
        return '<span class="badge medio">● Médio</span>'
    elif "Alto" in texto:
        return '<span class="badge alto">● Alto</span>'
    elif "Sem dado" in texto:
        return '<span class="badge sem-dado">● Sem dado</span>'
    return texto


logo = imagem_base64("assets/logo.png")

st.markdown(f"""
<style>
.stApp {{
    background:
        linear-gradient(rgba(255,248,232,0.18), rgba(255,248,232,0.18)),
        url("https://images.unsplash.com/photo-1447933601403-0c6688de566e?q=80&w=1800");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.block-container {{
    padding-top: 28px;
    max-width: 1180px;
}}

.hero {{
    background: linear-gradient(135deg, #064d2c, #08743b);
    border-radius: 18px;
    padding: 28px 44px;
    display: flex;
    align-items: center;
    gap: 34px;
    box-shadow: 0 10px 28px rgba(0,0,0,.28);
    margin-bottom: 18px;
}}

.logo {{
    width: 150px;
    height: 150px;
    object-fit: contain;
}}

.divider {{
    width: 2px;
    height: 120px;
    background: rgba(255,255,255,.75);
}}

.hero h1 {{
    color: white !important;
    font-size: 48px !important;
    margin: 0;
    letter-spacing: 1px;
}}

.hero h2 {{
    color: white !important;
    font-size: 34px !important;
    font-weight: 400;
    margin: 8px 0 0 0;
}}

.main-card {{
    background: rgba(255,250,235,.96);
    border-radius: 16px;
    padding: 34px;
    box-shadow: 0 8px 24px rgba(0,0,0,.22);
    border: 1px solid rgba(120,90,40,.25);
}}

.row {{
    display: grid;
    grid-template-columns: 36% 64%;
    gap: 28px;
    align-items: center;
    padding: 28px 0;
    border-bottom: 1px solid rgba(120,90,40,.22);
}}

.row:last-child {{
    border-bottom: none;
}}

.left {{
    display: flex;
    gap: 20px;
    align-items: flex-start;
}}

.icon {{
    font-size: 44px;
    color: #075c34;
    min-width: 55px;
}}

.title {{
    color: #073d25;
    font-size: 25px;
    font-weight: 800;
    margin-bottom: 8px;
}}

.desc {{
    color: #25362d;
    font-size: 17px;
    line-height: 1.45;
}}

.upload-box {{
    border: 2px dashed rgba(7,92,52,.28);
    border-radius: 14px;
    padding: 28px;
    text-align: center;
    background: rgba(255,255,255,.38);
}}

.action-box {{
    background: #eef2df;
    border-radius: 12px;
    padding: 22px 28px;
    color: #073d25;
    font-weight: 800;
    display: flex;
    align-items: center;
    gap: 18px;
    justify-content: space-between;
    border: 1px solid rgba(7,92,52,.15);
}}

.footer-card {{
    margin-top: 28px;
    display: flex;
    gap: 18px;
    align-items: center;
    color: #073d25;
    font-weight: 700;
}}

.footer-card span {{
    display: block;
    font-weight: 400;
    color: #25362d;
    margin-top: 4px;
}}

section[data-testid="stFileUploader"] {{
    background: transparent !important;
}}

section[data-testid="stFileUploader"] > div {{
    background: rgba(255,255,255,.65) !important;
    border-radius: 14px !important;
    border: 2px dashed rgba(7,92,52,.25) !important;
    padding: 22px !important;
}}

section[data-testid="stFileUploader"] label {{
    display: none !important;
}}

.badge {{
    font-weight: 700;
    padding-left: 4px;
}}

.baixo {{ color: #d62828; }}
.medio {{ color: #d9a21b; }}
.alto {{ color: #1faa66; }}
.sem-dado {{ color: #8d79b8; }}

.result-card {{
    background: rgba(255,255,255,.96);
    border-radius: 16px;
    padding: 24px;
    margin-top: 18px;
    border: 1px solid rgba(120,90,40,.22);
}}

.result-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px 30px;
    font-size: 17px;
}}

.result-card h3 {{
    color: #073d25 !important;
    margin-top: 18px;
}}

@media (max-width: 768px) {{
    .hero {{
        flex-direction: column;
        text-align: center;
        padding: 24px;
    }}

    .divider {{
        display: none;
    }}

    .logo {{
        width: 125px;
        height: 125px;
    }}

    .hero h1 {{
        font-size: 34px !important;
    }}

    .hero h2 {{
        font-size: 22px !important;
    }}

    .main-card {{
        padding: 22px;
    }}

    .row {{
        grid-template-columns: 1fr;
        gap: 14px;
    }}

    .result-grid {{
        grid-template-columns: 1fr;
    }}
}}
</style>

<div class="hero">
    <img class="logo" src="data:image/png;base64,{logo}">
    <div class="divider"></div>
    <div>
        <h1>FUNDAÇÃO PROCAFÉ</h1>
        <h2>Diagnóstico Inteligente de Solo</h2>
    </div>
</div>

<div class="main-card">
    <div class="row">
        <div class="left">
            <div class="icon">☁️</div>
            <div>
                <div class="title">Upload do Laudo de Análise de Solo (PDF)</div>
                <div class="desc">Envie o arquivo do laboratório para análise automática.</div>
            </div>
        </div>
        <div class="upload-box">
            <strong>Arraste e solte o arquivo aqui</strong><br>
            ou clique para selecionar<br>
            <small>somente arquivos PDF</small>
        </div>
    </div>
""", unsafe_allow_html=True)

arquivo = st.file_uploader("Selecione o laudo em PDF", type=["pdf"], label_visibility="collapsed")

st.markdown("""
    <div class="row">
        <div class="left">
            <div class="icon">▥</div>
            <div>
                <div class="title">Resultados da Análise</div>
                <div class="desc">Interpretação automática dos principais parâmetros do solo.</div>
            </div>
        </div>
        <div class="action-box">☰ <span>VER RESULTADOS</span>⌄</div>
    </div>

    <div class="row">
        <div class="left">
            <div class="icon">🌿</div>
            <div>
                <div class="title">Recomendações Agronômicas</div>
                <div class="desc">Sugestões personalizadas para melhoria da fertilidade do solo.</div>
            </div>
        </div>
        <div class="action-box">🌱 <span>VER RECOMENDAÇÕES</span>⌄</div>
    </div>

    <div class="row">
        <div class="left">
            <div class="icon">📄</div>
            <div>
                <div class="title">Relatório Técnico</div>
                <div class="desc">Gere um relatório técnico completo com todos os resultados.</div>
            </div>
        </div>
        <div class="action-box">📄 <span>GERAR RELATÓRIO PDF</span>⌄</div>
    </div>

    <div class="footer-card">
        <div class="icon">🛡️</div>
        <div>
            Tecnologia e conhecimento a serviço da cafeicultura
            <span>Fundação Procafé – Inovação para uma cafeicultura sustentável</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


if arquivo is not None:
    with open("temp.pdf", "wb") as f:
        f.write(arquivo.read())

    dados = analisar_pdf("temp.pdf")

    if not dados:
        st.error("O PDF foi carregado, mas nenhuma amostra foi identificada.")
        st.stop()

    st.success("Laudo processado com sucesso!")

    st.markdown("## Diagnóstico das Amostras")

    for item in dados:
        with st.expander(f"🌱 {item['numero']} - {item['nome']}"):

            st.markdown('<div class="result-card">', unsafe_allow_html=True)

            st.markdown("### Informações básicas")
            st.markdown(f"""
            <div class="result-grid">
                <div><b>pH H2O:</b> {item['ph_h2o']} - {cor_diagnostico(item['diag_ph'])}</div>
                <div><b>M.O.:</b> {item['mo']} - {cor_diagnostico(item['diag_mo'])}</div>
                <div><b>Al:</b> {item['al']} - {cor_diagnostico(item['diag_al'])}</div>
                <div><b>pH CaCl2:</b> {item['ph_cacl2']}</div>
                <div><b>V%:</b> {item['v_percent']} - {cor_diagnostico(item['diag_v'])}</div>
                <div><b>H + Al:</b> {item['h_al']} - {cor_diagnostico(item['diag_h_al'])}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### Macronutrientes")
            st.markdown(f"""
            <div class="result-grid">
                <div><b>P:</b> {item['p']} - {cor_diagnostico(item['diag_p'])}</div>
                <div><b>Ca:</b> {item['ca']} - {cor_diagnostico(item['diag_ca'])}</div>
                <div><b>S:</b> {item['s']} - {cor_diagnostico(item['diag_s'])}</div>
                <div><b>K:</b> {item['k']} - {cor_diagnostico(item['diag_k'])}</div>
                <div><b>Mg:</b> {item['mg']} - {cor_diagnostico(item['diag_mg'])}</div>
                <div><b>P-rem:</b> {item['p_rem']}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### Micronutrientes")
            st.markdown(f"""
            <div class="result-grid">
                <div><b>Zn:</b> {item['zn']} - {cor_diagnostico(item['diag_zn'])}</div>
                <div><b>Mn:</b> {item['mn']} - {cor_diagnostico(item['diag_mn'])}</div>
                <div><b>B:</b> {item['b']} - {cor_diagnostico(item['diag_b'])}</div>
                <div><b>Fe:</b> {item['fe']} - {cor_diagnostico(item['diag_fe'])}</div>
                <div><b>Cu:</b> {item['cu']} - {cor_diagnostico(item['diag_cu'])}</div>
                <div><b>T:</b> {item['t']}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### Recomendações")

            recomendacoes = gerar_recomendacoes(item)
            for r in recomendacoes:
                st.write("✅", r)

            st.markdown("</div>", unsafe_allow_html=True)
