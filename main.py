from src.scraper import ANSScraper
from src.file_handler import download_files, create_zip, cleanup

def main():
    scraper = ANSScraper()
    pdf_links = scraper.get_pdf_links()
    
    # Após obter os pdf_links
    print("Links encontrados:")
    for name, url in pdf_links:
        print(f"{name}: {url}")
        
    if not pdf_links:
        print("Nenhum PDF encontrado para download.")
        return
    
    downloaded_files = download_files(scraper.session, pdf_links)
    
    if create_zip(downloaded_files):
        cleanup(downloaded_files)
        print("Processo concluído com sucesso!")
    else:
        print("Falha na compactação. Arquivos mantidos em:", downloaded_files)

if __name__ == "__main__":
    main()