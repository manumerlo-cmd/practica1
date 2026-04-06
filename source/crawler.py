import requests
import time
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_subcategories(URL, headers):
    """
      Obtiene las subcategorías de una página de categoria de Naturitas.

    Args:
        url (str): URL de la categoría principal.
        headers (dict): Cabeceras HTTP para la petición.

    Returns:
        list: Lista de diccionarios con el nombre, enlace y número de productos
        de cada subcategoría.
    """
    response = requests.get(URL, headers=headers)
    print("Status: ", response.status_code)
    soup = BeautifulSoup(response.content, "html.parser")
    # Obtenemos todos los los links de productos de la página (etiqueta a, clase "product-item-link" con link)
    products_links = soup.find_all("a", class_="product-item-link", href=True)

    # Buscamos caterorías por su etiqueta
    category_names = soup.find_all("span", class_="cat-name")
    # Sacamos el link de la etiqueta padre y guardamos en diccionario subcategorias, links y contador
    subcategorias = []
    for cat in category_names:
        name = cat.get_text(strip=True)
        parent_link = cat.find_parent("a")
        href = parent_link["href"]
        count_tag = parent_link.find("span", class_="count")
        count_tag = count_tag.get_text(strip=True)
        count = int(count_tag.replace("(", "").replace(")", ""))

    subcategorias.append({"name": name, "href": href, "count": count})

    return subcategorias

def get_product_links(subcat_url, headers):
    """
    Para obtener los productos de cada subcategoría
    Definimos una función que reciba la URL de cada subcategoría, extraiga los productos a través de las diferentes
    páginas, añada pausas aleatorias para no saturar el servidor y que nos devuleva los productos en formato lista.
    """

    product_links = []
    current_page = 1
    while True:
        url = f"{subcat_url}?page={current_page}"
        print(f"Descargando página {current_page} : {url}")
        time.sleep(random.uniform(0.8, 1.6))

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("Error al cargar la página:", response.status_code)

        soup = BeautifulSoup(response.content, "html.parser")

        cards = soup.find_all("a", clas_="productt_card")
        if not cards:
            print("No hay productos. Fin de la paginación")
        break

        for card in cards:
            href = card.get("href")
            full_url = "https://www.naturitas.es" + href
            product_links.append(full_url)

            current_page += 1

    return product_links
