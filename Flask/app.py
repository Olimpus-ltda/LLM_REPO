import sys
import os
import json

# Adiciona o diretório pai ao sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

# Agora você consegue importar
from Program.main import faz_analise_arquivos_diretorios
from Program.sql_lite import criar_tabela_flexivel
from Program.sql_lite import listar_editais

from flask import Flask, request, render_template, redirect, flash
from werkzeug.utils import secure_filename

#from Program/main.py import az_analise_arquivos_diretorios 

# --- Configuração Flask ---
app = Flask(__name__)
app.secret_key = "supersecretkey"  # em produção use variável de ambiente

criar_tabela_flexivel()


# --- Pasta de uploads fora da pasta Flask ---
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "editais")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"] = {"pdf"}
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB

# --- Função para validar PDF ---
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

# --- Rota principal ---
@app.route("/", methods=["GET"])
def index():
    default_prompt = """Você é um sistema de extração de dados.
            Extraia as seguintes informações do texto.
            Responda apenas em JSON válido neste formato:

            {
            "nome": "",
            "instituicao": "",
            "prazo_final": "",
            "tipo_bolsa": "",
            "publico": "",
            "valor": ""
            }

            Se não encontrar, use "não encontrado".
            Não escreva nada além do JSON. """
    
    return render_template("submit.html", default_prompt=default_prompt)

# --- Rota de submissão ---
@app.route("/submit", methods=["POST"])
def submit():
    prompt = request.form.get("prompt")
    provider = request.form.get("provider")

    if provider not in ["ollama", "groq"]:
        flash("Provedor inválido.")
        return redirect("/")

    if "files" not in request.files:
        flash("Nenhum arquivo enviado.")
        return redirect("/")

    files = request.files.getlist("files")
    saved_files = []

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            saved_files.append(filename)

    if not saved_files:
        flash("Nenhum PDF válido enviado.")
        return redirect("/")

    faz_analise_arquivos_diretorios(prompt,provider) # chama o program e faz a analise.  

    return f"""
    Arquivos salvos: {saved_files} <br>
    Provedor escolhido: {provider} <br>
    Prompt recebido: <pre>{prompt}</pre>
    """

@app.route("/ver")
def ler_editais():
    editais = listar_editais()

    # Formata o JSON de cada edital para exibição
    for e in editais:
        e["conteudo_formatado"] = json.dumps(e["conteudo_json"], indent=4, ensure_ascii=False)
        

    return render_template("lista_editais.html", editais=editais)


# --- Executa o app ---
if __name__ == "__main__":
    app.run(debug=True)