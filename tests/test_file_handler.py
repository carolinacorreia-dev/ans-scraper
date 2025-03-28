import os
import zipfile
from unittest import TestCase, mock
from datetime import datetime
from src.file_handler import download_files, create_zip, cleanup
from src.config import OUTPUT_DIR

class TestFileHandler(TestCase):
    def setUp(self):
        # Configuração inicial para os testes
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        
        # Arquivo de teste simulado
        self.test_file = os.path.join(OUTPUT_DIR, "test_file.pdf")
        with open(self.test_file, 'wb') as f:
            f.write(b"Test content")

    def tearDown(self):
        # Limpeza após cada teste
        if os.path.exists(OUTPUT_DIR):
            for file in os.listdir(OUTPUT_DIR):
                os.remove(os.path.join(OUTPUT_DIR, file))
            os.rmdir(OUTPUT_DIR)
        
        # Remove arquivos ZIP criados nos testes
        for file in os.listdir('.'):
            if file.startswith("Anexos_ANS_") and file.endswith(".zip"):
                os.remove(file)

    @mock.patch('requests.Session')
    def test_download_files_success(self, mock_session):
        """Testa download bem-sucedido de arquivos"""
        # Configuração mais completa do mock
        mock_response = mock.Mock()
        mock_response.iter_content.return_value = [b"content"]
        mock_response.raise_for_status.return_value = None
        mock_response.status_code = 200
        
        mock_session.return_value.get.return_value.__enter__.return_value = mock_response
        
        pdf_links = [("file1.pdf", "http://example.com/file1.pdf")]
        result = download_files(mock_session.return_value, pdf_links)
        
        # Verifica se o arquivo foi criado
        downloaded_file = os.path.join(OUTPUT_DIR, "file1.pdf")
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0].endswith("file1.pdf"))
        self.assertTrue(os.path.exists(downloaded_file))
        
        # Limpeza
        if os.path.exists(downloaded_file):
            os.remove(downloaded_file)

    @mock.patch('requests.Session')
    def test_download_files_failure(self, mock_session):
        """Testa falha no download de arquivos"""
        mock_session.return_value.get.side_effect = Exception("Error")
        
        pdf_links = [("file1.pdf", "http://example.com/file1.pdf")]
        result = download_files(mock_session.return_value, pdf_links)
        
        self.assertEqual(len(result), 0)

    def test_create_zip_success(self):
        """Testa criação bem-sucedida de arquivo ZIP"""
        files = [self.test_file]
        result = create_zip(files)
        
        self.assertTrue(result)
        
        # Verifica se o ZIP contém o arquivo
        zip_files = [f for f in os.listdir('.') if f.startswith("Anexos_ANS_")]
        self.assertEqual(len(zip_files), 1)
        
        with zipfile.ZipFile(zip_files[0], 'r') as zipf:
            self.assertEqual(len(zipf.namelist()), 1)

    def test_create_zip_empty_list(self):
        """Testa criação de ZIP com lista vazia"""
        result = create_zip([])
        self.assertFalse(result)

    def test_create_zip_integrity_failure(self):
        """Testa falha na verificação de integridade do ZIP"""
        with mock.patch('zipfile.ZipFile.testzip', return_value="error"):
            result = create_zip([self.test_file])
            self.assertFalse(result)

    def test_cleanup(self):
        """Testa limpeza dos arquivos temporários"""
        files = [self.test_file]
        cleanup(files)
        
        self.assertFalse(os.path.exists(self.test_file))
        self.assertFalse(os.path.exists(OUTPUT_DIR))