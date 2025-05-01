from sqlalchemy import text
from app import db  # Asegúrate que `db` es tu instancia de SQLAlchemy

# Ajusta esto a tu tabla y columna reales
tabla = "employees"
columna = "salary"

# Sentencia SQL que hace el cambio
sql = f"""
ALTER TABLE {tabla}
ALTER COLUMN {columna} TYPE numeric(10, 2)
USING {columna}::numeric;
"""

# Ejecutar desde SQLAlchemy
with db.engine.connect() as connection:
    connection.execute(text(sql))
    connection.commit()
