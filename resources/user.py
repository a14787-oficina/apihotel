from flask_restful import Resource, reqparse
from models.user import UserModel
from hmac import compare_digest
from flask_jwt_extended import create_access_token, jwt_required


class User(Resource):
    
    def get(self, username):
        user_encontrado = UserModel.find_user(username)
        if user_encontrado:
            return user_encontrado.json(), 200
        return { "message": "User Not Found" }, 404

    
    @jwt_required()
    def delete(self, username):
        user_encontrado = UserModel.find_user(username)
        if user_encontrado:
            user_encontrado.delete_user()
            return{ "message": f"User with {username} deleted"}, 200
        return { "message": "User not found"}, 404

class UserRegister(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("usernme", type=str, help="Username Obrigatório")
    argumentos.add_argument("password", type=str, help="Password Obrigatória")


    def post(self):
        dados = UserRegister.argumentos.parse_args() # Dicionario
        user_encontrado = UserModel.find_user(dados["username"])
        if user_encontrado:
            return { "message": "User with this username already exists"}
        novo_user = UserModel(**dados)
        novo_user.save_user()
        return novo_user.json(), 200

class UserLogin(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("usernme", type=str, help="Username Obrigatório")
    argumentos.add_argument("password", type=str, help="Password Obrigatória")

    def post(self):
        dados = UserLogin.argumentos.parse_args()
        user = UserModel.find_user(dados["username"])

        if user and compare_digest(user.password,dados["password"]):
            token = create_access_token(identity=user.username)
            return { "access_token": token}
        return{ "message": "Username or password ivalid!"}


class UserLogout(Resource):
    ...