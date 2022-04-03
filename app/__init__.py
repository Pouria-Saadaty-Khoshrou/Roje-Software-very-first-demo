from flask import Flask

app = Flask(__name__,
            static_url_path="",
            static_folder="templates/vendors",
            template_folder="templates")

from app import routes

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

