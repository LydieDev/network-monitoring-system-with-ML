from flask import Blueprint, render_template, url_for,request,jsonify
import pickle

from model import Model
# from joblib import load
import pandas as pd
import os
import csv
import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle
from flask import Flask, request, render_template, jsonify

# import pickle
from sklearn.preprocessing import StandardScaler, LabelEncoder
import requests
import os
from scapy.all import sniff, wrpcap
def open_file(filename):
    data=[]
    with open(filename, mode='r') as file:
        lecteur=csv.DictReader(file)
        for line in lecteur:
            data.append(line)
    return data
def total(file,champ):
    compte={}
    for l in file:
        val=l[champ]
        compte[val]=compte.get(val,0)+1
    return compte
def capp():
    def packet_callback(packet):
    # Callback function to process each captured packet
    # You can customize this function to extract specific information from the packets
        p=packet.summary()

# Spécifiez le nom de l'interface réseau que vous souhaitez capturer
    interface_name = "Wi-Fi 3"  # Remplacez par le nom de votre interface

    # Set the file path to the user's home directory
    # file_path = os.path.expanduser("capture.pcap")

    # Print a message indicating the start of the script
    print("Script execution started.")

    # Print a message indicating the start of packet capture
    print(f"Starting packet capture on interface: {interface_name}...")

    try:
        # Perform packet capture on the specified interface and save to the specified file
        sniffed_packets = sniff(iface=interface_name, prn=packet_callback, store=1, count=1000000)  # Adjust count as needed
        # wrpcap(file_path, sniffed_packets)
        # print(f"Captured packets are saved to: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return sniffed_packets
# Print a message indicating the end of the script
# print("Script execution complete.")
def connect_to_router(router_ip,user,passw):
    auth_response = requests.get(f'http://{user}/{passw}/{router_ip}')
    if auth_response.status_code == 200:
        auth_token = auth_response
        return auth_response
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
    else:
        print('Échec du blocage de l\'adresse MAC.')
scale= StandardScaler()
my_blueprint = Blueprint('my_blueprint', __name__)
def le(df):
    for col in df.columns:
        if df[col].dtype == 'object':
            label_encoder = LabelEncoder()
            df[col] = label_encoder.fit_transform(df[col])
    return df
@my_blueprint.route('/')
def index():
    return render_template('index.html')
@my_blueprint.route('/file', methods=['POST'])

def file():
    predictions = None  # Initialize predictions variable
    
    if request.method == 'POST':
        file = request.files['data_file']
        
        if file:
            # Ensure absolute path and create missing directories
            upload_dir = os.path.join(os.getcwd(), 'uploads')
            os.makedirs(upload_dir, exist_ok=True)

            # Save the uploaded file to the absolute path
            file_path = os.path.join(upload_dir, file.filename)
            file.save(file_path)
            if file_path.endswith('.txt') or file_path.endswith('.csv'):
               predict = Model.prediction(file_path)
               predict = predict['protocol_type'].to_frame()

               print(predict)
            else:
                return "Unsupported file format!"

    return render_template('analyse.html',predictions=[predict.to_html(classes='data')])

@my_blueprint.route('/users')
def users():
    from scapy.all import ARP, Ether, srp

    def scan_network(ip):
        arp_request = ARP(pdst=ip)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")  # Broadcast MAC address
        packet = ether / arp_request
        result = srp(packet, timeout=3, verbose=False)[0]

        devices = []
        for sent, received in result:
            devices.append({'ip': received.psrc, 'mac': received.hwsrc})
        return devices

# Example usage:
    target_ip = "192.168.0.1/24"  # Specify the target IP range
    connected_devices = scan_network(target_ip)
    for device in connected_devices:
        print(f"IP Address: {device['ip']}, MAC Address: {device['mac']}")

    return render_template('users.html',devices=connected_devices)
@my_blueprint.route('/band')
def band():
    return render_template('band.html')
@my_blueprint.route('/analyse')
def analyse():
    return render_template('analyse.html')
from flask import Flask, request, jsonify

app = Flask(__name__)
blocked_macs = set()

@my_blueprint.route('/login/<ip>/<u>/<p>', methods=['POST', 'GET'])
def login(ip,u,p):
    a=connect_to_router(ip,u,p)
    return jsonify({'success': f'token  {a}'})
    # # data = request.form
    # if user == 'admin' and passw == 'admin':
    # # if data['username'] == 'admin' and data['password'] == 'password':
    #     return jsonify({'token': 'fake_token'}), 200
    # else:
    #     return jsonify({'error': 'Authentification échouée'}), 401

@my_blueprint.route('/block-mac', methods=['POST'])
def block_mac():
    auth_token = request.headers.get('Authorization')
    if auth_token != 'Bearer fake_token':
        return jsonify({'error': 'Authentification requise'}), 401

    data = request.json
    mac_address = data.get('mac_address')
    if mac_address:
        blocked_macs.add(mac_address)
        return jsonify({'message': f'Adresse MAC {mac_address} bloquée avec succès'}), 200
    else:
        return jsonify({'error': 'Adresse MAC non fournie'}), 400

@my_blueprint.route('/trafic')
def traffic():
    # p=open_file('output_file.csv')
    # ip=total(p,'class')
    return render_template('trafic.html')
@my_blueprint.route('/alert')
def charts():
    return render_template('alert.html')
@my_blueprint.route('/about')
def about():
    return render_template('about.html')
@my_blueprint.route('/setting')
def setting():
    return render_template('setting.html')
