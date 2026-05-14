import streamlit as st
from analisador import analisar_pdf, gerar_recomendacoes

st.set_page_config(
    page_title="Fundação Procafé",
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
.stApp {
    background-color: #f3efe3;
    color: #1d2b1f;
}

.titulo {
    background: #06752f;
    padding: 40px;
    border-radius: 25px;
    color: white;
    margin-bottom: 30px;
}

.titulo h1, .titulo h3 {
    color: white !important;
}

h1, h2, h3, h4, p, span, div, label {
    color: #1d2b1f !important;
}

div[data-testid="stExpander"] {
    background-color: white !important;
    color: #1d2b1f !important;
    border-radius: 14px;
    border: 1px solid #ddd;
}

div[data-testid="stExpander"] * {
    color: #1d2b1f !important;
}

.streamlit-expanderHeader {
    background-color: #ffffff !important;
    color: #1d2b1f !important;
}

hr {
    margin-top: 25px;
    margin-bottom: 25px;
}

@media (max-width: 768px) {
    .titulo {
        padding: 25px;
        border-radius: 18px;
    }

    .titulo h1 {
        font-size: 30px !important;
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
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="titulo">
<h1>☕ Fundação Procafé</h1>
<h3>Diagnóstico inteligente de análises de solo para cafeicultura</h3>
</div>
""", unsafe_allow_html=True)

st.info(
    "Envie o laudo em PDF ou imagem para análise automática. "
    "O sistema irá extrair os dados, classificar os nutrientes "
    "e apresentar um diagnóstico visual por amostra."
)

arquivo = st.file_uploader(
    "Selecione o laudo em PDF ou imagem",
    type=["pdf", "png", "jpg", "jpeg"]
)

if arquivo is not None:

    extensao = arquivo.name.split(".")[-1].lower()
    caminho_arquivo = f"temp.{extensao}"

    with open(caminho_arquivo, "wb") as f:
        f.write(arquivo.read())

    dados = analisar_pdf(caminho_arquivo)

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
