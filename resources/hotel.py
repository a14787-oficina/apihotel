from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
    { "hotel_id": "paraiso", "nome": "Hotel Paraiso", "estrelas": 4.6, "diaria": 123.99, "cidade": "Porto"},
    { "hotel_id": "fukui", "nome": "Fukui Resort", "estrelas": 4.8, "diaria": 225.99, "cidade": "Viena"},
    { "hotel_id": "aguas", "nome": "Hotel Aguas", "estrelas": 4.2, "diaria": 193.99, "cidade": "Lisboa"}
]

# Listar todos os hoteis
class Hoteis(Resource):
        def get(self):
            return{"hoteis": [hotel.json() for hotel in HotelModel.query.all()] }

# Listar, Inserir, Atuaçozar e Eliminar um hotel especifico
class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("nome", type=str, help="Nome Obrigatório")
    argumentos.add_argument("estrelas", type=float, help="Estrelas Obrigatório")
    argumentos.add_argument("diaria", type=float, help="Diária Obrigatório")
    argumentos.add_argument("cidade", type=str, help="Cidade Obrigatório")
    def get(self, id_hotel):
        hotel_encontrado = HotelModel.find_hotel(id_hotel)
        if hotel_encontrado:
            return hotel_encontrado.json(), 200
        return { "message": "Hotel Not Found" }, 404

    def post(self, id_hotel):
        dados = Hotel.argumentos.parse_args() # Dicionario
        hotel_encontrado = HotelModel.find_hotel(id_hotel)
        if hotel_encontrado:
            return { "message": "Hotel with this id already exists"}
        novo_hotel = HotelModel(id_hotel,**dados)
        novo_hotel.save_hotel()
        return novo_hotel.json(), 200

    def put(self, id_hotel):
            dados = Hotel.argumentos.parse_args() # Dicionario
            hotel_encontrado = HotelModel.find_hotel(id_hotel)
            if hotel_encontrado:
                    hotel_atualizado = HotelModel(id_hotel, **dados)
                    hotel.atualizado.update_hotel(**dados)
                    hotel_atualizado.save_hotel()
                    return hotel_atualizado.json(), 200
            novo_hotel = { "hotel_id": id_hotel, **dados }
            hoteis.append(novo_hotel)
            return novo_hotel, 201 # Created

    def delete(self, id_hotel):
         global hoteis
         hoteis = [hotel for hotel in hoteis if hotel["hotel_id"] != id_hotel]
         return{ "message": f"Hotel with ID: {id_hotel} deleted"}