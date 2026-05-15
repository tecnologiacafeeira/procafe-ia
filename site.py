import streamlit as st
from analisador import analisar_pdf, gerar_recomendacoes

st.set_page_config(
    page_title="Fundação Procafé - Diagnóstico Inteligente",
    page_icon="🌱",
    layout="wide"
)


def cor_diagnostico(texto):
    if "Baixo" in texto:
        return "🔴 Baixo"
    elif "Médio" in texto:
        return "🟡 Médio"
    elif "Alto" in texto:
        return "🟢 Alto"
    elif "Sem dado" in texto:
        return "⚪ Sem dado"
    return texto


st.markdown("""
<style>
.stApp {
    background:
        linear-gradient(rgba(245, 239, 225, 0.80), rgba(245, 239, 225, 0.86)),
        url("https://images.unsplash.com/photo-1447933601403-0c6688de566e?q=80&w=1800");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.block-container {
    max-width: 1180px;
    padding-top: 35px;
}

.hero {
    background: linear-gradient(135deg, #064d2c, #08743b);
    border-radius: 26px;
    padding: 34px 48px;
    margin-bottom: 26px;
    box-shadow: 0px 8px 26px rgba(0,0,0,0.28);
    display: flex;
    align-items: center;
    gap: 36px;
}

.logo-img {
    width: 155px;
    height: 155px;
    object-fit: contain;
}

.divider {
    width: 2px;
    height: 120px;
    background: rgba(255,255,255,0.75);
}

.hero-text h1 {
    color: white !important;
    font-size: 50px !important;
    margin: 0;
    letter-spacing: 1px;
}

.hero-text h3 {
    color: white !important;
    font-size: 34px !important;
    font-weight: 400;
    margin-top: 8px;
}

.main-card {
    background: rgba(255,250,235,0.96);
    border-radius: 22px;
    padding: 32px;
    box-shadow: 0px 8px 24px rgba(0,0,0,0.18);
    margin-bottom: 26px;
}

.feature-row {
    display: grid;
    grid-template-columns: 38% 62%;
    gap: 28px;
    align-items: center;
    padding: 26px 0;
    border-bottom: 1px solid rgba(120,90,40,0.22);
}

.feature-row:last-child {
    border-bottom: none;
}

.feature-left {
    display: flex;
    gap: 20px;
    align-items: flex-start;
}

.feature-icon {
    font-size: 42px;
    color: #075c34;
    min-width: 52px;
}

.feature-title {
    font-size: 25px;
    color: #073d25;
    font-weight: 800;
    margin-bottom: 8px;
}

.feature-desc {
    font-size: 17px;
    color: #25362d;
    line-height: 1.45;
}

.action-box {
    background: #eef2df;
    border-radius: 14px;
    padding: 24px 28px;
    font-weight: 800;
    color: #073d25;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1px solid rgba(7,92,52,0.15);
}

.info-card {
    background: rgba(255,255,255,0.96);
    border-radius: 18px;
    padding: 20px 24px;
    border-left: 7px solid #08743b;
    box-shadow: 0px 3px 14px rgba(0,0,0,0.10);
    margin-bottom: 22px;
}

section[data-testid="stFileUploader"] {
    background: white !important;
    padding: 18px !important;
    border-radius: 18px !important;
    border: 2px dashed #cbb98a !important;
}

section[data-testid="stFileUploader"] * {
    color: #1d2b1f !important;
}

section[data-testid="stFileUploader"] button {
    background: #08743b !important;
    color: white !important;
    border-radius: 12px !important;
    border: none !important;
}

section[data-testid="stFileUploader"] button * {
    color: white !important;
}

div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.97) !important;
    border-radius: 18px !important;
    border: 1px solid #d8c9a5 !important;
    overflow: hidden;
    box-shadow: 0px 3px 14px rgba(0,0,0,0.10);
    margin-bottom: 16px;
}

div[data-testid="stExpander"] * {
    color: #1d2b1f !important;
}

h1, h2, h3, h4, p, span, label {
    color: #1d2b1f !important;
}

.footer-card {
    background: rgba(255,250,235,0.96);
    border-radius: 18px;
    padding: 24px;
    margin-top: 22px;
    display: flex;
    align-items: center;
    gap: 18px;
    color: #073d25;
    font-weight: 800;
}

.footer-card small {
    display: block;
    font-weight: 400;
    color: #25362d;
    margin-top: 4px;
}

@media (max-width: 768px) {
    .stApp {
        background-attachment: scroll;
    }

    .hero {
        flex-direction: column;
        text-align: center;
        padding: 26px;
    }

    .divider {
        display: none;
    }

    .logo-img {
        width: 135px;
        height: 135px;
    }

    .hero-text h1 {
        font-size: 34px !important;
    }

    .hero-text h3 {
        font-size: 22px !important;
    }

    .main-card {
        padding: 22px;
    }

    .feature-row {
        grid-template-columns: 1fr;
        gap: 16px;
    }
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="hero">
    <img src="https://github.com/tecnologiacafeeira/procafe-ia/blob/main/assets/logo.png?raw=true" class="logo-img">
    <div class="divider"></div>
    <div class="hero-text">
        <h1>FUNDAÇÃO PROCAFÉ</h1>
        <h3>Diagnóstico Inteligente de Solo</h3>
    </div>
</div>
""", unsafe_allow_html=True)


st.markdown("""
<div class="main-card">
    <div class="feature-row">
        <div class="feature-left">
            <div class="feature-icon">☁️</div>
            <div>
                <div class="feature-title">Upload do Laudo de Análise de Solo (PDF)</div>
                <div class="feature-desc">Envie o arquivo do laboratório para análise automática.</div>
            </div>
        </div>
        <div class="action-box">
            <span>Arraste e solte o arquivo ou clique para selecionar</span>
            <span>PDF</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


arquivo = st.file_uploader(
    "Selecione o laudo em PDF",
    type=["pdf"],
    label_visibility="visible"
)


st.markdown("""
<div class="main-card">
    <div class="feature-row">
        <div class="feature-left">
            <div class="feature-icon">▥</div>
            <div>
                <div class="feature-title">Resultados da Análise</div>
                <div class="feature-desc">Interpretação automática dos principais parâmetros do solo.</div>
            </div>
        </div>
        <div class="action-box">
            <span>☰ VER RESULTADOS</span>
            <span>⌄</span>
        </div>
    </div>

    <div class="feature-row">
        <div class="feature-left">
            <div class="feature-icon">🌿</div>
            <div>
                <div class="feature-title">Recomendações Agronômicas</div>
                <div class="feature-desc">Sugestões personalizadas para melhoria da fertilidade do solo.</div>
            </div>
        </div>
        <div class="action-box">
            <span>🌱 VER RECOMENDAÇÕES</span>
            <span>⌄</span>
        </div>
    </div>

    <div class="feature-row">
        <div class="feature-left">
            <div class="feature-icon">📄</div>
            <div>
                <div class="feature-title">Relatório Técnico</div>
                <div class="feature-desc">Gere um relatório técnico completo com todos os resultados.</div>
            </div>
        </div>
        <div class="action-box">
            <span>📄 GERAR RELATÓRIO PDF</span>
            <span>⌄</span>
        </div>
    </div>
</div>

<div class="footer-card">
    <div style="font-size:42px;">🛡️</div>
    <div>
        Tecnologia e conhecimento a serviço da cafeicultura
        <small>Fundação Procafé – Inovação para uma cafeicultura sustentável</small>
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

            st.markdown("## Informações básicas")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write("**pH H2O:**", item["ph_h2o"], "-", cor_diagnostico(item["diag_ph"]))
                st.write("**pH CaCl2:**", item["ph_cacl2"])

            with col2:
                st.write("**M.O.:**", item["mo"], "-", cor_diagnostico(item["diag_mo"]))
                st.write("**V%:**", item["v_percent"], "-", cor_diagnostico(item["diag_v"]))

            with col3:
                st.write("**Al:**", item["al"], "-", cor_diagnostico(item["diag_al"]))
                st.write("**H + Al:**", item["h_al"], "-", cor_diagnostico(item["diag_h_al"]))

            st.markdown("---")
            st.markdown("## Macronutrientes")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write("**P:**", item["p"], "-", cor_diagnostico(item["diag_p"]))
                st.write("**K:**", item["k"], "-", cor_diagnostico(item["diag_k"]))

            with col2:
                st.write("**Ca:**", item["ca"], "-", cor_diagnostico(item["diag_ca"]))
                st.write("**Mg:**", item["mg"], "-", cor_diagnostico(item["diag_mg"]))

            with col3:
                st.write("**S:**", item["s"], "-", cor_diagnostico(item["diag_s"]))
                st.write("**P-rem:**", item["p_rem"])

            st.markdown("---")
            st.markdown("## Micronutrientes")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write("**Zn:**", item["zn"], "-", cor_diagnostico(item["diag_zn"]))
                st.write("**Fe:**", item["fe"], "-", cor_diagnostico(item["diag_fe"]))

            with col2:
                st.write("**Mn:**", item["mn"], "-", cor_diagnostico(item["diag_mn"]))
                st.write("**Cu:**", item["cu"], "-", cor_diagnostico(item["diag_cu"]))

            with col3:
                st.write("**B:**", item["b"], "-", cor_diagnostico(item["diag_b"]))
                st.write("**T:**", item["t"])

            st.markdown("---")
            st.markdown("## Recomendações")

            recomendacoes = gerar_recomendacoes(item)

            for r in recomendacoes:
                st.write("✅", r)
