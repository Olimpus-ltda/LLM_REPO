from pathlib import Path
import os
from pathlib import Path
import shutil


def listar_pdfs(pasta="editais"):
    """
    Retorna uma lista com os caminhos completos dos PDFs encontrados.
    """
    # Caminho do script atual
    base_dir = Path(__file__).resolve().parent
    # Sobe um nível e acessa a pasta "editais"
    pasta_pdfs = base_dir.parent / pasta

    if not pasta_pdfs.exists():
        print(f"Pasta não encontrada: {pasta_pdfs}")
        return []

    # Lista todos os PDFs
    arquivos = list(pasta_pdfs.glob("*.pdf"))

    # Retorna caminhos como strings
    return [str(arq) for arq in arquivos]

def mover_para_editais_lidos(caminho_arquivo, pasta_destino="../editais_lidos"):
    """
    Move um arquivo PDF para a pasta 'editais_lidos' que está fora da pasta Program.
    
    :param caminho_arquivo: caminho completo do arquivo PDF a ser movido
    :param pasta_destino: caminho relativo ou absoluto da pasta destino (default: ../editais_lidos)
    :return: caminho final do arquivo movido
    """
    caminho_arquivo = Path(caminho_arquivo).resolve()
    destino = Path(pasta_destino).resolve()
    
    # Cria a pasta destino se não existir
    destino.mkdir(parents=True, exist_ok=True)

    # Caminho final do arquivo
    arquivo_final = destino / caminho_arquivo.name

    # Move o arquivo
    shutil.move(str(caminho_arquivo), str(arquivo_final))

    return arquivo_final