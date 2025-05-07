from app import create_app
import os
from dotenv import load_dotenv

load_dotenv()

app = create_app()

if __name__ == "__main__":
    if os.getenv('PRODUCTION') == "false":
        app.run(debug=True, host='0.0.0.0')
    else:
        app.run()
