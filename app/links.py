from flask import Blueprint, render_template, url_for,request,jsonify
from joblib import load
# from joblib import load
import pandas as pd
import os
# import pickle
from sklearn.preprocessing import StandardScaler, LabelEncoder

scale= StandardScaler()
my_blueprint = Blueprint('my_blueprint', __name__)
def le(df):
    for col in df.columns:
        if df[col].dtype=='object':
            label_encoder = LabelEncoder()
            df[col]= label_encoder.fit_transform(df[col])
@my_blueprint.route('/')
def index():
    return render_template('index.html')
@my_blueprint.route('/file', methods=['POST'])
def file():
    if request.method == 'POST':
        file=request.files['data_file']
        if file:
            # Ensure absolute path and create missing directories
            upload_dir = os.path.join(os.getcwd(), 'uploads')
            os.makedirs(upload_dir, exist_ok=True)

            # Save the uploaded file to the absolute path
            file_path = os.path.join(upload_dir, file.filename)
            file.save(file_path)
            if file_path.endswith('.txt') or file_path.endswith('.csv')  :
                data = pd.read_csv(file_path, sep=',')
                le(data)
                print(data)  # Apply LabelEncoder or any other processing
                selected_features=['protocol_type','service','flag','src_bytes','dst_bytes','count','same_srv_rate','diff_srv_rate','dst_host_srv_count','dst_host_same_srv_rate']
                newdata = data[selected_features]
                newdata=scale.fit_transform(newdata)
                dt_loaded = load('./crssri.joblib')
                predictions = dt_loaded.predict(newdata)
                print(newdata)
            else:
                return "Unsupported file format!"
            
    # return jsonify(predictions.tolist())

    return render_template('analyse.html', predictions=predictions)
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
    target_ip = "192.168.43.1/24"  # Specify the target IP range
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
@my_blueprint.route('/trafic')
def traffic():
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
