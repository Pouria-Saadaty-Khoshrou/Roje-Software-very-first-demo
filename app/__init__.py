from flask import Flask

app = Flask(__name__,
            static_url_path="",
            static_folder="templates/vendors",
            template_folder="templates")

from app import routes


