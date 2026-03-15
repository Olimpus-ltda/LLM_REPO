---

# 🤖 PDF Analyzer com LLM

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Web-Flask-black)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Groq](https://img.shields.io/badge/LLM-Groq-purple)
![Ollama](https://img.shields.io/badge/LLM-Ollama-darkgreen)
![Status](https://img.shields.io/badge/Status-Open%20Source-success)

---


## 📌 Analisador de PDFs com IA

Aplicação web **open source** que permite upload de múltiplos PDFs, envio de prompt personalizado e processamento via LLM (local ou cloud), armazenando resultados em SQLite e exibindo tudo em uma interface web simples e organizada.

A aplicação permite ler o PDF enviado e gerar resumo, extração estruturada ou qualquer saída dinâmica em JSON com base no prompt escolhido pelo usuário.


## 🧠 Provedores de LLM

- **Groq** → Processamento em nuvem com alta performance.
- **Ollama** → Execução local de modelos open source.

O usuário pode selecionar o provedor diretamente na interface.

---
## 🖼️ Interface

<table width="100%">
  <tr>
    <th width="50%"><h3>📤 Tela de Submissão</h3></th>
    <th width="50%"><h3>📊 Tela de Visualização</h3></th>
  </tr>
  <tr>
    <td valign="top">
      <ul>
        <li>Prompt editável</li>
        <li>Seleção do provedor (Groq ou Ollama)</li>
        <li>Upload múltiplo de PDFs</li>
      </ul>
    </td>
    <td valign="top">
      <ul>
        <li>Lista de PDFs processados</li>
        <li>Prompt utilizado</li>
        <li>JSON formatado</li>
        <li>Data de processamento</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <img src="https://raw.githubusercontent.com/FabioRSJunior/Estudo_llms/main/Projeto%2002%20-%20Sistema%20Groq%20Ollm/Images/submit.png" alt="Tela Submit" width="100%">
    </td>
    <td valign="top">
      <img src="https://raw.githubusercontent.com/FabioRSJunior/Estudo_llms/main/Projeto%2002%20-%20Sistema%20Groq%20Ollm/Images/list.png" alt="Tela Lista" width="100%">
    </td>
  </tr>
</table>
---

## 📂 Estrutura

- `app.py` → Aplicação Flask.
- `database.py` → Criação e manipulação do SQLite.
- `func_pdf.py` → Extração e divisão do texto.
- `llm_groq.py` → Integração com API Groq.
- `llm_ollama.py` → Integração com Ollama local.
- `templates/` → Interfaces HTML.

---

