import pytest
from unittest import mock
from src.scraper import ANSScraper
from src.file_handler import download_files, create_zip, cleanup
import main

class TestMain:
    @mock.patch.object(ANSScraper, 'get_pdf_links')
    @mock.patch('main.download_files')
    @mock.patch('main.create_zip')
    @mock.patch('main.cleanup')
    def test_main_success_flow(self, mock_cleanup, mock_create_zip, 
                            mock_download, mock_get_links):
        """Testa o fluxo completo com sucesso"""
        # Configura os mocks
        mock_get_links.return_value = [
            ('Anexo_I.pdf', 'http://exemplo.com/anexo1.pdf'),
            ('Anexo_II.pdf', 'http://exemplo.com/anexo2.pdf')
        ]
        mock_download.return_value = ['/tmp/Anexo_I.pdf', '/tmp/Anexo_II.pdf']
        mock_create_zip.return_value = True

        # Captura a saída impressa
        with mock.patch('builtins.print') as mock_print:
            main.main()

        # Verifica o fluxo
        mock_get_links.assert_called_once()
        mock_download.assert_called_once_with(mock.ANY, mock_get_links.return_value)
        mock_create_zip.assert_called_once_with(mock_download.return_value)
        mock_cleanup.assert_called_once_with(mock_download.return_value)
        
        # Verifica as mensagens de saída
        assert any("Links encontrados:" in str(call) for call in mock_print.call_args_list)
        assert any("Processo concluído com sucesso!" in str(call) for call in mock_print.call_args_list)

    @mock.patch.object(ANSScraper, 'get_pdf_links')
    def test_main_no_files_found(self, mock_get_links):
        """Testa quando nenhum PDF é encontrado"""
        mock_get_links.return_value = []

        with mock.patch('builtins.print') as mock_print:
            main.main()

        mock_print.assert_any_call("Nenhum PDF encontrado para download.")

    @mock.patch.object(ANSScraper, 'get_pdf_links')
    @mock.patch('main.download_files')
    @mock.patch('main.create_zip')
    def test_main_zip_failure(self, mock_create_zip, mock_download, mock_get_links):
        """Testa quando a criação do ZIP falha"""
        mock_get_links.return_value = [('test.pdf', 'http://exemplo.com/test.pdf')]
        mock_download.return_value = ['/tmp/test.pdf']
        mock_create_zip.return_value = False

        with mock.patch('builtins.print') as mock_print:
            main.main()

        mock_print.assert_any_call("Falha na compactação. Arquivos mantidos em:", mock_download.return_value)