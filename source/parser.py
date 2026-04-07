import requests
from bs4 import BeautifulSoup
import csv
import os

def parse_product(url, headers):
    """
        Descarga la página de un producto de Naturitas y extrae sus datos principales.

        Parámetros:
            url (str): URL de la ficha del producto.
            headers (dict): Cabeceras HTTP utilizadas en la petición.

        Devuelve:
            dict: Diccionario con la información extraída del producto, incluyendo
            nombre, precio, marca y SKU. Si algún campo no se encuentra, se devuelve
            con valor None.
        """

    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    nombre_producto = soup.find("span", class_="base", attrs={"data-ui-id": "page-title-wrapper"})
    name = nombre_producto.get_text(strip=True) if nombre_producto else None

    price_element = soup.find("span", attrs={"data-price-type": "finalPrice"})
    price = price_element["data-price-amount"] if price_element else None

    brand_element = soup.find("div", class_="product-brand")
    brand = brand_element.get_text(strip=True) if brand_element else None

    form_element = soup.find("form", id="product_addtocart_form")
    sku = form_element["data-product-sku"] if form_element else None

    return {
    "name": name,
    "price": price,
    "brand": brand,
    "sku": sku
}


def append_to_csv(data, filename):
    """
    Añade una lista de diccionarios a un archivo CSV.

    Si el archivo no existe, lo crea y escribe la cabecera. Si ya existe,
    agrega las nuevas filas al final sin sobrescribir su contenido.

    Parámetros:
        data (list): Lista de diccionarios con la información de los productos.
        filename (str): Ruta del archivo CSV de salida.

    Devuelve:
        None
    """
    if not data:
        print("No hay datos para guardar.")
        return

    if isinstance(data, dict):
        data = [data]

    file_exists = os.path.isfile(filename)
    fieldnames = data[0].keys()

    with open(filename, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerows(data)

def load_processed_urls(filename):
    """
    Carga las URLs ya procesadas desde un archivo de texto.

    Parámetros:
        filename (str): Ruta del archivo con las URLs procesadas.

    Devuelve:
        set: Conjunto de URLs ya procesadas.
    """
    if not os.path.exists(filename):
        return set()

    with open(filename, "r", encoding="utf-8") as file:
        return set(line.strip() for line in file if line.strip())

def save_processed_url(url, filename):
    """
    Guarda una URL procesada en un archivo de texto.

    Parámetros:
        url (str): URL ya procesada.
        filename (str): Ruta del archivo donde registrar la URL.

    Devuelve:
        None
    """
    with open(filename, "a", encoding="utf-8") as file:
        file.write(url + "\n")