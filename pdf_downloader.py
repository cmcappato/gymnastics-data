import requests  # Librería para hacer solicitudes HTTP
import time  # Para agregar pausas entre descargas
from bs4 import BeautifulSoup  # Para analizar el contenido HTML de la página
import os  # Para manejar directorios y archivos

# URL de la página donde se encuentran los archivos PDF
base_url = ""

# Carpeta donde se guardarán los archivos descargados
output_folder = ""
os.makedirs(output_folder, exist_ok=True)  # Crea la carpeta si no existe

# Encabezado HTTP para evitar bloqueos por parte del servidor
headers = {"User-Agent": "Mozilla/5.0"}

def get_pdf_links(url):
    """Obtiene los enlaces de todos los archivos PDF en la página dada."""

    # Realiza una solicitud HTTP a la página
    response = requests.get(url, headers=headers)
    
    # Analiza el contenido HTML de la respuesta
    soup = BeautifulSoup(response.text, "html.parser")

    pdf_links = []  # Lista para almacenar los enlaces de los PDFs

    # Busca todos los enlaces en la página
    for link in soup.find_all("a", href=True):
        href = link["href"]  # Obtiene el atributo href del enlace
        
        # Verifica si el enlace termina en ".pdf"
        if href.endswith(".pdf"):  
            # Si el enlace es relativo, lo concatena con la URL base
            full_url = url + href if not href.startswith("http") else href
            pdf_links.append(full_url)  # Agrega el enlace a la lista

    return pdf_links  # Retorna la lista de enlaces a PDFs

def download_pdfs(pdf_links):
    """Descarga los archivos PDF de la lista de enlaces proporcionada."""

    for pdf_url in pdf_links:
        pdf_name = pdf_url.split("/")[-1]  # Extrae el nombre del archivo desde la URL
        pdf_path = os.path.join(output_folder, pdf_name)  # Define la ruta completa del archivo

        # Descarga el archivo PDF en fragmentos para evitar errores
        with requests.get(pdf_url, headers=headers, stream=True) as r:
            with open(pdf_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):  # Descarga en bloques de 8 KB
                    f.write(chunk)  # Guarda cada fragmento en el archivo

        print(f"Descargado: {pdf_name}")  # Mensaje de confirmación
        time.sleep(3)  # Pausa de 3 segundos entre descargas para evitar bloqueos del servidor

# Ejecuta las funciones para obtener y descargar los PDFs
pdf_links = get_pdf_links(base_url)  # Obtiene los enlaces de los PDFs
download_pdfs(pdf_links)  # Descarga los archivos encontrados

print("Descarga completa.")  # Mensaje final cuando todas las descargas han terminado
