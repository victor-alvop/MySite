from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    # Usar el puerto de la variable de entorno 'PORT' que asigna Railway, o 5000 por defecto
    port = int(os.getenv('PORT', 5000))

    # Ejecutar la aplicación Flask en el puerto y dirección correcta
    app.run(host='0.0.0.0', port=port, debug=True)