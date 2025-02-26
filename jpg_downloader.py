import requests  # Librería para hacer solicitudes HTTP
import os  # Para manejar directorios y archivos
import time  # Para agregar pausas entre descargas
from bs4 import BeautifulSoup  # Para analizar el contenido HTML de la página
from urllib.parse import urljoin  # Para construir URLs absolutas a partir de relativas

# URL de la página donde se encuentran las imágenes
base_url = ""

# Carpeta donde se guardarán las imágenes descargadas
output_folder = ""
os.makedirs(output_folder, exist_ok=True)  # Crea la carpeta si no existe

# Encabezado HTTP para evitar bloqueos por parte del servidor
headers = {"User-Agent": "Mozilla/5.0"}

def get_image_links(url):
    """Obtiene los enlaces de todas las imágenes (.jpg) en la página dada."""

    # Realiza una solicitud HTTP a la página
    response = requests.get(url, headers=headers)
    
    # Verifica si la solicitud fue exitosa (código 200)
    if response.status_code != 200:
        print(f"Error al acceder a la página: {response.status_code}")
        return []

    # Analiza el contenido HTML de la página
    soup = BeautifulSoup(response.text, "html.parser")

    img_links = []  # Lista para almacenar los enlaces de las imágenes

    # Busca todos los enlaces en la página
    for link in soup.find_all("a", href=True):
        href = link["href"]  # Obtiene el atributo href del enlace
        
        # Verifica si el enlace termina en ".jpg"
        if href.endswith(".jpg"):  
            # Si el enlace es relativo, lo convierte en una URL absoluta
            full_url = urljoin(url, href)
            img_links.append(full_url)  # Agrega el enlace a la lista

    return img_links  # Retorna la lista de enlaces a imágenes

def download_images(img_links):
    """Descarga las imágenes encontradas en la lista de enlaces."""

    # Verifica si la lista está vacía
    if not img_links:
        print("No se encontraron imágenes JPG.")
        return

    for img_url in img_links:
        img_name = img_url.split("/")[-1]  # Extrae el nombre del archivo desde la URL
        img_path = os.path.join(output_folder, img_name)  # Define la ruta completa del archivo

        # Descarga la imagen en fragmentos para evitar errores
        try:
            with requests.get(img_url, headers=headers, stream=True) as r:
                if r.status_code == 200:  # Verifica si la descarga fue exitosa
                    with open(img_path, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):  # Descarga en bloques de 8 KB
                            f.write(chunk)  # Guarda cada fragmento en el archivo
                    print(f"Descargado: {img_name}")  # Mensaje de confirmación
                else:
                    print(f"No se pudo descargar {img_name}. Código {r.status_code}")
        except Exception as e:
            print(f"Error al descargar {img_name}: {e}")

        time.sleep(3)  # Pausa de 3 segundos entre descargas para evitar bloqueos del servidor

# Ejecuta las funciones para obtener y descargar las imágenes
img_links = get_image_links(base_url)  # Obtiene los enlaces de las imágenes
download_images(img_links)  # Descarga los archivos encontrados

print("Descarga completa.")  # Mensaje final cuando todas las descargas han terminado
