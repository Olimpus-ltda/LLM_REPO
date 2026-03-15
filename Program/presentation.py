import json
import re
import unicodedata



def gerar_nome_arquivo(nome):
    # Remove acentos
    nome = unicodedata.normalize("NFKD", nome)
    nome = nome.encode("ascii", "ignore").decode("ascii")

    # Minúsculo
    nome = nome.lower()

    # Substitui qualquer coisa que não seja letra ou número por _
    nome = re.sub(r"[^a-z0-9]+", "_", nome)

    # Remove _ duplicado
    nome = re.sub(r"_+", "_", nome)

    # Remove _ no início/fim
    nome = nome.strip("_")

    return nome


# as partes do json do llm vem em partes 
# para cada chunk, então devo criar um json 
# juntando todas as informações 

def consolidar_jsons(lista_respostas):
    """
    Recebe lista de strings JSON retornadas pela LLM
    e retorna um único dicionário consolidado.
    """

    # Estrutura base
    final = {
        "nome": "não encontrado",
        "instituicao": "não encontrado",
        "prazo_final": "não encontrado",
        "tipo_bolsa": "não encontrado",
        "publico": "não encontrado",
        "valor": "não encontrado"
    }

    jsons_validos = []

    # 1️⃣ Converter respostas para dict
    for resposta in lista_respostas:
        if not resposta:
            continue

        try:
            dados = json.loads(resposta)
            jsons_validos.append(dados)
        except json.JSONDecodeError:
            print("⚠️ JSON inválido ignorado:")
            print(resposta)
            continue

    # 2️⃣ Consolidar
    for parcial in jsons_validos:
        for chave in final.keys():
            valor_parcial = parcial.get(chave, "não encontrado")

            # Regra de consolidação:
            # Só substitui se o atual for "não encontrado"
            # e o novo tiver informação válida
            if (
                final[chave] == "não encontrado"
                and valor_parcial
                and valor_parcial.lower() != "não encontrado"
            ):
                final[chave] = valor_parcial

    return final



import os
import json
from datetime import datetime


def salvar_json(edital_dict, nome_base=None):
    os.makedirs("data/editais", exist_ok=True)

    # Se não passar nome, cria automático
    if not nome_base:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_base = f"edital_{timestamp}"

    caminho = f"data/editais/{nome_base}.json"

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(edital_dict, f, indent=4, ensure_ascii=False)

    print(f"✅ JSON salvo em: {caminho}")




def generate_html(editais):
    html = """
    <html>
    <head>
        <title>Relatório de Editais</title>
        <style>
            body { font-family: Arial; }
            .card {
                border: 1px solid #ccc;
                padding: 15px;
                margin: 10px;
                border-radius: 8px;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>
        <h1>📄 Relatório de Editais</h1>
    """

    for edital in editais:
        html += f"""
        <div class="card">
            <h2>{edital['nome']}</h2>
            <p><strong>Instituição:</strong> {edital['instituicao']}</p>
            <p><strong>Prazo:</strong> {edital['prazo']}</p>
            <p><strong>Tipo de bolsa:</strong> {edital['tipo_bolsa']}</p>
            <p><strong>Público:</strong> {edital['publico']}</p>
            <p><strong>Valor:</strong> {edital['valor']}</p>
        </div>
        """

    html += "</body></html>"

    with open("relatorio.html", "w", encoding="utf-8") as f:
        f.write(html)