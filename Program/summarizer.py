import subprocess
#import json 



# recebe o texto e passa o promprr para o ollama


def consult_llm(prompt, text):
    full_prompt = f"""
    {prompt}

    Texto:
    {text}
    """

    result = subprocess.run(
        ['ollama', 'run', 'llama3'], 
        input=full_prompt,
        text=True,
        capture_output=True
    )

    if result.returncode != 0:
        print("Erro ao chamar LLM:")
        print(result.stderr)
        return None

    return result.stdout


def summarize_text(text):
    prompt = f"""
    Extraia apenas as segintes informações do texto:
    - Nome do edital
    - instituição 
    - prazo final 
    - tipo de bolsa 
    - A que publico destina (graduado, mestrado, doutorado)
    - valor da bolsa

    Se não encontrar, excreva "não encontrado"

    Texto:
    {text}
    """

    result = subprocess.run(
        ["ollama", "run", "llma3"],
        input=prompt,
        text=True,
        capture_output=True
    )

    return result.stdout