# Práctica 1 –  Web Scraping Naturitas

## Introducción

El presente trabajo tiene como objetivo desarrollar un sistema de extracción de datos mediante técnicas de web scraping aplicado a una web real. En concreto, se ha seleccionado el sitio web de Naturitas, especializado en la venta de productos naturales y suplementos alimenticios.

El propósito principal es construir un scraper capaz de:

- Navegar de forma autónoma  
- Extraer información estructurada de productos  
- Generar un dataset reutilizable  
- Aplicar buenas prácticas en el proceso de recolección de datos  

---
## Autores

Este proyecto ha sido realizado por:

- Xaime Ferrín Suárez
- Manuel Merlo Torrente

---
## Estructura del repositorio
    practica1/
    ├── dataset/
    │ ├── data.csv
    │ └── processed_urls.txt
    ├── source/
    │ ├── main.py
    │ ├── crawler.py
    │ └── parser.py
    ├── README.md
    ├── requirements.txt
    └── .gitignore

## Descripción del sitio web

La web seleccionada (https://www.naturitas.es) es un ecommerce que organiza sus productos de forma jerárquica:

- Categorías principales  
- Subcategorías  
- Listados de productos  
- Fichas individuales de producto  

Para el desarrollo del proyecto se ha utilizado como punto de partida la categoría:

https://www.naturitas.es/c/suplementos

---

## Metodología de scraping

El scraper se ha diseñado siguiendo una estrategia jerárquica:

Categoría -> Subcategorías -> Productos -> Ficha de producto

### Descubrimiento de subcategorías

Se extraen:

- nombre  
- URL  
- número de productos  

### Navegación por subcategorías

Uso de paginación (?p=1, ?p=2...)

### Extracción de enlaces de productos

```html
<a class="product-item-link" href="...">
```

### Extracción de datos

Campos:

- name  
- price  
- brand  
- sku  

### Almacenamiento

dataset/data.csv

### Control de progreso

dataset/processed_urls.txt

---

## Diagrama de flujo del scraper

```
        [Inicio]
           |
           v
 [URL Categoría Principal]
           |
           v
 [Extraer Subcategorías]
           |
           v
   ┌────────────────────────┐
   │ Para cada subcategoría │
   └────────────────────────┘
           |
           v
 [Obtener páginas (?p=1,2,...)]
           |
           v
 [Extraer links de productos]
           |
           v
   ┌─────────────────────┐
   │ Para cada producto  │
   └─────────────────────┘
           |
           v
 [¿Ya procesado?] ─── Sí ───▶ [Saltar]
           |
           No
           |
           v
 [Parsear producto]
           |
           v
 [Guardar en CSV]
           |
           v
 [Guardar URL procesada]
           |
           v
        [Fin]
```

---

## Estructura del código

source/
├── main.py  
├── crawler.py  
└── parser.py  

---

## Dataset generado

Formato:

name,price,brand,sku,url,subcategory

---

## Aspectos éticos

- robots.txt  
- pausas entre peticiones  
- evitar rutas restringidas  

---

## Limitaciones

- Dependencia del HTML  
- Posibles cambios en la web  
- No JavaScript  

---

## Mejoras futuras

- más campos  
- paralelización  
- base de datos  

---

## Conclusión

Se ha desarrollado un scraper funcional capaz de extraer datos estructurados de una web real aplicando buenas prácticas.

---

