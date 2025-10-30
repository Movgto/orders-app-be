from app import create_app
from app.config import config_selection# Usar DevConfig para desarrollo
import os
from dotenv import load_dotenv

load_dotenv()

app = create_app(config_selection[os.environ.get('ENVIRONMENT', 'development')])

if __name__ == '__main__':
    app.run(
        host=app.config.get('HOST', 'localhost'),
        port=app.config.get('PORT', 5001)
    )
