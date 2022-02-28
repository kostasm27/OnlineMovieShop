from views import view
from flask import Flask
from utils.config import AppConfig


app = Flask(__name__)
app.config.from_object(AppConfig)


app.register_blueprint(view)


if __name__ == '__main__':
    app.run(debug=True)
