from crawler import get_subcategories, get_product_links
from parser import parse_product, append_to_csv, load_processed_urls, save_processed_url
import time
import random

# Definimos url de partida y ruta del archivo csv, ruta archivo de url procesadas
# (para retomar si se rompe el flujo) y header
#URL = "https://www.naturitas.es/c/suplementos"
URL = "https://www.naturitas.es/c/mama-y-bebe"
file = r".\dataset\data.csv"
file_processed = r".\dataset\processed.csv"
headers = {
    "User-Agent": (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    "AppleWebKit/537.36 "
    "Chrome/123.0.0.0 Safari/537.36"
     )
}
# Cargamos las url procesadas
processed_urls = load_processed_urls(file_processed)

# Extraemos las subcategorías de la url inicial: {"name": name, "url": href, "count": count}
subcategorias = get_subcategories(URL, headers)

# Recorremos subcategorías extrayendo links de productos. Finalmente recorremos esos links para almacenar
# los datos. Si ya está parseada, continuamos sin procesarla. Guardamos en csv auxiliar las url parseadas
for subcat in subcategorias:
    link = subcat['url']
    subcategoria = subcat['name']
    productos = get_product_links(link, headers)
    for producto in productos:
        if producto in processed_urls:
            print("{} ya procesado".format(producto))
        else:
            time.sleep(random.uniform(0.8, 1.6))
            print("Procesado {}".format(producto))
            product = parse_product(producto,headers)
            product["Subcategoria"] = subcategoria
            save_processed_url(producto, file_processed)
            append_to_csv(product, file)
