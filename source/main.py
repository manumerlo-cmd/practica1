from crawler import get_subcategories, process_subcategory_pages

URL = "https://www.naturitas.es/c/suplementos"

dataset_file = r".\dataset\data.csv"
processed_products_file = r".\dataset\processed_product_urls.txt"
processed_pages_file = r".\dataset\processed_pages.txt"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "Chrome/123.0.0.0 Safari/537.36"
    )
}

subcategories = get_subcategories(URL, headers)

for subcat in subcategories:
    process_subcategory_pages(
        subcat_url=subcat["url"],
        subcategory_name=subcat["name"],
        headers=headers,
        dataset_file=dataset_file,
        processed_products_file=processed_products_file,
        processed_pages_file=processed_pages_file
    )