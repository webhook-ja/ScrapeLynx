"""
TEMU SCRAPER con Crawl4AI
Scraper avanzado para productos de Temu con generación de links de afiliado
"""

import asyncio
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field
from typing import List, Optional
import os

# ================== MODELOS DE DATOS ==================

class TemuProduct(BaseModel):
    """Modelo de producto de Temu"""
    title: str = Field(description="Nombre del producto")
    price: float = Field(description="Precio del producto en dólares")
    original_price: Optional[float] = Field(description="Precio original (antes de descuento)")
    discount_percentage: Optional[int] = Field(description="Porcentaje de descuento")
    rating: Optional[float] = Field(description="Rating del producto (estrellas)")
    reviews_count: Optional[int] = Field(description="Número total de reviews/reseñas")
    sales_count: Optional[int] = Field(description="Número de ventas/descargas")
    image_url: Optional[str] = Field(description="URL de la imagen principal del producto")
    product_url: str = Field(description="URL del producto en Temu")
    category: Optional[str] = Field(description="Categoría del producto")

class TemuSearchResults(BaseModel):
    """Resultados de búsqueda de Temu"""
    products: List[TemuProduct]
    total_found: int = Field(description="Total de productos encontrados")

# ================== CONFIGURACIÓN ==================

# Tu ID de afiliado de Temu (cámbialo por el tuyo)
TEMU_AFFILIATE_ID = "YOUR_AFFILIATE_ID"  # ← CAMBIAR ESTO

# Modelo LLM a usar (opciones: "ollama/llama2", "openai/gpt-4o", "openai/gpt-4o-mini")
LLM_PROVIDER = "openai/gpt-4o-mini"  # Más barato y rápido

# ================== FUNCIONES PRINCIPALES ==================

def generate_affiliate_link(product_url: str, affiliate_id: str = TEMU_AFFILIATE_ID) -> str:
    """
    Genera link de afiliado de Temu

    Args:
        product_url: URL original del producto
        affiliate_id: Tu ID de afiliado

    Returns:
        URL con parámetros de afiliado
    """
    # Limpiar URL
    if "?" in product_url:
        base_url = product_url.split("?")[0]
    else:
        base_url = product_url

    # Agregar parámetros de afiliado
    affiliate_params = f"?_x_ads_channel=affiliate&_x_ads_sub_channel={affiliate_id}"

    return base_url + affiliate_params


async def scrape_temu_search(
    search_query: str,
    max_products: int = 20,
    min_rating: float = 0.0,
    min_reviews: int = 0,
    min_sales: int = 0,
    price_min: float = 0.0,
    price_max: float = 999999.0
) -> dict:
    """
    Scrape de búsqueda en Temu con filtros

    Args:
        search_query: Término de búsqueda
        max_products: Máximo de productos a extraer
        min_rating: Rating mínimo (0-5)
        min_reviews: Mínimo de reviews
        min_sales: Mínimo de ventas
        price_min: Precio mínimo
        price_max: Precio máximo

    Returns:
        Dict con productos filtrados y stats
    """

    # URL de búsqueda en Temu
    search_url = f"https://www.temu.com/search_result.html?search_key={search_query.replace(' ', '+')}"

    print(f"🔍 Buscando: '{search_query}' en Temu...")
    print(f"📊 Filtros: Rating>={min_rating}, Reviews>={min_reviews}, Ventas>={min_sales}")
    print(f"💰 Precio: ${price_min} - ${price_max}")

    # Configuración del crawler
    config = CrawlerRunConfig(
        # Anti-bot protection
        magic=True,  # Activa múltiples features anti-bot
        simulate_user=True,  # Simula comportamiento humano
        override_navigator=True,  # Falsifica navigator properties

        # Stealth mode
        browser_type="chromium",
        headless=True,

        # Esperar a que cargue contenido dinámico
        wait_until="networkidle",
        delay_before_return_html=3.0,  # Esperar 3 segundos

        # User agent real
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",

        # Headers adicionales
        headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
    )

    # Estrategia de extracción con LLM
    extraction_strategy = LLMExtractionStrategy(
        provider=LLM_PROVIDER,
        schema=TemuSearchResults.model_json_schema(),
        extraction_type="schema",
        instruction=f"""
        Extrae información de TODOS los productos visibles en esta página de resultados de Temu.

        Para cada producto, extrae:
        - Título completo del producto
        - Precio actual (en dólares, como número decimal)
        - Precio original si hay descuento
        - Porcentaje de descuento si aplica
        - Rating (estrellas, como número decimal 0-5)
        - Número de reviews/reseñas
        - Número de ventas/descargas si está visible
        - URL de la imagen principal
        - URL del producto (link completo)
        - Categoría del producto si está visible

        Extrae hasta {max_products} productos.
        Si un campo no está disponible, usa null.
        Asegúrate de que los precios sean números decimales sin símbolos de moneda.
        """
    )

    # Ejecutar crawling
    async with AsyncWebCrawler(config=config) as crawler:
        print("🤖 Iniciando crawler con anti-bot protection...")

        result = await crawler.arun(
            url=search_url,
            extraction_strategy=extraction_strategy,
            bypass_cache=True
        )

        if not result.success:
            return {
                "success": False,
                "error": "Failed to scrape Temu",
                "products": []
            }

        # Parsear resultados
        try:
            extracted_data = json.loads(result.extracted_content)
            products = extracted_data.get("products", [])

            print(f"✅ Encontrados {len(products)} productos inicialmente")

            # Aplicar filtros
            filtered_products = []
            for product in products:
                # Filtro de rating
                if product.get("rating") and product["rating"] < min_rating:
                    continue

                # Filtro de reviews
                if product.get("reviews_count") and product["reviews_count"] < min_reviews:
                    continue

                # Filtro de ventas
                if product.get("sales_count") and product["sales_count"] < min_sales:
                    continue

                # Filtro de precio
                price = product.get("price", 0)
                if price < price_min or price > price_max:
                    continue

                # Generar link de afiliado
                if product.get("product_url"):
                    product["affiliate_link"] = generate_affiliate_link(product["product_url"])

                filtered_products.append(product)

            print(f"🎯 {len(filtered_products)} productos después de filtros")

            return {
                "success": True,
                "search_query": search_query,
                "total_found": len(products),
                "total_after_filters": len(filtered_products),
                "filters_applied": {
                    "min_rating": min_rating,
                    "min_reviews": min_reviews,
                    "min_sales": min_sales,
                    "price_range": f"${price_min} - ${price_max}"
                },
                "products": filtered_products
            }

        except json.JSONDecodeError as e:
            print(f"❌ Error parseando JSON: {e}")
            return {
                "success": False,
                "error": f"JSON parse error: {str(e)}",
                "products": []
            }


async def scrape_single_product(product_url: str) -> dict:
    """
    Scrape de un producto individual de Temu

    Args:
        product_url: URL del producto

    Returns:
        Dict con datos del producto
    """

    print(f"🔍 Scrapeando producto: {product_url}")

    # Configuración del crawler (similar a arriba)
    config = CrawlerRunConfig(
        magic=True,
        simulate_user=True,
        override_navigator=True,
        browser_type="chromium",
        headless=True,
        wait_until="networkidle",
        delay_before_return_html=3.0,
    )

    # Estrategia de extracción
    extraction_strategy = LLMExtractionStrategy(
        provider=LLM_PROVIDER,
        schema=TemuProduct.model_json_schema(),
        extraction_type="schema",
        instruction="""
        Extrae toda la información disponible de este producto de Temu:
        - Título completo
        - Precio actual
        - Precio original (si hay descuento)
        - Porcentaje de descuento
        - Rating (estrellas)
        - Número de reviews
        - Número de ventas
        - URL de la imagen principal
        - Categoría
        - Todas las especificaciones técnicas disponibles
        """
    )

    async with AsyncWebCrawler(config=config) as crawler:
        result = await crawler.arun(
            url=product_url,
            extraction_strategy=extraction_strategy,
            bypass_cache=True
        )

        if not result.success:
            return {"success": False, "error": "Failed to scrape product"}

        try:
            product_data = json.loads(result.extracted_content)

            # Agregar link de afiliado
            product_data["affiliate_link"] = generate_affiliate_link(product_url)
            product_data["original_url"] = product_url

            return {
                "success": True,
                "product": product_data
            }

        except json.JSONDecodeError as e:
            return {"success": False, "error": f"JSON parse error: {str(e)}"}


# ================== FUNCIONES DE PRUEBA ==================

async def test_search():
    """Prueba de búsqueda"""
    results = await scrape_temu_search(
        search_query="wireless earbuds",
        max_products=10,
        min_rating=4.0,
        min_reviews=100,
        price_max=50.0
    )

    print("\n" + "="*60)
    print("RESULTADOS DE BÚSQUEDA")
    print("="*60)
    print(json.dumps(results, indent=2, ensure_ascii=False))

    # Guardar en archivo
    with open("temu_search_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Resultados guardados en: temu_search_results.json")


async def test_single_product():
    """Prueba de producto individual"""
    # Ejemplo de URL de producto (cámbiala por una real)
    product_url = "https://www.temu.com/example-product.html"

    result = await scrape_single_product(product_url)

    print("\n" + "="*60)
    print("DATOS DEL PRODUCTO")
    print("="*60)
    print(json.dumps(result, indent=2, ensure_ascii=False))


# ================== MAIN ==================

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║         TEMU SCRAPER con Crawl4AI + Afiliados           ║
    ║                      by Dev.Jorge                        ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    # Verificar si existe API key de OpenAI (si usas OpenAI)
    if LLM_PROVIDER.startswith("openai") and not os.getenv("OPENAI_API_KEY"):
        print("⚠️  ADVERTENCIA: No se encontró OPENAI_API_KEY en variables de entorno")
        print("    Configúrala con: export OPENAI_API_KEY='tu-api-key'")
        print("    O usa Ollama local cambiando LLM_PROVIDER a 'ollama/llama2'")

    # Ejecutar prueba de búsqueda
    asyncio.run(test_search())

    # Para probar producto individual, descomenta:
    # asyncio.run(test_single_product())
