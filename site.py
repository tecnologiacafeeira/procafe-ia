import streamlit as st
from analisador import analisar_pdf, gerar_recomendacoes

st.set_page_config(
    page_title="Fundação Procafé",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #f3efe3;
}

.titulo {
    background: #06752f;
    padding: 40px;
    border-radius: 25px;
    color: white;
    margin-bottom: 30px;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 20px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
}

h1, h2, h3 {
    color: #1d2b1f;
}

hr {
    margin-top: 30px;
    margin-bottom: 30px;
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
    "Envie o laudo em PDF para análise automática. "
    "O sistema irá extrair os dados, classificar os nutrientes "
    "e apresentar um diagnóstico visual por amostra."
)

arquivo = st.file_uploader(
    "Selecione o laudo em PDF",
    type=["pdf"]
)

def cor_diagnostico(texto):
    if "Baixo" in texto:
        return f"🔴 {texto}"
    elif "Médio" in texto:
        return f"🟡 {texto}"
    elif "Adequado" in texto:
        return f"🟢 {texto}"
    elif "Alto" in texto:
        return f"🟢 {texto}"
    else:
        return f"🟣 {texto}"

if arquivo:

    with open("temp.pdf", "wb") as f:
        f.write(arquivo.read())

    dados = analisar_pdf("temp.pdf")

    st.success("Laudo processado com sucesso!")

    for item in dados:

        with st.expander(f"{item['numero']} - {item['nome']}"):

            st.markdown("## Informações básicas")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(
                    "**pH H2O:**",
                    item["ph_h2o"],
                    "-",
                    cor_diagnostico(item["diag_ph"])
                )

                st.write(
                    "**pH CaCl2:**",
                    item["ph_cacl2"]
                )

            with col2:
                st.write(
                    "**M.O.:**",
                    item["mo"],
                    "-",
                    cor_diagnostico(item["diag_mo"])
                )

                st.write(
                    "**V%:**",
                    item["v_percent"],
                    "-",
                    cor_diagnostico(item["diag_v"])
                )

            with col3:
                st.write(
                    "**Al:**",
                    item["al"],
                    "-",
                    cor_diagnostico(item["diag_al"])
                )

                st.write(
                    "**H + Al:**",
                    item["h_al"],
                    "-",
                    cor_diagnostico(item["diag_h_al"])
                )

            st.markdown("---")

            st.markdown("## Macronutrientes")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(
                    "**P:**",
                    item["p"],
                    "-",
                    cor_diagnostico(item["diag_p"])
                )

                st.write(
                    "**K:**",
                    item["k"],
                    "-",
                    cor_diagnostico(item["diag_k"])
                )

            with col2:
                st.write(
                    "**Ca:**",
                    item["ca"],
                    "-",
                    cor_diagnostico(item["diag_ca"])
                )

                st.write(
                    "**Mg:**",
                    item["mg"],
                    "-",
                    cor_diagnostico(item["diag_mg"])
                )

            with col3:
                st.write(
                    "**S:**",
                    item["s"],
                    "-",
                    cor_diagnostico(item["diag_s"])
                )

                st.write(
                    "**P-rem:**",
                    item["p_rem"]
                )

            st.markdown("---")

            st.markdown("## Micronutrientes")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(
                    "**Zn:**",
                    item["zn"],
                    "-",
                    cor_diagnostico(item["diag_zn"])
                )

                st.write(
                    "**Fe:**",
                    item["fe"],
                    "-",
                    cor_diagnostico(item["diag_fe"])
                )

            with col2:
                st.write(
                    "**Mn:**",
                    item["mn"],
                    "-",
                    cor_diagnostico(item["diag_mn"])
                )

                st.write(
                    "**Cu:**",
                    item["cu"],
                    "-",
                    cor_diagnostico(item["diag_cu"])
                )

            with col3:
                st.write(
                    "**B:**",
                    item["b"],
                    "-",
                    cor_diagnostico(item["diag_b"])
                )

                st.write(
                    "**T:**",
                    item["t"]
                )

            st.markdown("---")

            st.markdown("## Recomendações")

            recomendacoes = gerar_recomendacoes(item)

            for r in recomendacoes:
                st.write("✅", r)
