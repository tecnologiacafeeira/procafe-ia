import streamlit as st
from analisador import analisar_pdf, gerar_recomendacoes

st.set_page_config(
    page_title="Fundação Procafé - Diagnóstico Inteligente",
    page_icon="☕",
    layout="wide"
)


def cor_diagnostico(texto):
    if "Baixo" in texto:
        return f"🔴 {texto}"
    elif "Médio" in texto:
        return f"🟡 {texto}"
    elif "Alto" in texto:
        return f"🟢 {texto}"
    elif "Sem dado" in texto:
        return f"⚪ {texto}"
    return texto


st.markdown("""
<style>

/* Upload area corrigida */
section[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.96) !important;
    padding: 20px !important;
    border-radius: 18px !important;
    border: 2px dashed #cbb98a !important;
}

/* Caixa interna */
section[data-testid="stFileUploader"] > div {
    background: white !important;
    color: #1d2b1f !important;
}

/* Botão */
section[data-testid="stFileUploader"] button {
    background: #08743b !important;
    color: white !important;
    border-radius: 12px !important;
    border: none !important;
}

/* Texto do botão */
section[data-testid="stFileUploader"] button p {
    color: white !important;
    font-weight: bold !important;
}

/* Troca Upload por Carregar */
section[data-testid="stFileUploader"] button p::after {
    content: "Carregar";
    font-size: 16px;
}

section[data-testid="stFileUploader"] button p {
    font-size: 0 !important;
}

.stApp {
    background:
        linear-gradient(rgba(245, 239, 225, 0.88), rgba(245, 239, 225, 0.92)),
        url("https://images.unsplash.com/photo-1447933601403-0c6688de566e?q=80&w=1600");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.hero {
    background: linear-gradient(135deg, #064d2c, #08743b);
    border-radius: 28px;
    padding: 36px;
    margin-bottom: 28px;
    box-shadow: 0px 5px 22px rgba(0,0,0,0.25);
}

.hero-content {
    display: flex;
    align-items: center;
    gap: 28px;
}

.logo-circle {
    width: 115px;
    height: 115px;
    border-radius: 50%;
    border: 5px solid white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 54px;
    background: rgba(255,255,255,0.10);
}

.hero h1 {
    color: white !important;
    font-size: 48px !important;
    margin: 0;
    letter-spacing: 1px;
}

.hero h3 {
    color: #eef7ed !important;
    font-weight: 400;
    margin-top: 8px;
}

.info-card {
    background: rgba(255,255,255,0.95);
    border-radius: 22px;
    padding: 22px;
    margin-bottom: 24px;
    border-left: 7px solid #08743b;
    box-shadow: 0px 3px 14px rgba(0,0,0,0.10);
    font-size: 17px;
    color: #1d2b1f !important;
}

.upload-card {
    background: rgba(255,255,255,0.96);
    border-radius: 22px;
    padding: 24px;
    margin-bottom: 28px;
    border: 1px solid #d8c9a5;
    box-shadow: 0px 3px 14px rgba(0,0,0,0.10);
}

section[data-testid="stFileUploader"] {
    background: #f7f6f2;
    padding: 18px;
    border-radius: 18px;
    border: 2px dashed #cbb98a;
}

div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.97) !important;
    border-radius: 18px !important;
    border: 1px solid #d8c9a5 !important;
    overflow: hidden;
    box-shadow: 0px 3px 14px rgba(0,0,0,0.10);
    margin-bottom: 16px;
}

.streamlit-expanderHeader {
    background: #0b1320 !important;
    color: white !important;
    font-size: 22px !important;
    padding: 18px !important;
}

div[data-testid="stExpander"] * {
    color: #1d2b1f !important;
}

h1, h2, h3, h4, p, span, label {
    color: #1d2b1f !important;
}

hr {
    margin-top: 28px;
    margin-bottom: 28px;
}

div[data-testid="stAlert"] {
    background: rgba(255,255,255,0.96);
    border-radius: 18px;
}

@media (max-width: 768px) {
    .stApp {
        background-attachment: scroll;
    }

    .hero {
        padding: 25px;
        border-radius: 20px;
    }

    .hero-content {
        flex-direction: column;
        text-align: center;
    }

    .logo-circle {
    width: 170px;
    height: 170px;
    border-radius: 50%;
    background: rgba(255,255,255,0.10);
    border: 4px solid white;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}
        width: 88px;
        height: 88px;
        font-size: 42px;
    }

    .logo-img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    transform: scale(2.5);
    position: relative;
    top: 5px;
}

    .hero h1 {
        font-size: 32px !important;
    }

    .hero h3 {
        font-size: 18px !important;
    }

    h1 {
        font-size: 30px !important;
    }

    h2 {
        font-size: 24px !important;
    }

    h3 {
        font-size: 20px !important;
    }
}
/* CORREÇÃO FINAL DO UPLOADER NO CELULAR */
section[data-testid="stFileUploader"] {
    background: #ffffff !important;
    color: #1d2b1f !important;
    padding: 18px !important;
    border-radius: 18px !important;
    border: 2px dashed #cbb98a !important;
}

section[data-testid="stFileUploader"] * {
    color: #1d2b1f !important;
}

section[data-testid="stFileUploader"] button {
    background: #08743b !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
}

section[data-testid="stFileUploader"] button * {
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="hero">
    <div class="hero-content">
        <div class="logo-circle">
    <img src="https://github.com/tecnologiacafeeira/procafe-ia/blob/main/assets/logo.png?raw=true" class="logo-img">
</div>
        <div>
            <h1>FUNDAÇÃO PROCAFÉ</h1>
            <h3>Diagnóstico Inteligente de Solo</h3>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


st.markdown("""
<div class="info-card">
    <p style="color:#1d2b1f !important; margin:0;">
        Envie o laudo em PDF para análise automática. O sistema irá extrair os dados,
        classificar os nutrientes e apresentar um diagnóstico visual por amostra,
        com recomendações técnicas iniciais.
    </p>
</div>
""", unsafe_allow_html=True)



st.markdown("## Upload do Laudo de Análise")

arquivo = st.file_uploader(
    "Selecione o laudo em PDF",
    type=["pdf"],
    label_visibility="visible"
)



if arquivo is not None:

    with open("temp.pdf", "wb") as f:
        f.write(arquivo.read())

    dados = analisar_pdf("temp.pdf")

    st.success("Laudo processado com sucesso!")

    st.markdown("## Diagnóstico das Amostras")

    for item in dados:

        with st.expander(f"☕ {item['numero']} - {item['nome']}"):

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
