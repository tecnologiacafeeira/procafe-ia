import fitz
import re


def numero(valor):
    if valor is None:
        return None

    valor = str(valor).strip()

    if valor.upper() in ["X.XX", "XXX", "X", "-", ""]:
        return None

    try:
        return float(valor.replace(",", "."))
    except:
        return None


def eh_valor(valor):
    return numero(valor) is not None


def primeiro_valor(lista, padrao="X.XX"):
    for item in lista:
        if eh_valor(item):
            return item
    return padrao


def classificar(valor, baixo_max, medio_max):
    if valor is None:
        return "Sem dado"
    if valor < baixo_max:
        return "Baixo"
    elif valor <= medio_max:
        return "Médio"
    return "Alto"


def interpretar_ph(valor):
    if valor is None:
        return "Sem dado"
    if valor < 5.0:
        return "Baixo"
    elif valor <= 6.0:
        return "Médio"
    return "Alto"


def interpretar_mo(valor): return classificar(valor, 2.0, 4.0)
def interpretar_p(valor): return classificar(valor, 10.0, 20.0)
def interpretar_k(valor): return classificar(valor, 100.0, 160.0)
def interpretar_ca(valor): return classificar(valor, 1.5, 3.0)
def interpretar_mg(valor): return classificar(valor, 0.5, 1.0)
def interpretar_s(valor): return classificar(valor, 5.0, 10.0)
def interpretar_zn(valor): return classificar(valor, 1.0, 2.0)
def interpretar_b(valor): return classificar(valor, 0.5, 1.0)
def interpretar_cu(valor): return classificar(valor, 0.5, 1.0)
def interpretar_fe(valor): return classificar(valor, 20.0, 50.0)
def interpretar_mn(valor): return classificar(valor, 5.0, 20.0)


def interpretar_al(valor):
    if valor is None:
        return "Sem dado"
    if valor <= 0.3:
        return "Baixo"
    elif valor <= 1.0:
        return "Médio"
    return "Alto"


def interpretar_h_al(valor):
    if valor is None:
        return "Sem dado"
    if valor > 4.0:
        return "Baixo"
    elif valor >= 2.0:
        return "Médio"
    return "Alto"


def interpretar_v(valor):
    return classificar(valor, 40.0, 60.0)


def preencher_diagnosticos(item):
    item["diag_ph"] = interpretar_ph(numero(item.get("ph_h2o")))
    item["diag_mo"] = interpretar_mo(numero(item.get("mo")))
    item["diag_p"] = interpretar_p(numero(item.get("p")))
    item["diag_k"] = interpretar_k(numero(item.get("k")))
    item["diag_ca"] = interpretar_ca(numero(item.get("ca")))
    item["diag_mg"] = interpretar_mg(numero(item.get("mg")))
    item["diag_s"] = interpretar_s(numero(item.get("s")))
    item["diag_zn"] = interpretar_zn(numero(item.get("zn")))
    item["diag_fe"] = interpretar_fe(numero(item.get("fe")))
    item["diag_mn"] = interpretar_mn(numero(item.get("mn")))
    item["diag_cu"] = interpretar_cu(numero(item.get("cu")))
    item["diag_b"] = interpretar_b(numero(item.get("b")))
    item["diag_al"] = interpretar_al(numero(item.get("al")))
    item["diag_h_al"] = interpretar_h_al(numero(item.get("h_al")))
    item["diag_v"] = interpretar_v(numero(item.get("v_percent")))


def extrair_texto(pdf_path):
    texto = ""
    doc = fitz.open(pdf_path)

    for pagina in doc:
        texto += pagina.get_text("text") + "\n"

    return texto


def analisar_modelo_antigo(texto_total):
    linhas = [l.strip() for l in texto_total.split("\n") if l.strip()]
    dados = []

    for i, linha in enumerate(linhas):
        if re.match(r"^\d{2}-", linha):
            valores_antes = linhas[max(0, i - 6):i]
            valores_depois = linhas[i + 1:i + 25]

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

    return dados


def analisar_modelo_procafe(texto_total):
    texto = " ".join(texto_total.split())
    dados = []

    padrao = re.compile(
        r"(\d+[,.]\d+)\s+"      # Ca
        r"(\d+[,.]\d+)\s+"      # Al
        r"(\d+[,.]\d+)\s+"      # T
        r"(\d+[,.]\d+)\s+"      # V
        r"(\d{4,5})\s+"         # Amostra
        r"(\d+[,.]\d+)\s+"      # Ca/T
        r"(.+?)\s+"             # Identificação
        r"(\d{1,4})\s+"         # K
        r"(.+?)(?=\s+\d+[,.]\d+\s+\d+[,.]\d+\s+\d+[,.]\d+\s+\d+[,.]\d+\s+\d{4,5}\s+| Ca - Mg| H\+Al| Observação|$)"
    )

    for m in padrao.finditer(texto):
        ca = m.group(1)
        al = m.group(2)
        t = m.group(3)
        v_percent = m.group(4)
        numero_amostra = m.group(5)
        ca_t_percent = m.group(6)
        nome = m.group(7).strip()
        k = m.group(8)
        resto = m.group(9).strip().split()

        if len(resto) < 12:
            continue

        def pega(pos):
            return resto[pos] if pos < len(resto) else "X.XX"

        mg = pega(0)
        h_al = pega(1)
        mg_t_percent = pega(2)
        k_t_percent = pega(3)
        m_percent = pega(4)
        ph_h2o = pega(5)
        ph_cacl2 = pega(6)

        if len(resto) >= 24:
            p_rem = pega(21)
            p = pega(20)
            s = pega(23)

            b = pega(8)
            cu = pega(10)
            mn = pega(12)
            fe = pega(14)
            zn = pega(16)
            mo = pega(18)

        elif len(resto) == 19:
            p_rem = pega(7)
            p = pega(17)
            s = pega(18)

            b = pega(8)
            cu = pega(10)
            mn = pega(11)
            fe = pega(12)
            zn = pega(13)
            mo = pega(15)

        else:
            p_rem = pega(7)
            p = pega(16)
            s = pega(17)

            b = pega(8)
            cu = pega(10)
            mn = pega(11)
            fe = pega(12)
            zn = pega(13)
            mo = pega(14)

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
            "mg": mg,
            "h_al": h_al,
            "mg_t_percent": mg_t_percent,
            "k_t_percent": k_t_percent,
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
            "s": s,
        }

        preencher_diagnosticos(item)
        dados.append(item)

    return dados


def analisar_pdf(pdf_path):
    if pdf_path.split(".")[-1].lower() != "pdf":
        return []

    texto_total = extrair_texto(pdf_path)

    dados = analisar_modelo_antigo(texto_total)
    if dados:
        return dados

    dados = analisar_modelo_procafe(texto_total)
    if dados:
        return dados

    return []


def gerar_recomendacoes(item):
    criticos = []
    atencao = []
    positivos = []

    ph = numero(item.get("ph_h2o"))
    v = numero(item.get("v_percent"))
    mo = numero(item.get("mo"))
    p = numero(item.get("p"))
    k = numero(item.get("k"))
    ca = numero(item.get("ca"))
    mg = numero(item.get("mg"))
    al = numero(item.get("al"))
    h_al = numero(item.get("h_al"))
    zn = numero(item.get("zn"))
    b = numero(item.get("b"))
    cu = numero(item.get("cu"))
    fe = numero(item.get("fe"))
    mn = numero(item.get("mn"))
    s = numero(item.get("s"))

    # ACIDEZ / CALAGEM
    if ph is not None and ph < 5.0:
        criticos.append("pH baixo: solo ácido, com possível limitação ao desenvolvimento radicular do cafeeiro.")

    if v is not None and v < 50:
        criticos.append("Saturação por bases baixa: forte indicativo de necessidade de calagem.")

    if al is not None and al > 0.3:
        criticos.append("Alumínio elevado: pode causar toxidez e reduzir o crescimento das raízes.")

    if ph is not None and v is not None and al is not None:
        if ph < 5.0 and v < 50 and al > 0.3:
            criticos.append("Conjunto pH baixo + V% baixo + alumínio elevado indica prioridade alta para correção da acidez.")

    # MATÉRIA ORGÂNICA
    if mo is not None:
        if mo < 2.0:
            atencao.append("Matéria orgânica baixa: melhorar cobertura do solo, palhada e uso de práticas conservacionistas.")
        elif mo <= 4.0:
            positivos.append("Matéria orgânica em faixa média.")
        else:
            positivos.append("Boa matéria orgânica: manter o manejo conservacionista.")

    # FÓSFORO
    if p is not None:
        if p < 10:
            criticos.append("Fósforo baixo: pode limitar enraizamento, vigor vegetativo e produtividade.")
        elif p <= 20:
            atencao.append("Fósforo em nível médio: acompanhar e ajustar a adubação conforme produtividade esperada.")
        else:
            positivos.append("Fósforo em nível adequado ou alto.")

    # POTÁSSIO
    if k is not None:
        if k < 100:
            criticos.append("Potássio baixo: pode prejudicar enchimento de grãos, resistência e produtividade.")
        elif k <= 160:
            positivos.append("Potássio em faixa adequada/intermediária.")
        else:
            atencao.append("Potássio alto: observar equilíbrio com cálcio e magnésio.")

    # CÁLCIO E MAGNÉSIO
    if ca is not None:
        if ca < 1.5:
            criticos.append("Cálcio baixo: avaliar calagem e equilíbrio de bases.")
        elif ca <= 3.0:
            positivos.append("Cálcio em faixa adequada/intermediária.")
        else:
            atencao.append("Cálcio alto: observar possível desequilíbrio com Mg e K.")

    if mg is not None:
        if mg < 0.5:
            criticos.append("Magnésio baixo: avaliar calcário dolomítico ou fonte de magnésio.")
        elif mg <= 1.0:
            positivos.append("Magnésio em faixa adequada/intermediária.")
        else:
            atencao.append("Magnésio alto: observar equilíbrio com cálcio e potássio.")

    if ca is not None and mg is not None:
        if ca > 3.5 and mg < 0.5:
            atencao.append("Cálcio alto com magnésio baixo: possível desequilíbrio entre bases.")

    # ENXOFRE
    if s is not None:
        if s < 5:
            atencao.append("Enxofre baixo: avaliar fonte sulfurada no manejo de adubação.")
        else:
            positivos.append("Enxofre sem deficiência evidente.")

    # MICRONUTRIENTES
    if zn is not None:
        if zn < 1.0:
            atencao.append("Zinco baixo: pode afetar brotação e desenvolvimento vegetativo.")
        else:
            positivos.append("Zinco sem deficiência evidente.")

    if b is not None:
        if b < 0.5:
            atencao.append("Boro baixo: atenção ao florescimento, pegamento e crescimento dos ramos.")
        else:
            positivos.append("Boro sem deficiência evidente.")

    if cu is not None:
        if cu < 0.5:
            atencao.append("Cobre baixo: avaliar correção considerando histórico de aplicações foliares.")
        else:
            positivos.append("Cobre sem deficiência evidente.")

    if fe is not None:
        if fe < 20:
            atencao.append("Ferro baixo: verificar pH, matéria orgânica e disponibilidade no solo.")
        else:
            positivos.append("Ferro sem deficiência evidente.")

    if mn is not None:
        if mn < 5:
            atencao.append("Manganês baixo: verificar disponibilidade, principalmente em solos com pH elevado.")
        else:
            positivos.append("Manganês sem deficiência evidente.")

    recomendacoes = []

    if criticos:
        recomendacoes.append("🔴 PROBLEMAS CRÍTICOS")
        recomendacoes.extend(criticos)

    if atencao:
        recomendacoes.append("🟡 PONTOS DE ATENÇÃO")
        recomendacoes.extend(atencao)

    if positivos:
        recomendacoes.append("🟢 PONTOS POSITIVOS")
        recomendacoes.extend(positivos)

    if not recomendacoes:
        recomendacoes.append("Não foram identificados alertas principais nesta amostra.")

    recomendacoes.append(
        "Observação: recomendações automáticas iniciais. A dose final de corretivos e fertilizantes deve considerar produtividade esperada, textura do solo, histórico da área e orientação de um engenheiro agrônomo."
    )

    return recomendacoes
