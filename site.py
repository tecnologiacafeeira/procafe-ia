import streamlit as st

from analisador import analisar_pdf


st.set_page_config(
    page_title="Procafé - Diagnóstico Inteligente",
    page_icon="☕",
    layout="wide"
)


def cor_diagnostico(valor):
    if valor == "Baixo":
        return "🔴 Baixo"
    elif valor == "Médio":
        return "🟡 Médio"
    elif valor == "Alto":
        return "🟢 Alto"
    elif valor == "Sem dado":
        return "⚪ Sem dado"
    return valor


st.markdown(
    """
    <style>
    .stApp {
        background-color: #f7f1e3;
    }

    h1, h2, h3 {
        color: #005c32;
        font-family: Arial, sans-serif;
    }

    .hero {
        background: linear-gradient(135deg, #005c32, #0b7a3b);
        padding: 35px;
        border-radius: 28px;
        color: white;
        margin-bottom: 30px;
    }

    .hero h1 {
        color: white;
        font-size: 42px;
        margin-bottom: 10px;
    }

    .hero p {
        font-size: 18px;
        color: #f5f5f5;
    }

    .card-info {
        background-color: white;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 6px solid #005c32;
        box-shadow: 0px 3px 12px rgba(0,0,0,0.08);
    }

    div[data-testid="stExpander"] {
        background-color: white;
        border-radius: 18px;
        border: 1px solid #e2d8c3;
        margin-bottom: 14px;
        box-shadow: 0px 3px 10px rgba(0,0,0,0.06);
    }

    .stButton button {
        background-color: #005c32;
        color: white;
        border-radius: 12px;
        border: none;
        padding: 10px 22px;
    }

    section[data-testid="stFileUploader"] {
        background-color: white;
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #e2d8c3;
    }

    hr {
        border: none;
        height: 1px;
        background-color: #e2d8c3;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="hero">
        <h1>☕ Fundação Procafé</h1>
        <p>Diagnóstico inteligente de análises de solo para cafeicultura</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="card-info">
        Envie o laudo em PDF para análise automática. O sistema irá extrair os dados,
        classificar os nutrientes e apresentar um diagnóstico visual por amostra.
    </div>
    """,
    unsafe_allow_html=True
)

arquivo = st.file_uploader(
    "Selecione o laudo em PDF",
    type=["pdf"]
)

if arquivo is not None:

    with open("laudo_recebido.pdf", "wb") as f:
        f.write(arquivo.read())

    st.success("PDF enviado com sucesso!")

    dados = analisar_pdf("laudo_recebido.pdf")

    st.markdown("## Diagnóstico das Amostras")

    for item in dados:

        with st.expander(f"☕ {item['numero']} - {item['nome']}"):

            st.markdown("### Informações básicas")

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
            st.markdown("### Macronutrientes")

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
            st.markdown("### Micronutrientes")

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