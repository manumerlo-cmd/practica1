from crawler import get_subcategories

URL =  "https://www.naturitas.es/c/suplementos"
headers = {
    "User-Agent": (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    "AppleWebKit/537.36 "
    "Chrome/123.0.0.0 Safari/537.36"
     )
}

subcategorias = get_subcategories(URL, headers)


#Para obtener los productos de cada subcategoría

import requests
import time
import random
import bs4 from BeautifulSoup
from urlib.parse import urljoin

#Definimos una función que reciba la URL de cada subcategoría, extraiga los productos a través de las diferentes páginas, añada pausas aleatorias para no saturar el servidor y que nos devuleva los productos en formato lista.

def get_product_links(subcat_url, headers):
    product_links = []
    current_page = 1
    while True:
        url = f"{subcat_url}?page={current_page]"
        print(f"Descargnado página {current_page} : {url}")
        time.sleep(random.uniform(0.8, 1.6))

        response = request.get(url, headers=headers)
        if response.status.code != 200:
            print("Error al cargar la página:", response.status.code)
        soup = BeautifulSoup(response.content, "html.parser")

cards = soup.find_all("a", clas_="productt_card")
if not cards:
    print("No hay productos. Fin de la paginación")
    break
for card in cards:
    href = card.get("href")
    full_url= "https://www.naturitas.es", href)
    product_links.append(full_url)

    current_page += 1

return product_links



