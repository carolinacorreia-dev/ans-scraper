import pytest
from unittest import mock
from bs4 import BeautifulSoup
import requests  # Adicionado import faltante
from src.scraper import ANSScraper

class TestANSScraper:
    @pytest.fixture
    def mock_response(self):
        """Fixture para mock de resposta HTTP"""
        mock_resp = mock.Mock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.status_code = 200
        return mock_resp

    @pytest.fixture
    def html_with_pdf_links(self):
        """HTML de exemplo com links para PDFs"""
        return """
        <html>
            <body>
                <a href="/Anexo_I.pdf">Anexo I - Rol de Procedimentos</a>
                <a href="/Anexo_II.pdf">Anexo II - Diretrizes de Utilização</a>
                <a href="/outro.pdf">Documento não relevante</a>
            </body>
        </html>
        """

    def test_init_sets_proper_headers(self):
        """Testa se o inicializador configura os headers corretamente"""
        scraper = ANSScraper()
        assert 'User-Agent' in scraper.session.headers
        assert 'Mozilla/5.0' in scraper.session.headers['User-Agent']
        assert 'Accept' in scraper.session.headers

    @mock.patch('requests.Session.get')
    def test_get_pdf_links_success(self, mock_get, mock_response, html_with_pdf_links):
        """Testa extração bem-sucedida de links PDF"""
        # Configura o mock com HTML que atende aos critérios
        mock_response.text = """
        <html>
            <body>
                <a href="/Anexo_I_rol.pdf">Anexo I - Rol de Procedimentos</a>
                <a href="/Anexo_II_dut.pdf">Anexo II - Diretrizes de Utilização</a>
                <a href="/outro.pdf">Documento não relevante</a>
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        scraper = ANSScraper()
        result = scraper.get_pdf_links()

        # Debug: mostra o que foi encontrado
        print("Links encontrados:", result)
        
        # Verifica os resultados
        assert len(result) == 2
        filenames = [filename for filename, url in result]
        assert 'Anexo_I.pdf' in filenames
        assert 'Anexo_II.pdf' in filenames

    @mock.patch('requests.Session.get')
    def test_get_pdf_links_with_empty_response(self, mock_get, mock_response):
        """Testa comportamento com HTML vazio"""
        mock_response.text = "<html></html>"
        mock_get.return_value = mock_response

        scraper = ANSScraper()
        result = scraper.get_pdf_links()

        assert len(result) == 0

    @mock.patch('requests.Session.get')
    def test_get_pdf_links_with_http_error(self, mock_get):
        """Testa comportamento com erro HTTP"""
        mock_get.side_effect = requests.exceptions.HTTPError("404 Not Found")

        scraper = ANSScraper()
        result = scraper.get_pdf_links()

        assert len(result) == 0

    @mock.patch('requests.Session.get')
    def test_get_pdf_links_with_connection_error(self, mock_get):
        """Testa comportamento com erro de conexão"""
        mock_get.side_effect = requests.exceptions.ConnectionError()

        scraper = ANSScraper()
        result = scraper.get_pdf_links()

        assert len(result) == 0

    @mock.patch('requests.Session.get')
    def test_get_pdf_links_with_timeout(self, mock_get):
        """Testa comportamento com timeout"""
        mock_get.side_effect = requests.exceptions.Timeout()

        scraper = ANSScraper()
        result = scraper.get_pdf_links()

        assert len(result) == 0

    @mock.patch('requests.Session.get')
    def test_get_pdf_links_with_invalid_pdfs(self, mock_get, mock_response):
        """Testa filtragem de PDFs inválidos"""
        mock_response.text = """
        <html>
            <a href="/not_a_pdf.txt">Arquivo texto</a>
            <a href="/invalid.pdf">PDF sem anexo</a>
        </html>
        """
        mock_get.return_value = mock_response

        scraper = ANSScraper()
        result = scraper.get_pdf_links()

        assert len(result) == 0