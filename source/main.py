import requests
from bs4 import BeautifulSoup

URL =  "https://www.naturitas.es/c/suplementos"

headers = {
    "User-Agent": (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    "AppleWebKit/537.36 "
    "Chrome/123.0.0.0 Safari/537.36"
     )
}

response = requests.get(URL, headers=headers)
print("Status: ", response.status_code)
soup = BeautifulSoup(response.content, "html.parser")
# Obtenemos todos los los links de productos de la página (etiqueta a, clase "product-item-link" con link)
products_links = soup.find_all("a", class_="product-item-link", href=True)

# Buscamos caterorías por su etiqueta
category_names = soup.find_all("span", class_="cat-name")

# Sacamos el link de la etiqueta padre y guardamos en diccionario subcategorias
subcategorias = []
for cat in category_names:
    name = cat.get_text(strip=True)
    parent_link = cat.find_parent("a")

    href = parent_link["href"]

    subcategorias.append({"name": name, "href": href})



