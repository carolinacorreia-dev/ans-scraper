# **📂 TESTE DE WEB SCRAPING**  

**Projeto de automação para download e compactação dos Anexos I e II do Rol de Procedimentos da ANS**  

---

## **📌 Visão Geral**  
Este projeto automatiza o download dos **Anexos I e II** (em PDF) do site da [Agência Nacional de Saúde Suplementar (ANS)](https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos) e os compacta em um único arquivo ZIP.  

**Funcionalidades principais**:  
✔ **Web scraping** com `requests` e `BeautifulSoup`  
✔ **Download seguro** dos PDFs com verificação de integridade  
✔ **Compactação automática** em ZIP com timestamp  
✔ **Tratamento de erros** robusto  
✔ **Estrutura modularizada** (pronta para escalar)  

---

## **⚙️ Configuração**  

### **Pré-requisitos**  
- Python 3.8+  
- Pip (gerenciador de pacotes)  

### **Instalação**  
1. Clone o repositório:  
   ```bash
   git clone https://github.com/carolinacorreia-dev/ans-scraper.git
   cd ans-web-scraper
   ```  

2. Instale as dependências:  
   ```bash
   pip install -r requirements.txt
   ```  

---

## **🚀 Como Usar**  
Execute o script principal:  
```bash
python main.py
```  

### **Saída Esperada**  
1. O script acessa o site da ANS.  
2. Baixa os Anexos I e II em `output/`.  
3. Gera um arquivo `Anexos_ANS_<TIMESTAMP>.zip`.  
4. Remove os arquivos temporários (opcional).  

Exemplo:  
```
🔍 Conectando ao site da ANS...
📄 Analisando documentos...
✅ Anexo I confirmado: https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf
✅ Anexo II confirmado: https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf

Links encontrados:
Anexo_I.pdf: [URL completa do Anexo I]
Anexo_II.pdf: [URL completa do Anexo II]

✓ ZIP criado: Anexos_ANS_[DATA_HORA].zip
Arquivo removido: output/Anexo_I.pdf
Arquivo removido: output/Anexo_II.pdf
Processo concluído com sucesso!  
```  

---

## **📂 Estrutura do Projeto**  
```
ans_scraper/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── file_handler.py
│   └── scraper.py
├── tests/
│   ├── __init__.py
│   ├── test_file_handler.py
│   └── test_scraper.py
├── output/
├── main.py
├── README.md 
└── requirements.txt
```  

---

## **🧪 Testes**  
Para executar os testes unitários:  
```bash
python -m pytest tests/
```  

---

**Desenvolvido por Carolina Correia**  
📧 **Contato**: carolinacorreia.dev@gmail.com  

--- 
