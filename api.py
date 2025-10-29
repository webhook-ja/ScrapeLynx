"""
TEMU SCRAPER API REST
FastAPI backend para el sistema de scraping de Temu
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import asyncio
from datetime import datetime
import json
import os

from scraper import scrape_temu_search, scrape_single_product, generate_affiliate_link

# ================== CONFIGURACIÓN ==================

app = FastAPI(
    title="Temu Scraper API",
    description="API para scraping de productos de Temu con links de afiliado",
    version="1.0.0"
)

# CORS (permitir requests desde frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================== MODELOS DE REQUEST ==================

class SearchRequest(BaseModel):
    """Request para búsqueda de productos"""
    search_query: str = Field(..., description="Término de búsqueda", example="wireless earbuds")
    max_products: int = Field(20, ge=1, le=100, description="Máximo de productos")
    min_rating: float = Field(0.0, ge=0.0, le=5.0, description="Rating mínimo")
    min_reviews: int = Field(0, ge=0, description="Mínimo de reviews")
    min_sales: int = Field(0, ge=0, description="Mínimo de ventas")
    price_min: float = Field(0.0, ge=0.0, description="Precio mínimo")
    price_max: float = Field(999999.0, ge=0.0, description="Precio máximo")

class ProductURLRequest(BaseModel):
    """Request para scrape de producto individual"""
    product_url: str = Field(..., description="URL del producto en Temu")

class AffiliateLinkRequest(BaseModel):
    """Request para generar link de afiliado"""
    product_url: str = Field(..., description="URL del producto")
    affiliate_id: Optional[str] = Field(None, description="ID de afiliado (opcional)")

# ================== STORAGE SIMPLE (JSON) ==================

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def save_results(data: dict, prefix: str = "search") -> str:
    """Guarda resultados en archivo JSON"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.json"
    filepath = os.path.join(RESULTS_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return filename

def load_results(filename: str) -> dict:
    """Carga resultados desde archivo JSON"""
    filepath = os.path.join(RESULTS_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Results file not found: {filename}")

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def list_all_results() -> List[dict]:
    """Lista todos los resultados guardados"""
    results = []

    for filename in os.listdir(RESULTS_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(RESULTS_DIR, filename)
            stat = os.stat(filepath)

            results.append({
                "filename": filename,
                "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "size_kb": round(stat.st_size / 1024, 2)
            })

    # Ordenar por fecha más reciente
    results.sort(key=lambda x: x["created_at"], reverse=True)

    return results

# ================== ENDPOINTS ==================

@app.get("/")
async def root():
    """Endpoint raíz - Info de la API"""
    return {
        "message": "Temu Scraper API",
        "version": "1.0.0",
        "endpoints": {
            "search": "/api/search",
            "product": "/api/product",
            "affiliate": "/api/affiliate",
            "results": "/api/results",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/search")
async def search_products(request: SearchRequest, background_tasks: BackgroundTasks):
    """
    Búsqueda de productos en Temu con filtros

    Retorna inmediatamente con task_id y procesa en background
    """
    try:
        # Ejecutar scraping
        results = await scrape_temu_search(
            search_query=request.search_query,
            max_products=request.max_products,
            min_rating=request.min_rating,
            min_reviews=request.min_reviews,
            min_sales=request.min_sales,
            price_min=request.price_min,
            price_max=request.price_max
        )

        # Agregar metadata
        results["timestamp"] = datetime.now().isoformat()
        results["request_params"] = request.dict()

        # Guardar resultados
        filename = save_results(results, prefix="search")
        results["saved_as"] = filename

        return {
            "success": True,
            "message": "Búsqueda completada",
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en scraping: {str(e)}")

@app.post("/api/product")
async def get_product(request: ProductURLRequest):
    """
    Obtiene datos de un producto individual
    """
    try:
        result = await scrape_single_product(request.product_url)

        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "Unknown error"))

        # Agregar metadata
        result["timestamp"] = datetime.now().isoformat()

        # Guardar resultado
        filename = save_results(result, prefix="product")
        result["saved_as"] = filename

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en scraping: {str(e)}")

@app.post("/api/affiliate")
async def create_affiliate_link(request: AffiliateLinkRequest):
    """
    Genera link de afiliado para una URL de producto
    """
    try:
        affiliate_link = generate_affiliate_link(
            product_url=request.product_url,
            affiliate_id=request.affiliate_id or os.getenv("TEMU_AFFILIATE_ID", "YOUR_AFFILIATE_ID")
        )

        return {
            "success": True,
            "original_url": request.product_url,
            "affiliate_link": affiliate_link,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando link: {str(e)}")

@app.get("/api/results")
async def get_all_results():
    """
    Lista todos los resultados guardados
    """
    try:
        results = list_all_results()

        return {
            "success": True,
            "total_results": len(results),
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listando resultados: {str(e)}")

@app.get("/api/results/{filename}")
async def get_result(filename: str):
    """
    Obtiene un resultado específico por filename
    """
    try:
        data = load_results(filename)

        return {
            "success": True,
            "filename": filename,
            "data": data
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cargando resultado: {str(e)}")

@app.delete("/api/results/{filename}")
async def delete_result(filename: str):
    """
    Elimina un resultado guardado
    """
    try:
        filepath = os.path.join(RESULTS_DIR, filename)

        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail=f"File not found: {filename}")

        os.remove(filepath)

        return {
            "success": True,
            "message": f"Deleted: {filename}"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error eliminando archivo: {str(e)}")

# ================== WEBHOOK PARA N8N ==================

@app.post("/webhook/n8n/search")
async def n8n_search_webhook(request: SearchRequest):
    """
    Endpoint especial para n8n
    Retorna datos en formato optimizado para n8n
    """
    try:
        results = await scrape_temu_search(
            search_query=request.search_query,
            max_products=request.max_products,
            min_rating=request.min_rating,
            min_reviews=request.min_reviews,
            min_sales=request.min_sales,
            price_min=request.price_min,
            price_max=request.price_max
        )

        if not results.get("success"):
            return {
                "success": False,
                "error": results.get("error", "Unknown error"),
                "products": []
            }

        # Formato para n8n (array de productos)
        products = results.get("products", [])

        return {
            "success": True,
            "total_products": len(products),
            "search_query": request.search_query,
            "timestamp": datetime.now().isoformat(),
            "products": products
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "products": []
        }

# ================== MAIN ==================

if __name__ == "__main__":
    import uvicorn

    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║            TEMU SCRAPER API - Iniciando...              ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    # Verificar configuración
    affiliate_id = os.getenv("TEMU_AFFILIATE_ID", "YOUR_AFFILIATE_ID")
    if affiliate_id == "YOUR_AFFILIATE_ID":
        print("⚠️  ADVERTENCIA: TEMU_AFFILIATE_ID no configurado en .env")
    else:
        print(f"✅ Affiliate ID configurado: {affiliate_id}")

    # Iniciar servidor
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
