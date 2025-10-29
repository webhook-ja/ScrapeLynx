"""
INICIALIZACIÓN DE BASE DE DATOS
Script para crear tablas e insertar datos iniciales
Se ejecuta automáticamente en el entrypoint.sh
"""

import asyncio
import sys
import os
from database import db, init_database, test_database

async def main():
    """Inicializa la base de datos"""

    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║     TEMU SCRAPER - INICIALIZACIÓN DE BASE DE DATOS   ║
    ╚═══════════════════════════════════════════════════════╝
    """)

    try:
        # 1. Crear tablas
        print("📊 Creando tablas...")
        init_database()
        print("✅ Tablas creadas exitosamente\n")

        # 2. Probar conexión
        print("🔌 Probando conexión...")
        success = await test_database()

        if not success:
            print("❌ Error conectando a la base de datos")
            sys.exit(1)

        print("\n" + "="*60)
        print("✅ BASE DE DATOS INICIALIZADA CORRECTAMENTE")
        print("="*60)
        print("\n🚀 Puedes iniciar la API ahora con:")
        print("   python api.py")
        print("   O con Docker:")
        print("   docker-compose up api\n")

        return True

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\n💡 Verifica:")
        print("   1. DATABASE_URL está configurado correctamente")
        print("   2. PostgreSQL está corriendo")
        print("   3. Las credenciales son correctas")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
