import os
import zipfile
from datetime import datetime
from .config import OUTPUT_DIR

def download_files(session, pdf_links):
    """Realiza download dos arquivos"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    downloaded_files = []
    
    for filename, url in pdf_links:
        try:
            filepath = os.path.join(OUTPUT_DIR, filename)
            with session.get(url, stream=True, timeout=20) as r:
                r.raise_for_status()
                with open(filepath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            
            if os.path.getsize(filepath) > 0:
                downloaded_files.append(filepath)
        except Exception as e:
            print(f"Erro ao baixar {filename}: {str(e)}")
    
    return downloaded_files

def create_zip(downloaded_files):
    """Cria arquivo ZIP com nomes únicos"""
    if not downloaded_files:
        return False

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"Anexos_ANS_{timestamp}.zip"

    try:
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in downloaded_files:
                if os.path.exists(file):  # Verifica se o arquivo ainda existe
                    # Garante nomes únicos no ZIP
                    arcname = f"{timestamp}_{os.path.basename(file)}"
                    zipf.write(file, arcname)
        
        # Verificação de integridade
        with zipfile.ZipFile(zip_name, 'r') as zipf:
            if zipf.testzip() is None:
                print(f"✓ ZIP criado: {zip_name}")
                return True
        
        os.remove(zip_name)
        return False
        
    except Exception as e:
        print(f"Erro na compactação: {str(e)}")
        if os.path.exists(zip_name):
            os.remove(zip_name)
        return False

def cleanup(downloaded_files):
    """Remove arquivos com verificação robusta"""
    for file in downloaded_files:
        try:
            if os.path.exists(file):  # Só tenta remover se existir
                os.remove(file)
                print(f"Arquivo removido: {file}")
        except Exception as e:
            print(f"⚠️ Erro ao remover {file}: {str(e)}")
    
    # Tenta remover a pasta output se estiver vazia
    try:
        if os.path.exists(OUTPUT_DIR) and not os.listdir(OUTPUT_DIR):
            os.rmdir(OUTPUT_DIR)
    except Exception as e:
        print(f"⚠️ Não foi possível remover {OUTPUT_DIR}: {str(e)}")