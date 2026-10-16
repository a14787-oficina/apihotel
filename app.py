from flask import Flask
from flask_restful import Resource, Api
from resources.hotel import Hoteis, Hotel


# Variavel representar minha apliacação

app = Flask(__name__)
api = Api(app)

# Rotas
api.add_resource(Hoteis, "/hoteis")
api.add_resource(Hotel,"/hoteis/<string:id_hotel>")

if __name__ == "__main__":
    app.run(debug=True)