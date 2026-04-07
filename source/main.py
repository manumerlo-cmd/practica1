from crawler import get_subcategories, get_product_links
from parser import parse_product, append_to_csv

# Definimos url de partida y ruta del archivo csv y header
#URL = "https://www.naturitas.es/c/suplementos"
URL = "https://www.naturitas.es/c/mama-y-bebe"
file = r".\dataset\data.csv"
headers = {
    "User-Agent": (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    "AppleWebKit/537.36 "
    "Chrome/123.0.0.0 Safari/537.36"
     )
}

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-ES,es;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive",
}


# Extraemos las subcategorías de la url inicial: {"name": name, "url": href, "count": count}
subcategorias = get_subcategories(URL, headers)

# Recorremos subcategorías extrayendo links de productos. Finalmente recorremos esos links para almacenar los datos
for subcat in subcategorias:
    link = subcat['url']
    nombre = subcat['name']
    productos = get_product_links(link, headers)
    for producto in productos:
        product = parse_product(producto,headers)
        print(product)
        append_to_csv(product, file)

#producto = parse_product(url_producto, headers)
#print(producto)
#append_to_csv(producto, file)

#subcategorias = get_subcategories(URL, headers)



#for subcat in subcategorias:
#    subcat_url = subcat["url"]
#    get_product_links(subcat_url, headers)

#subcat_url = "https://www.naturitas.es/c/suplementos/carbon-activado"
#pl = get_product_links(subcat_url, headers)
#print(pl)



