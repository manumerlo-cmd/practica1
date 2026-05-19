import requests
import os
import time
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from parser import parse_product, append_to_csv, load_processed_urls, save_processed_url

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

    session = requests.Session()
    session.headers.update(headers)
    response = session.get(URL, headers=headers)
    print("Status: ", response.status_code)
    soup = BeautifulSoup(response.content, "html.parser")
    print("Buscando links de subcategorías...", end=" ")
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
    print("OK\n")
    return subcategorias


def get_product_links(subcat_url, headers, processed_pages_file):
    """
    Extrae los enlaces de productos de una subcategoría de Naturitas.

    La función recorre las páginas de una subcategoría usando paginación,
    evita volver a procesar páginas ya rastreadas y guarda el progreso en
    un archivo auxiliar.

    Parámetros:
        subcat_url (str): URL de la subcategoría.
        headers (dict): Cabeceras HTTP utilizadas en la solicitud.
        processed_pages_file (str): Archivo donde se guardan las páginas ya procesadas.

    Devuelve:
        list: Lista de URLs de productos encontradas.
    """
    product_links = []
    current_page = 1

    processed_pages = load_processed_items(processed_pages_file)

    while True:
        page_url = f"{subcat_url}?p={current_page}"

        if page_url in processed_pages:
            print(f"Página ya procesada: {page_url}")
            current_page += 1
            continue

        print(f"Procesando página: {page_url}")

        response = requests.get(page_url, headers=headers, timeout=15)

        if response.status_code != 200:
            print(f"Error al cargar página {page_url}: {response.status_code}")
            break

        soup = BeautifulSoup(response.content, "html.parser")

        links = soup.find_all("a", class_="product-item-link", href=True)

        if not links:
            print("No hay más productos en esta subcategoría.")
            break

        for link in links:
            product_url = urljoin(subcat_url, link.get("href"))
            product_links.append(product_url)

        save_processed_item(page_url, processed_pages_file)
        processed_pages.add(page_url)

        time.sleep(random.uniform(1.5, 3.0))
        current_page += 1

    product_links = list(dict.fromkeys(product_links))

    return product_links

def load_processed_items(filename):
    """
    Carga elementos ya procesados desde un archivo de texto.

    Parámetros:
        filename (str): Ruta del archivo.

    Devuelve:
        set: Conjunto de elementos procesados.
    """
    if not os.path.exists(filename):
        return set()

    with open(filename, "r", encoding="utf-8") as file:
        return set(line.strip() for line in file if line.strip())


def save_processed_item(item, filename):
    """
    Guarda un elemento procesado en un archivo de texto.

    Parámetros:
        item (str): Elemento procesado.
        filename (str): Ruta del archivo.

    Devuelve:
        None
    """
    with open(filename, "a", encoding="utf-8") as file:
        file.write(item + "\n")

def process_subcategory_pages(
    subcat_url,
    subcategory_name,
    headers,
    dataset_file,
    processed_products_file,
    processed_pages_file
):
    """
    Recorre las páginas paginadas de una subcategoría, extrae los enlaces
    de producto, parsea cada producto y guarda los resultados.

    La página solo se marca como procesada cuando todos sus productos han
    sido tratados correctamente o saltados por estar ya procesados.
    """

    processed_products = load_processed_urls(processed_products_file)
    processed_pages = load_processed_urls(processed_pages_file)

    current_page = 1

    while True:
        page_url = f"{subcat_url}?p={current_page}"

        if page_url in processed_pages:
            print(f"Página ya procesada: {page_url}")
            current_page += 1
            continue

        print(f"Procesando página: {page_url}")

        try:
            response = requests.get(page_url, headers=headers, timeout=15)
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f"Error cargando página {page_url}: {e}")
            break

        soup = BeautifulSoup(response.content, "html.parser")

        product_link_elements = soup.find_all("a", class_="product-item-link", href=True)

        if not product_link_elements:
            print("No hay más productos en esta subcategoría.")
            break

        product_links = []

        for link in product_link_elements:
            product_url = urljoin(subcat_url, link.get("href"))
            product_links.append(product_url)

        product_links = list(dict.fromkeys(product_links))

        page_ok = True

        for product_url in product_links:
            if product_url in processed_products:
                print(f"Producto ya procesado: {product_url}")
                continue

            try:
                time.sleep(random.uniform(1.0, 2.5))

                product_data = parse_product(product_url, headers)

                if product_data is None:
                    print(f"No se pudo parsear: {product_url}")
                    page_ok = False
                    continue

                product_data["url"] = product_url
                product_data["subcategory"] = subcategory_name

                append_to_csv(product_data, dataset_file)

                save_processed_url(product_url, processed_products_file)
                processed_products.add(product_url)

                print(f"Producto guardado: {product_data.get('name')}")

            except Exception as e:
                print(f"Error procesando producto {product_url}: {e}")
                page_ok = False

        if page_ok:
            save_processed_url(page_url, processed_pages_file)
            processed_pages.add(page_url)
            print(f"Página completada: {page_url}")
        else:
            print(f"Página no marcada como completada: {page_url}")

        time.sleep(random.uniform(1.5, 3.0))
        current_page += 1