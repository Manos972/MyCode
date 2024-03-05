from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import os

MSG_USER_PASS_REQUIRED = "Veuillez fournir un nom d'utilisateur et un mot de passe"
MSG_INVALID_USER_PASS = "Nom d'utilisateur ou mot de passe incorrect"
MSG_USER_NOT_FOUND = "Utilisateur introuvable"
MSG_ACCESS_DENIED = "Vous n'avez pas l'autorisation d'accéder à cette ressource"
PROTECTED_FILE_NAME = 'example.txt'
DEFAULT_SECRET = 'default_secret_key'

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', DEFAULT_SECRET)
jwt = JWTManager(app)
users = {
	"user1": {"password": generate_password_hash("password1"), "roles": ["admin"]},
	"user2": {"password": generate_password_hash("password2"), "roles": ["user"]}
	}


def authenticate_user (username, password):
	user_info = users.get(username, None)
	if user_info and check_password_hash(user_info['password'], password):
		return user_info
	return None


def get_user_role (user_info):
	return user_info['roles'][0] if user_info and 'roles' in user_info and user_info['roles'] else None


@app.route('/login', methods = ['POST'])
def login ():
	request_payload = request.json
	username = request_payload.get('username', None)
	password = request_payload.get('password', None)
	if not username or not password:
		return jsonify({"msg": MSG_USER_PASS_REQUIRED}), 400
	if not authenticate_user(username, password):
		return jsonify({"msg": MSG_INVALID_USER_PASS}), 401
	access_token = create_access_token(identity = username)
	return jsonify(access_token = access_token), 200


@app.route('/protected', methods = ['GET'])
@jwt_required()
def protected ():
	current_user = get_jwt_identity()
	user_info = users.get(current_user)
	if not user_info:
		return jsonify({"msg": MSG_USER_NOT_FOUND}), 404
	if 'admin' == get_user_role(user_info):
		with open(PROTECTED_FILE_NAME, 'r') as file:
			content = file.read()
			return jsonify(file_content = content), 200
	else:
		return jsonify({"msg": MSG_ACCESS_DENIED}), 403


if __name__ == '__main__':
	app.run(debug = True)
