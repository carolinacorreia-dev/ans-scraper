"""
src/scraper.py
Web Scraper para a ANS - Versão Aprimorada
"""

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from typing import List, Tuple

class ANSScraper:
    """
    Classe para extração segura dos Anexos I e II da ANS
    """

    BASE_URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'text/html,application/xhtml+xml'
        })
    
    def get_pdf_links(self) -> List[Tuple[str, str]]:
        """
        Extrai links dos PDFs com validação rigorosa
        
        Returns:
            Lista de tuplas (nome_arquivo, url) para cada anexo
        """
        try:
            print("🔍 Conectando ao site da ANS...")
            response = self.session.get(self.BASE_URL, timeout=20)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            pdf_links = []
            anexos_encontrados = set()
            
            print("📄 Analisando documentos...")
            for link in soup.find_all('a', href=True):
                href = link['href']
                text = link.get_text(' ', strip=True)
                
                # Filtra apenas PDFs
                if not href.lower().endswith('.pdf'):
                    continue
                    
                full_url = urljoin(self.BASE_URL, href)
                
                # Identificação robusta do Anexo I
                if ('anexo i' in text.lower() or 'anexo-i' in href.lower()) and 'anexo_i' not in anexos_encontrados:
                    if 'rol' in href.lower():  # Verificação adicional
                        pdf_links.append(('Anexo_I.pdf', full_url))
                        anexos_encontrados.add('anexo_i')
                        print(f"✅ Anexo I confirmado: {full_url}")
                
                # Identificação robusta do Anexo II
                elif ('anexo ii' in text.lower() or 'anexo-ii' in href.lower()) and 'anexo_ii' not in anexos_encontrados:
                    if 'dut' in href.lower():  # Verificação adicional
                        pdf_links.append(('Anexo_II.pdf', full_url))
                        anexos_encontrados.add('anexo_ii')
                        print(f"✅ Anexo II confirmado: {full_url}")
                
                if len(anexos_encontrados) == 2:
                    break
            
            return pdf_links
            
        except Exception as e:
            print(f"❌ Erro durante scraping: {str(e)}")
            return []
