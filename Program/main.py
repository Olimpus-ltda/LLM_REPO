import sys
import os
import json
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from Program.func_pdf import extract_pdf_txt, chunk_text
from Program.summarizer import consult_llm, summarize_text
from Program.llm_groq import consult_groq
from Program.presentation import generate_html, consolidar_jsons, salvar_json, gerar_nome_arquivo
from Program.miscelanius import listar_pdfs, mover_para_editais_lidos
from Program.sql_lite import  salvar_json_flexivel


result = [] 
tipo_llm = 0 


def faz_analise_arquivos_diretorios(prompt, tipo_llm=None):
    # retorna uma lista com o caminho 
    # dos pdfs no diretorio Editais.  
    lista_path = listar_pdfs()


    # Para cada caminhos de pdfs
    # faça a consulta no llm 

    for i, pdf_path in enumerate(lista_path, 1):
        print(pdf_path)
        # função que consulta a llm
        txt = extract_pdf_txt(pdf_path)
        chunks = chunk_text(txt) 
        for i, chunk in enumerate(chunks):
            print(f"processando chunk {i+1} / {len(chunks)}")
            if tipo_llm == "ollama" : 
                    resposta = consult_llm(prompt,chunk)
            else : resposta = consult_groq(prompt,chunk) # consulta groc 
             
            result.append(resposta)
        edital_final = consolidar_jsons(result)

        print("\nRESULTADO FINAL CONSOLIDADO:\n")
        print(json.dumps(edital_final, indent=4, ensure_ascii=False))


        nome_base = gerar_nome_arquivo(edital_final["nome"])
        salvar_json(result,nome_base)

         # salva o JSON flexível no SQLite
        salvar_json_flexivel(edital_final, pdf_path, prompt)

        novo_caminho = mover_para_editais_lidos(pdf_path)



#  excuta a analise 
# faz_analise_arquivos_diretorios(prompt)

prompt = """Você é um sistema de extração de dados.
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
