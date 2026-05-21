import streamlit as st
from analisador import analisar_pdf, gerar_recomendacoes
import base64
import os
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


st.set_page_config(
    page_title="Fundação Procafé - Diagnóstico Inteligente",
    page_icon="🌱",
    layout="wide"
)


def carregar_logo_base64(caminho):
    if os.path.exists(caminho):
        with open(caminho, "rb") as img:
            return base64.b64encode(img.read()).decode()
    return ""


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


def gerar_pdf_relatorio(dados):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2,
        leftMargin=2,
        topMargin=0,
        bottomMargin=25
    )

    estilos = getSampleStyleSheet()
    elementos = []

    header_title = ParagraphStyle(
        "header_title",
        textColor=colors.white,
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=20
    )

    header_sub = ParagraphStyle(
        "header_sub",
        textColor=colors.white,
        fontName="Helvetica",
        fontSize=12,
        leading=14
    )

    titulo_verde = ParagraphStyle(
        "titulo_verde",
        parent=estilos["Title"],
        textColor=colors.HexColor("#08743b"),
        alignment=1,
        fontSize=18,
        leading=22
    )

    subtitulo = ParagraphStyle(
        "subtitulo",
        parent=estilos["Heading2"],
        alignment=1,
        fontSize=13,
        leading=16
    )

    logo_path = "assets/logo.png"

    if os.path.exists(logo_path):
        logo_pdf = Image(logo_path, width=78, height=78)
    else:
        logo_pdf = ""

    texto_header = [
        Paragraph("FUNDAÇÃO PROCAFÉ", header_title),
        Paragraph("Diagnóstico Inteligente de Solo", header_sub)
    ]

    header = Table(
        [[logo_pdf, texto_header]],
        colWidths=[95, 470],
        rowHeights=[74]
    )

    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#08743b")),
        ("ALIGN", (0, 0), (0, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))

    elementos.append(header)
    elementos.append(Spacer(1, 2))

    for item in dados:
        titulo_amostra = f"Amostra {item['numero']} - {item['nome']}"

        tabela = [
            [titulo_amostra, "", ""],
            ["Parâmetro", "Valor", "Diagnóstico"],
            ["pH H2O", item["ph_h2o"], item["diag_ph"]],
            ["pH CaCl2", item["ph_cacl2"], ""],
            ["M.O.", item["mo"], item["diag_mo"]],
            ["V%", item["v_percent"], item["diag_v"]],
            ["Al", item["al"], item["diag_al"]],
            ["H + Al", item["h_al"], item["diag_h_al"]],
            ["P", item["p"], item["diag_p"]],
            ["K", item["k"], item["diag_k"]],
            ["Ca", item["ca"], item["diag_ca"]],
            ["Mg", item["mg"], item["diag_mg"]],
            ["S", item["s"], item["diag_s"]],
            ["Zn", item["zn"], item["diag_zn"]],
            ["Fe", item["fe"], item["diag_fe"]],
            ["Mn", item["mn"], item["diag_mn"]],
            ["Cu", item["cu"], item["diag_cu"]],
            ["B", item["b"], item["diag_b"]],
        ]

        table = Table(tabela, colWidths=[140, 120, 180])
        table.setStyle(TableStyle([
            ("SPAN", (0, 0), (-1, 0)),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f7f6f2")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 14),
            ("TOPPADDING", (0, 0), (-1, 0), 10),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
            ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#08743b")),
            ("TEXTCOLOR", (0, 1), (-1, 1), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f7f6f2")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))

        elementos.append(table)
        elementos.append(Spacer(1, 14))

        elementos.append(Paragraph("<b>Recomendações:</b>", estilos["Heading3"]))

        for rec in gerar_recomendacoes(item):
            rec_pdf = (
                rec.replace("🔴", "")
                   .replace("🟡", "")
                   .replace("🟢", "")
                   .replace("✅", "")
                   .strip()
            )

            if "PROBLEMAS CRÍTICOS" in rec_pdf:
                elementos.append(Paragraph("<b>PROBLEMAS CRÍTICOS</b>", estilos["Heading3"]))
            elif "PONTOS DE ATENÇÃO" in rec_pdf:
                elementos.append(Paragraph("<b>PONTOS DE ATENÇÃO</b>", estilos["Heading3"]))
            elif "PONTOS POSITIVOS" in rec_pdf:
                elementos.append(Paragraph("<b>PONTOS POSITIVOS</b>", estilos["Heading3"]))
            else:
                elementos.append(Paragraph(f"- {rec_pdf}", estilos["Normal"]))

        elementos.append(Spacer(1, 22))

        if item != dados[-1]:
            elementos.append(PageBreak())

    rodape = Table(
        [[Paragraph(
        "Observação: As recomendações apresentadas neste relatório são automáticas e possuem caráter orientativo inicial. A definição final de corretivos e fertilizantes deve considerar produtividade esperada, histórico da área, textura do solo, manejo adotado e avaliação de um engenheiro agrônomo responsável.",
        estilos["Normal"]
        )]],
        colWidths=[520]
    )

    rodape.setStyle(TableStyle([
        ("LINEABOVE", (0, 0), (-1, 0), 2, colors.HexColor("#08743b")),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("WORDWRAP", (0, 0), (-1, -1), "LTR"),
    ]))

    elementos.append(rodape)

    doc.build(elementos)
    buffer.seek(0)
    return buffer


logo_base64 = carregar_logo_base64("assets/logo.png")

st.markdown(f"""
<style>
.stApp {{
    background:
        linear-gradient(rgba(245,239,225,0.78), rgba(245,239,225,0.86)),
        url("https://images.unsplash.com/photo-1447933601403-0c6688de566e?q=80&w=1800");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.block-container {{
    max-width: 1180px;
    padding-top: 36px;
}}

.hero {{
    background: linear-gradient(135deg, #064d2c, #08743b);
    border-radius: 26px;
    padding: 34px 48px;
    margin-bottom: 26px;
    box-shadow: 0px 8px 26px rgba(0,0,0,0.28);
    display: flex;
    align-items: center;
    gap: 36px;
}}

.logo-img {{
    width: 155px;
    height: 155px;
    object-fit: contain;
}}

.divider {{
    width: 2px;
    height: 120px;
    background: rgba(255,255,255,0.75);
}}

.hero-text h1 {{
    color: white !important;
    font-size: 50px !important;
    margin: 0;
    letter-spacing: 1px;
}}

.hero-text h3 {{
    color: white !important;
    font-size: 34px !important;
    font-weight: 400;
    margin-top: 8px;
}}

.card {{
    background: rgba(255,250,235,0.96);
    border-radius: 22px;
    padding: 32px;
    box-shadow: 0px 8px 24px rgba(0,0,0,0.18);
    margin-bottom: 26px;
}}

.feature-title {{
    font-size: 25px;
    color: #073d25;
    font-weight: 800;
    margin-bottom: 8px;
}}

.feature-desc {{
    font-size: 17px;
    color: #25362d;
    line-height: 1.45;
}}

section[data-testid="stFileUploader"] {{
    background: #eef2df !important;
    padding: 24px !important;
    border-radius: 14px !important;
    border: 1px solid rgba(7,92,52,0.20) !important;
}}

section[data-testid="stFileUploader"] label {{
    color: #073d25 !important;
    font-weight: 800 !important;
}}

section[data-testid="stFileUploader"] * {{
    color: #1d2b1f !important;
}}

section[data-testid="stFileUploader"] button {{
    background: #08743b !important;
    color: white !important;
    border-radius: 12px !important;
    border: none !important;
}}

section[data-testid="stFileUploader"] button * {{
    color: white !important;
}}

div[data-testid="stDownloadButton"] button {{
    background: #08743b !important;
    color: white !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 14px 22px !important;
    font-weight: 800 !important;
}}

div[data-testid="stExpander"] {{
    background: rgba(255,255,255,0.97) !important;
    border-radius: 18px !important;
    border: 1px solid #d8c9a5 !important;
    overflow: hidden;
    box-shadow: 0px 3px 14px rgba(0,0,0,0.10);
    margin-bottom: 16px;
}}

div[data-testid="stExpander"] * {{
    color: #1d2b1f !important;
}}

h1, h2, h3, h4, p, span, label {{
    color: #1d2b1f !important;
}}

.footer-card {{
    background: rgba(255,250,235,0.96);
    border-radius: 18px;
    padding: 24px;
    margin-top: 22px;
    margin-bottom: 26px;
    display: flex;
    align-items: center;
    gap: 18px;
    color: #073d25;
    font-weight: 800;
}}

.footer-card small {{
    display: block;
    font-weight: 400;
    color: #25362d;
    margin-top: 4px;
}}

@media (max-width: 768px) {{
    .stApp {{
        background-attachment: scroll;
    }}

    .hero {{
        flex-direction: column;
        text-align: center;
        padding: 26px;
    }}

    .divider {{
        display: none;
    }}

    .logo-img {{
        width: 135px;
        height: 135px;
    }}

    .hero-text h1 {{
        font-size: 34px !important;
    }}

    .hero-text h3 {{
        font-size: 22px !important;
    }}

    .card {{
        padding: 22px;
    }}

    .card div[style*="grid-template-columns"] {{
    display: block !important;
    }}
    
    .card div[style*="display:flex"] {{
        display: block !important;
        text-align: center !important;
    }}
    
    .feature-title {{
        font-size: 26px !important;
        text-align: center !important;
    }}
    
    .feature-desc {{
        font-size: 16px !important;
        text-align: center !important;
    }}
    
    .card div[style*="background:#eef2df"] {{
        margin-top: 20px !important;
        display: block !important;
        text-align: center !important;
    }}
    
    .hero {{
        margin-top: 15px !important;
    }}
    
    .hero-text h1 {{
        font-size: 36px !important;
        line-height: 1.15 !important;
    }}
    
    .hero-text h3 {{
        font-size: 22px !important;
    }}
}}
</style>
""", unsafe_allow_html=True)


if logo_base64:
    logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="logo-img">'
else:
    logo_html = '<div style="font-size:80px;">🌱</div>'


st.markdown(f"""
<div class="hero">
    {logo_html}
    <div class="divider"></div>
    <div class="hero-text">
        <h1>FUNDAÇÃO PROCAFÉ</h1>
        <h3>Diagnóstico Inteligente de Solo</h3>
    </div>
</div>
""", unsafe_allow_html=True)


st.markdown("""
<div class="card">
    <div style="display:grid; grid-template-columns:38% 62%; gap:28px; align-items:center;">
        <div style="display:flex; gap:20px; align-items:flex-start;">
            <div style="font-size:42px;">☁️</div>
            <div>
                <div class="feature-title">Upload do Laudo de Análise de Solo (PDF)</div>
                <div class="feature-desc">Envie o arquivo do laboratório para análise automática.</div>
            </div>
        </div>
        <div style="background:#eef2df; border-radius:14px; padding:24px 28px; font-weight:800; color:#073d25; display:flex; justify-content:space-between; align-items:center; border:1px solid rgba(7,92,52,0.20);">
            <span>Use o campo abaixo para arrastar ou selecionar o arquivo</span>
            <span>PDF</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


arquivo = st.file_uploader(
    "Arraste e solte o arquivo aqui ou clique para selecionar",
    type=["pdf"],
    label_visibility="visible"
)


st.markdown("""
<div class="card">
    <div style="display:grid; grid-template-columns:38% 62%; gap:28px; align-items:center; padding:22px 0; border-bottom:1px solid rgba(120,90,40,0.22);">
        <div style="display:flex; gap:20px; align-items:flex-start;">
            <div style="font-size:42px;">▥</div>
            <div>
                <div class="feature-title">Resultados da Análise</div>
                <div class="feature-desc">Interpretação automática dos principais parâmetros do solo.</div>
            </div>
        </div>
        <div style="background:#eef2df; border-radius:14px; padding:24px 28px; font-weight:800; color:#073d25; display:flex; justify-content:space-between;">
            <span>☰ VER RESULTADOS</span>
            <span>⌄</span>
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

    pdf = gerar_pdf_relatorio(dados)

    st.download_button(
        label="📄 Baixar relatório técnico em PDF",
        data=pdf,
        file_name="relatorio_procafe.pdf",
        mime="application/pdf"
    )

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
