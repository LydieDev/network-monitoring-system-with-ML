# import requests

# def connect_to_router(username, password, router_ip):
#     auth_response = requests.get(f'http://{router_ip}/login/{username}/{password}')
#     if auth_response.status_code == 200:
#         auth_token = auth_response.json().get('token')
#         return auth_token
#     else:
#         print('Échec de l\'authentification.')
#         return None

# def block_mac_address(auth_token, router_ip, mac_address):
#     headers = {
#         'Authorization': f'Bearer {auth_token}'
#     }
#     block_data = {
#         'mac_address': mac_address
#     }
#     block_response = requests.post(f'http://{router_ip}/block-mac', headers=headers, json=block_data)

#     if block_response.status_code == 200:
#         print(f'Adresse MAC {mac_address} bloquée avec succès.')
#     else:
#         print('Échec du blocage de l\'adresse MAC.')

# if __name__ == '__main__':
#     router_ip = '127.0.0.1:5000'  # Remplacez par l'adresse IP et port de votre serveur Flask
#     username = 'admin'  # Remplacez par le nom d'utilisateur
#     password = 'password'  # Remplacez par le mot de passe

#     auth_token = connect_to_router(username, password, router_ip)
#     if auth_token:
#         mac_address_to_block = '00:11:22:33:44:55'  # Remplacez par l'adresse MAC à bloquer
#         block_mac_address(auth_token, router_ip, mac_address_to_block)


from flask import Blueprint, request, jsonify
import requests

my_blueprint = Blueprint('my_blueprint', __name__)

def connect_to_router(username, password, router_ip):
    # Exemple de connexion au routeur pour obtenir un jeton d'authentification
    auth_data = {
        'username': username,
        'password': password
    }
    auth_response = requests.post(f'http://{router_ip}/login', json=auth_data)

    if auth_response.status_code == 200:
        auth_token = auth_response.json().get('token')
        return auth_token
    else:
        print('Échec de l\'authentification.')
        return None

def block_mac_address(auth_token, router_ip, mac_address):
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    block_data = {
        'mac_address': mac_address
    }
    block_response = requests.post(f'http://{router_ip}/block-mac', headers=headers, json=block_data)

    if block_response.status_code == 200:
        print(f'Adresse MAC {mac_address} bloquée avec succès.')
        return True
    else:
        print('Échec du blocage de l\'adresse MAC.')
        return False

@my_blueprint.route('/login/<user>/<passw>/<mac>', methods=['POST', 'GET'])
def login(user, passw,mac):
    # data = request.form
    if user == 'admin' and passw == 'password':
        auth_token = connect_to_router(user, passw, '192.168.1.1')  # Remplacez par l'adresse IP de votre routeur
        if auth_token:
            mac_address_to_block = mac # Remplacez par l'adresse MAC à bloquer
            success = block_mac_address(auth_token, '192.168.1.1', mac_address_to_block)  # Remplacez par l'adresse IP de votre routeur
            if success:
                return jsonify({'message': f'Authentification réussie et Adresse MAC bloquée avec succès'}), 200
            else:
                return jsonify({'error': 'Erreur lors du blocage de l\'adresse MAC'}), 500
        else:
            return jsonify({'error': 'Échec de l\'authentification'}), 401
    else:
        return jsonify({'error': 'Authentification échouée'}), 401

@my_blueprint.route('/block-mac', methods=['POST'])
def block_mac():
    # Ce endpoint ne sera pas utilisé directement ici, car le blocage est géré dans le endpoint de login
    return jsonify({'error': 'Endpoint non utilisé pour le blocage MAC'}), 404

# Exemple d'utilisation de la blueprint dans une application Flask
# from flask import Flask
# app = Flask(__name__)
# app.register_blueprint(my_blueprint)
# if __name__ == '__main__':
#     app.run(debug=True)


######################################################

from flask import request, jsonify, session
from your_module_name import connect_to_router, block_mac_address

# Définissez votre blueprint ou utilisez l'objet app directement

@my_blueprint.route('/login/<username>/<password>/<router_ip>', methods=['GET'])
def login(username, password, router_ip):
    # Établir la connexion avec le routeur pour obtenir le jeton d'authentification
    auth_token = connect_to_router(username, password, router_ip)
    if auth_token:
        # Stocker le jeton d'authentification dans la session de l'utilisateur (ou autre méthode de stockage)
        session['auth_token'] = auth_token
        return jsonify({'message': 'Authentification réussie'}), 200
    else:
        return jsonify({'error': 'Échec de l\'authentification'}), 401

@my_blueprint.route('/block-mac/<mac_address>', methods=['POST'])
def block_mac(mac_address):
    # Vérifier si l'utilisateur est authentifié en récupérant le jeton d'authentification de la session
    auth_token = session.get('auth_token')
    if not auth_token:
        return jsonify({'error': 'Authentification requise'}), 401

    # Récupérer d'autres informations nécessaires à partir de la session ou d'une autre source sécurisée
    username = session.get('username')
    password = session.get('password')
    router_ip = session.get('router_ip')

    # Utiliser le jeton d'authentification pour bloquer l'adresse MAC
    block_mac_address(auth_token, router_ip, mac_address)
    return jsonify({'message': f'Adresse MAC {mac_address} bloquée avec succès'}), 200

##########################################################