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

def preencher_diagnosticos(item):
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


def analisar_pdf(pdf_path):
    texto_total = ""

    if pdf_path.split(".")[-1].lower() != "pdf":
        return []

    doc = fitz.open(pdf_path)

    for pagina in doc:
        texto_total += pagina.get_text("text") + "\n"

    linhas = [
        linha.strip()
        for linha in texto_total.split("\n")
        if linha.strip()
    ]

    dados = []

    # =========================
    # MODELO ANTIGO
    # =========================
    for i, linha in enumerate(linhas):
        if re.match(r"^\d{2}-", linha):

            valores_antes = linhas[max(0, i - 6):i]
            valores_depois = linhas[i + 1:i + 20]

            if len(valores_antes) < 6 or len(valores_depois) < 18:
                continue

            numero_amostra = linha.split("-")[0].strip()
            nome = linha.split("-", 1)[1].strip()

            item = {
                "numero": numero_amostra,
                "nome": nome,
                "amostra_lab": valores_antes[4],
                "h_al": valores_antes[0],
                "al": valores_antes[1],
                "t": valores_antes[2],
                "v_percent": valores_antes[3],
                "mg_t_percent": valores_antes[5],
                "k": valores_depois[0],
                "ca": valores_depois[1],
                "mg": valores_depois[2],
                "s": valores_depois[3],
                "ca_t_percent": valores_depois[4],
                "m_percent": valores_depois[5],
                "ph_h2o": valores_depois[6],
                "ph_cacl2": valores_depois[7],
                "p_rem": valores_depois[8],
                "mo": valores_depois[9],
                "zn": valores_depois[10],
                "fe": valores_depois[11],
                "mn": valores_depois[12],
                "cu": valores_depois[13],
                "b": valores_depois[14],
                "p": valores_depois[17],
            }

            preencher_diagnosticos(item)
            dados.append(item)

    if dados:
        return dados

    # =========================
    # MODELO NOVO PROCafé
    # =========================
    texto = " ".join(texto_total.split())

    padrao_linha = re.compile(
        r"(\d+[,.]\d+)\s+"
        r"(\d+[,.]\d+)\s+"
        r"(\d+[,.]\d+)\s+"
        r"(\d+[,.]\d+)\s+"
        r"(\d{5})\s+"
        r"(\d+[,.]\d+)\s+"
        r"(.+?)\s+"
        r"(\d{2,4})\s+"
        r"(.+?)(?=\s+\d+[,.]\d+\s+\d+[,.]\d+\s+\d+[,.]\d+\s+\d+[,.]\d+\s+\d{5}\s+| Ca - Mg|$)"
    )

    for m in padrao_linha.finditer(texto):
        ca = m.group(1)
        al = m.group(2)
        t = m.group(3)
        v_percent = m.group(4)
        numero_amostra = m.group(5)
        ca_t_percent = m.group(6)
        nome = m.group(7).strip()
        k = m.group(8)
        resto = m.group(9).strip().split()

        if len(resto) < 24:
            continue

        item = {
            "numero": numero_amostra,
            "nome": nome,
            "amostra_lab": numero_amostra,
            "ca": ca,
            "al": al,
            "t": t,
            "v_percent": v_percent,
            "ca_t_percent": ca_t_percent,
            "k": k,
            "mg": resto[0],
            "h_al": resto[1],
            "mg_t_percent": resto[2],
            "m_percent": resto[4],
            "ph_h2o": resto[5],
            "ph_cacl2": resto[6],
            "b": resto[8],
            "cu": resto[10],
            "mn": resto[12],
            "fe": resto[14],
            "zn": resto[16],
            "mo": resto[18],
            "p": resto[20],
            "p_rem": resto[21],
            "s": resto[23],
        }

        preencher_diagnosticos(item)
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
