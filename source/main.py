from crawler import get_subcategories, get_product_links

URL =  "https://www.naturitas.es/c/suplementos"
headers = {
    "User-Agent": (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    "AppleWebKit/537.36 "
    "Chrome/123.0.0.0 Safari/537.36"
     )
}

subcategorias = get_subcategories(URL, headers)

for subcat in subcategorias:
    subcat_url = subcat["url"]
    get_product_links(subcat_url, headers)

#subcat_url = "https://www.naturitas.es/c/suplementos/carbon-activado"
#pl = get_product_links(subcat_url, headers)
#print(pl)



