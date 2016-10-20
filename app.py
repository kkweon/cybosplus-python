# -*- encoding: utf-8 -*-

import sys

from flask import Flask
from flask.templating import render_template
from flask_cors import CORS
from flask_restful import Api

from API.main import CybosPlus
from models.info.views import info_blueprint
from models.portfolios.views import portfolio_blueprint
from models.stocks.views import stock_blueprint

# UTF-8 Encoding
# 없 으 면 에 러 남
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
api = Api(app)  # Restful
CORS(app)  # Cross Origin


@app.route('/')
def index():
    return render_template('index.html')


app.register_blueprint(stock_blueprint, url_prefix="/stock")
app.register_blueprint(info_blueprint, url_prefix="/info")
app.register_blueprint(portfolio_blueprint, url_prefix="/portfolio")

if __name__ == "__main__":
    from config import DEBUG, CYBOS_TRADING_PASSWORD

    if DEBUG:
        app.run(host="0.0.0.0", port=80, debug=DEBUG)
    else:
        CybosPlus.initialize(password=CYBOS_TRADING_PASSWORD)
        app.run(host="0.0.0.0", port=80)
