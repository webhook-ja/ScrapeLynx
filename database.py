"""
DATABASE MANAGER
Sistema de base de datos para guardar productos scrapeados
Soporta SQLite (desarrollo) y PostgreSQL (producción)
"""

import os
from datetime import datetime
from typing import Optional, List, Dict
from contextlib import asynccontextmanager

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.pool import StaticPool
from dotenv import load_dotenv

load_dotenv()

# ================== CONFIGURACIÓN ==================

DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")  # sqlite o postgresql
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///temu_products.db")

# Para PostgreSQL async
if DATABASE_TYPE == "postgresql":
    ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
else:
    ASYNC_DATABASE_URL = "sqlite+aiosqlite:///temu_products.db"

# ================== MODELOS ==================

Base = declarative_base()

class Product(Base):
    """Modelo de producto scrapeado"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    # Datos del producto
    title = Column(String(500), nullable=False, index=True)
    price = Column(Float, nullable=False)
    original_price = Column(Float, nullable=True)
    discount_percentage = Column(Integer, nullable=True)

    # Ratings y reviews
    rating = Column(Float, nullable=True, index=True)
    reviews_count = Column(Integer, nullable=True, index=True)
    sales_count = Column(Integer, nullable=True, index=True)

    # URLs
    image_url = Column(Text, nullable=True)
    product_url = Column(String(1000), nullable=False, unique=True, index=True)
    affiliate_link = Column(String(1000), nullable=True)

    # Categoría
    category = Column(String(200), nullable=True, index=True)

    # Metadata
    search_query = Column(String(200), nullable=True, index=True)
    scraped_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Control
    is_active = Column(Boolean, default=True)
    price_history = Column(Text, nullable=True)  # JSON string con historial de precios

    def to_dict(self) -> dict:
        """Convierte el modelo a diccionario"""
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "original_price": self.original_price,
            "discount_percentage": self.discount_percentage,
            "rating": self.rating,
            "reviews_count": self.reviews_count,
            "sales_count": self.sales_count,
            "image_url": self.image_url,
            "product_url": self.product_url,
            "affiliate_link": self.affiliate_link,
            "category": self.category,
            "search_query": self.search_query,
            "scraped_at": self.scraped_at.isoformat() if self.scraped_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_active": self.is_active
        }

class SearchHistory(Base):
    """Historial de búsquedas realizadas"""
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    search_query = Column(String(200), nullable=False, index=True)

    # Filtros usados
    max_products = Column(Integer)
    min_rating = Column(Float)
    min_reviews = Column(Integer)
    min_sales = Column(Integer)
    price_min = Column(Float)
    price_max = Column(Float)

    # Resultados
    total_found = Column(Integer)
    total_filtered = Column(Integer)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    execution_time = Column(Float)  # Segundos
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "search_query": self.search_query,
            "max_products": self.max_products,
            "min_rating": self.min_rating,
            "min_reviews": self.min_reviews,
            "min_sales": self.min_sales,
            "price_min": self.price_min,
            "price_max": self.price_max,
            "total_found": self.total_found,
            "total_filtered": self.total_filtered,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "execution_time": self.execution_time,
            "success": self.success,
            "error_message": self.error_message
        }

# ================== DATABASE MANAGER ==================

class DatabaseManager:
    """Gestor de base de datos con soporte async"""

    def __init__(self):
        # Engine síncrono (para crear tablas)
        if DATABASE_TYPE == "sqlite":
            self.engine = create_engine(
                DATABASE_URL,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool
            )
        else:
            self.engine = create_engine(DATABASE_URL, pool_pre_ping=True)

        # Engine asíncrono (para operaciones)
        self.async_engine = create_async_engine(
            ASYNC_DATABASE_URL,
            echo=False,
            pool_pre_ping=True
        )

        # Session maker
        self.async_session_maker = async_sessionmaker(
            self.async_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    def create_tables(self):
        """Crea todas las tablas (síncrono)"""
        Base.metadata.create_all(bind=self.engine)
        print("✅ Tablas creadas exitosamente")

    @asynccontextmanager
    async def get_session(self):
        """Context manager para sesiones async"""
        async with self.async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def save_product(self, product_data: dict) -> Product:
        """Guarda o actualiza un producto"""
        async with self.get_session() as session:
            # Buscar si existe por product_url
            from sqlalchemy import select
            stmt = select(Product).where(Product.product_url == product_data.get("product_url"))
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()

            if existing:
                # Actualizar
                for key, value in product_data.items():
                    if hasattr(existing, key):
                        setattr(existing, key, value)
                existing.updated_at = datetime.utcnow()
                product = existing
            else:
                # Crear nuevo
                product = Product(**product_data)
                session.add(product)

            await session.commit()
            await session.refresh(product)
            return product

    async def save_products_batch(self, products_data: List[dict]) -> List[Product]:
        """Guarda múltiples productos"""
        saved = []
        for product_data in products_data:
            product = await self.save_product(product_data)
            saved.append(product)
        return saved

    async def get_product_by_url(self, product_url: str) -> Optional[Product]:
        """Obtiene producto por URL"""
        async with self.get_session() as session:
            from sqlalchemy import select
            stmt = select(Product).where(Product.product_url == product_url)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def search_products(
        self,
        query: Optional[str] = None,
        min_rating: Optional[float] = None,
        min_reviews: Optional[int] = None,
        min_sales: Optional[int] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        category: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Product]:
        """Busca productos con filtros"""
        async with self.get_session() as session:
            from sqlalchemy import select, or_

            stmt = select(Product).where(Product.is_active == True)

            # Filtros
            if query:
                stmt = stmt.where(
                    or_(
                        Product.title.ilike(f"%{query}%"),
                        Product.search_query.ilike(f"%{query}%")
                    )
                )

            if min_rating:
                stmt = stmt.where(Product.rating >= min_rating)

            if min_reviews:
                stmt = stmt.where(Product.reviews_count >= min_reviews)

            if min_sales:
                stmt = stmt.where(Product.sales_count >= min_sales)

            if price_min:
                stmt = stmt.where(Product.price >= price_min)

            if price_max:
                stmt = stmt.where(Product.price <= price_max)

            if category:
                stmt = stmt.where(Product.category == category)

            # Ordenar por rating * reviews (popularidad)
            stmt = stmt.order_by((Product.rating * Product.reviews_count).desc())

            # Paginación
            stmt = stmt.limit(limit).offset(offset)

            result = await session.execute(stmt)
            return result.scalars().all()

    async def save_search_history(self, search_data: dict) -> SearchHistory:
        """Guarda historial de búsqueda"""
        async with self.get_session() as session:
            search = SearchHistory(**search_data)
            session.add(search)
            await session.commit()
            await session.refresh(search)
            return search

    async def get_search_history(self, limit: int = 50) -> List[SearchHistory]:
        """Obtiene historial de búsquedas"""
        async with self.get_session() as session:
            from sqlalchemy import select
            stmt = select(SearchHistory).order_by(SearchHistory.created_at.desc()).limit(limit)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_stats(self) -> dict:
        """Obtiene estadísticas generales"""
        async with self.get_session() as session:
            from sqlalchemy import select, func

            # Total productos
            total_stmt = select(func.count(Product.id)).where(Product.is_active == True)
            total_result = await session.execute(total_stmt)
            total_products = total_result.scalar()

            # Precio promedio
            avg_price_stmt = select(func.avg(Product.price)).where(Product.is_active == True)
            avg_price_result = await session.execute(avg_price_stmt)
            avg_price = avg_price_result.scalar() or 0

            # Rating promedio
            avg_rating_stmt = select(func.avg(Product.rating)).where(Product.is_active == True)
            avg_rating_result = await session.execute(avg_rating_stmt)
            avg_rating = avg_rating_result.scalar() or 0

            # Total búsquedas
            total_searches_stmt = select(func.count(SearchHistory.id))
            total_searches_result = await session.execute(total_searches_stmt)
            total_searches = total_searches_result.scalar()

            return {
                "total_products": total_products,
                "avg_price": round(avg_price, 2),
                "avg_rating": round(avg_rating, 2),
                "total_searches": total_searches
            }

# ================== INSTANCIA GLOBAL ==================

db = DatabaseManager()

# ================== FUNCIONES AUXILIARES ==================

async def init_database():
    """Inicializa la base de datos"""
    db.create_tables()
    print("✅ Base de datos inicializada")

async def test_database():
    """Prueba la conexión a la base de datos"""
    try:
        stats = await db.get_stats()
        print("✅ Conexión exitosa a la base de datos")
        print(f"📊 Estadísticas: {stats}")
        return True
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        return False

# ================== MAIN (TESTING) ==================

if __name__ == "__main__":
    import asyncio

    async def main():
        print("🔧 Inicializando base de datos...")
        init_database()

        print("\n🧪 Probando conexión...")
        await test_database()

        print("\n💾 Guardando producto de prueba...")
        test_product = {
            "title": "Auriculares Bluetooth TWS",
            "price": 15.99,
            "original_price": 39.99,
            "discount_percentage": 60,
            "rating": 4.7,
            "reviews_count": 1523,
            "sales_count": 5420,
            "image_url": "https://example.com/image.jpg",
            "product_url": "https://www.temu.com/test-product-123",
            "affiliate_link": "https://www.temu.com/test-product-123?_x_ads_channel=affiliate",
            "category": "Electronics",
            "search_query": "wireless earbuds"
        }

        product = await db.save_product(test_product)
        print(f"✅ Producto guardado: {product.id} - {product.title}")

        print("\n🔍 Buscando productos...")
        products = await db.search_products(query="earbuds", limit=10)
        print(f"✅ Encontrados {len(products)} productos")

        for p in products:
            print(f"  - {p.title} | ${p.price} | ⭐{p.rating}")

        print("\n📊 Estadísticas finales:")
        stats = await db.get_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")

    asyncio.run(main())
