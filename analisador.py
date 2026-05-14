import fitz
import re


def numero(valor):
    if valor in ["X.XX", "XXX", "xxx", "x.xx"]:
        return None

    return float(valor.replace(",", "."))


def classificar(valor, baixo_max, medio_max):
    if valor is None:
        return "Sem dado"

    if valor < baixo_max:
        return "Baixo"
    elif valor <= medio_max:
        return "Médio"
    else:
        return "Alto"


def interpretar_ph(valor):
    if valor is None:
        return "Sem dado"

    if valor < 5.0:
        return "Baixo"
    elif valor <= 6.0:
        return "Médio"
    else:
        return "Alto"


def interpretar_mo(valor):
    return classificar(valor, 2.0, 4.0)


def interpretar_p(valor):
    return classificar(valor, 10.0, 20.0)


def interpretar_k(valor):
    return classificar(valor, 100.0, 160.0)


def interpretar_ca(valor):
    return classificar(valor, 1.5, 3.0)


def interpretar_mg(valor):
    return classificar(valor, 0.5, 1.0)


def interpretar_s(valor):
    return classificar(valor, 5.0, 10.0)


def interpretar_zn(valor):
    return classificar(valor, 1.0, 2.0)


def interpretar_b(valor):
    return classificar(valor, 0.5, 1.0)


def interpretar_cu(valor):
    return classificar(valor, 0.5, 1.0)


def interpretar_fe(valor):
    return classificar(valor, 20.0, 50.0)


def interpretar_mn(valor):
    return classificar(valor, 5.0, 20.0)


def interpretar_al(valor):
    if valor is None:
        return "Sem dado"

    if valor <= 0.3:
        return "Baixo"
    elif valor <= 1.0:
        return "Médio"
    else:
        return "Alto"


def interpretar_h_al(valor):
    if valor is None:
        return "Sem dado"

    if valor > 4.0:
        return "Baixo"
    elif valor >= 2.0:
        return "Médio"
    else:
        return "Alto"


def interpretar_v(valor):
    return classificar(valor, 40.0, 60.0)


def analisar_pdf(pdf_path):
    texto_total = ""

    if pdf_path.split(".")[-1].lower() != "pdf":
        return []

    doc = fitz.open(pdf_path)

    for pagina in doc:
        texto_total += pagina.get_text("text") + "\n"

    texto_total = " ".join(texto_total.split())

    dados = []

    padrao = re.compile(
        r"(\d+[,.]\d+)\s+"      # Ca
        r"(\d+[,.]\d+)\s+"      # Al
        r"(\d+[,.]\d+)\s+"      # T
        r"(\d+[,.]\d+)\s+"      # V
        r"(\d{5})\s+"           # Amostra
        r"(\d+[,.]\d+)\s+"      # Ca/T
        r"(.+?)\s+"             # Identificação
        r"(\d{2,4})\s+"         # K
        r"(\d+[,.]\d+)\s+"      # Mg
        r"(\d+[,.]\d+)\s+"      # H+Al
        r"(\d+[,.]\d+)\s+"      # Mg/T
        r"(\d+[,.]\d+)\s+"      # K/T
        r"(\d+[,.]\d+)\s+"      # m
        r"(\d+[,.]\d+)\s+"      # pH H2O
        r"(\d+[,.]\d+)\s+"
        r"(?:X\.XX|\d+[,.]\d+)\s+"
        r"(\d+[,.]\d+|X\.XX)\s+"
        r"(?:X\.XX|\d+[,.]\d+)\s+"
        r"(\d+[,.]\d+|X\.XX)\s+"
        r"(\d+[,.]\d+|X\.XX)\s+"
        r"(?:X\.XX|\d+[,.]\d+)\s+"
        r"(\d+[,.]\d+|X\.XX)\s+"
        r"(?:X\.XX|\d+[,.]\d+)\s+"
        r"(?:X\.XX|\d+[,.]\d+)\s+"
        r"(\d+[,.]\d+|X\.XX)\s+"
        r"(\d+[,.]\d+|X\.XX)\s+"
        r"(?:X\.XX|\d+[,.]\d+)\s+"
        r"(?:X\.XX|\d+[,.]\d+)\s+"
        r"(\d+[,.]\d+|X\.XX)\s+"
        r"(\d+[,.]\d+|X\.XX)\s+"
        r"(\d+[,.]\d+|X\.XX)"
    )

    for m in padrao.finditer(texto_total):
        (
            ca, al, t, v_percent,
            numero_amostra, ca_t_percent, nome,
            k, mg, h_al, mg_t_percent, k_t_percent, m_percent,
            ph_h2o, ph_cacl2,
            b, cu, mn, fe, zn, mo, p, p_rem, s
        ) = m.groups()

        item = {
            "numero": numero_amostra,
            "nome": nome.strip(),
            "amostra_lab": numero_amostra,
            "h_al": h_al,
            "al": al,
            "t": t,
            "v_percent": v_percent,
            "mg_t_percent": mg_t_percent,
            "k": k,
            "ca": ca,
            "mg": mg,
            "s": s,
            "ca_t_percent": ca_t_percent,
            "m_percent": m_percent,
            "ph_h2o": ph_h2o,
            "ph_cacl2": ph_cacl2,
            "p_rem": p_rem,
            "mo": mo,
            "zn": zn,
            "fe": fe,
            "mn": mn,
            "cu": cu,
            "b": b,
            "p": p,
        }

        item["diag_ph"] = interpretar_ph(numero(item["ph_h2o"]))
        item["diag_mo"] = interpretar_mo(numero(item["mo"]))
        item["diag_p"] = interpretar_p(numero(item["p"]))
        item["diag_k"] = interpretar_k(numero(item["k"]))
        item["diag_ca"] = interpretar_ca(numero(item["ca"]))
        item["diag_mg"] = interpretar_mg(numero(item["mg"]))
        item["diag_s"] = interpretar_s(numero(item["s"]))
        item["diag_zn"] = interpretar_zn(numero(item["zn"]))
        item["diag_fe"] = interpretar_fe(numero(item["fe"]))
        item["diag_mn"] = interpretar_mn(numero(item["mn"]))
        item["diag_cu"] = interpretar_cu(numero(item["cu"]))
        item["diag_b"] = interpretar_b(numero(item["b"]))
        item["diag_al"] = interpretar_al(numero(item["al"]))
        item["diag_h_al"] = interpretar_h_al(numero(item["h_al"]))
        item["diag_v"] = interpretar_v(numero(item["v_percent"]))

        dados.append(item)

    return dados


def gerar_recomendacoes(item):
    recomendacoes = []

    if item["diag_p"] == "Baixo":
        recomendacoes.append("Necessidade de correção fosfatada.")

    if item["diag_k"] == "Baixo":
        recomendacoes.append("Potássio abaixo do ideal.")

    if item["diag_ca"] == "Baixo":
        recomendacoes.append("Cálcio baixo. Avaliar calagem.")

    if item["diag_mg"] == "Baixo":
        recomendacoes.append("Magnésio baixo.")

    if item["diag_v"] == "Baixo":
        recomendacoes.append("Saturação por bases baixa. Possível necessidade de calagem.")

    if item["diag_al"] == "Alto":
        recomendacoes.append("Alumínio elevado com possível risco de toxidez.")

    if len(recomendacoes) == 0:
        recomendacoes.append("Solo equilibrado nos principais parâmetros.")

    return recomendacoes
