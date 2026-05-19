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

    old_price_element = soup.find("span", attrs={"data-price-type": "msrpPrice"})
    old_price = old_price_element.get("data-price-amount") if old_price_element else None

    brand_element = soup.find("div", class_="product-brand")
    brand = brand_element.get_text(strip=True) if brand_element else None

    form_element = soup.find("form", id="product_addtocart_form")
    sku = form_element["data-product-sku"] if form_element else None

    presentation_element = soup.find("div", class_="product__presentation")
    presentation = presentation_element.get_text(strip=True) if presentation_element else None

    rating_element = soup.find("div", class_="product-reviews-summary-rating")
    rating_percent = rating_element.get("title") if rating_element else None

    review_element = soup.find("a", class_="product-reviews-summary-link")
    review_count = review_element.get_text(strip=True).split()[0] if review_element else None

    question_element = soup.find("a", class_="product-questions-summary-link")
    question_count = question_element.get_text(strip=True).split()[0] if question_element else None

    # Estado de stock
    stock_element = soup.find("div", class_="stock available product-available")
    stock_status = stock_element.get_text(strip=True) if stock_element else None

    # Longitud de la descripción
    description_element = soup.find("div", class_="product-short-description-text")
    description = description_element.get_text(" ", strip=True) if description_element else None
    description_length = len(description) if description else None

    seal_elements = soup.find_all("li", class_="product-seals-item")
    seals = []
    for seal in seal_elements:
        tooltip = seal.find("div", class_="product-seals-item-tooltip")
        if tooltip:
            tooltip.extract()
        seal_text = seal.get_text(strip=True)
        if seal_text:
            seals.append(seal_text)
    seals = "|".join(seals) if seals else None

    tier_elements = soup.find_all("li", class_="tier-discount-tab")
    tier_prices_list = []
    for tier in tier_elements:
        qty = tier.get("data-qty-discount")
        price = tier.get("data-discount-value")

        if qty and price:
            tier_prices_list.append(f"{qty}:{price}")
    tier_prices = "|".join(tier_prices_list) if tier_prices_list else None

    rating_distribution = {
        "rating_5_count": 0,
        "rating_4_count": 0,
        "rating_3_count": 0,
        "rating_2_count": 0,
        "rating_1_count": 0
    }

    rating_items = soup.find_all("div", class_="customer-reviews-filter-item-action")
    for item in rating_items:
        stars = item.get("data-filter")
        subtotal = item.get("data-subtotal")
        if stars and subtotal:
            key = f"rating_{stars}_count"
            rating_distribution[key] = subtotal

    return {
    "name": name,
    "price": price,
    "brand": brand,
    "sku": sku,
    "old_price": old_price,
    "presentation": presentation,
    "rating_percent": rating_percent,
    "review_count": review_count,
    "question_count": question_count,
    "stock_status": stock_status,
    "description_length": description_length,
    "seals": seals,
    "tier_prices": tier_prices,
    **rating_distribution

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
