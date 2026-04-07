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
        subcategorias.append({"name": name, "url": href, "count": count})

    return subcategorias

def get_product_links(subcat_url, headers):
    """
        Extrae los enlaces de productos de una subcategoría de Naturitas.

        La función navega por las distintas páginas de una subcategoría mediante
        paginación, realiza peticiones HTTP con pausas entre solicitudes para
        evitar sobrecargar el servidor y recopila las URLs de las fichas de
        producto detectadas en cada página.

        Parámetros:
            subcat_url (str): Dirección web de la subcategoría.
            headers (dict): Cabeceras HTTP utilizadas en la solicitud.

        Devuelve:
            list: Lista de URLs de productos encontradas en la subcategoría.
            Si no se detectan productos, devuelve una lista vacía.
        """

    product_links = []
    current_page = 1
    while True:
        url = f"{subcat_url}?page={current_page}"
        print(f"Descargando página {current_page} : {url}")
        #time.sleep(random.uniform(0.8, 1.6))

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("Error al cargar la página:", response.status_code)

        soup = BeautifulSoup(response.content, "html.parser")

        
        #links = soup.find_all("a", href=lambda x: x and x.startswith("/p/"))
        links = soup.find_all("a", class_="product-item-link")#Este a mí no me da los enlaces completos
        if not links:
            print("No hay productos. Fin de la paginación")
            break

        for link in links:
            href = link.get("href")
            full_url = urljoin("https://www.naturitas.es", href)
            product_links.append(href)
            #print (full_url)

        current_page += 1

    return product_links

#Extracción de los detalles de cada producto:
#Los productos en naturitas su href empieza por /p/. Por lo tanto:
#Vemos que se dividen en nombre del producto, precio actual, precio antiguo si es que tiene descuento, marca, descripción, ingredietes, valoración, número de opiniones y disponibilidad.
for product_url in product_links:
    details = get_product_details(product_url, headers)

def get_product_details(product_url, headers):
    response = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    data = {"url": product_url}

    # Nombre
    name_tag = soup.find("h1", class_="product-name")
    data["name"] = name_tag.get_text(strip=True) if name_tag else None

    # Precio actual
    price_tag = soup.find("span", class_="price")
    data["price"] = price_tag.get_text(strip=True) if price_tag else None

    # Marca
    brand_tag = soup.find("a", class_="brand-name")
    data["brand"] = brand_tag.get_text(strip=True) if brand_tag else None



    return data
