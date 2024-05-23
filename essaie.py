import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler, LabelEncoder  

def prediction(file_path):
    def le(df):
        for col in df.columns:
            if df[col].dtype == 'object':
                label_encoder = LabelEncoder()
                df[col] = label_encoder.fit_transform(df[col])
        return df
    data = pd.read_csv(file_path)

    selected_features = ['protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'count','same_srv_rate', 'diff_srv_rate', 'dst_host_srv_count', 'dst_host_same_srv_rate']
    newdata = data[selected_features]

    # Apply LabelEncoder to object columns
    newdata_encoded = le(newdata)

    # Scale the data using StandardScaler
    scale = StandardScaler()
    newdata_scaled = scale.fit_transform(newdata_encoded)

    # Load the model
    # dt_loaded = load('anomalie.pkl')
    with open('anomalie.pkl', 'rb') as f:
        dt_loaded = pickle.load(f)

    # Make predictions using the loaded model
    predictions = dt_loaded.predict(newdata_scaled)
    print(predictions)
    return predictions

tableau = prediction("captured_traffic.csv")


_data=pd.read_csv('captured_traffic.csv', sep=',')
txt_data = _data.copy()
# test=pd.read_csv('./dataset/testData.txt',sep=',')
# Affichage du contenu du fichier texte
# print(txt_data)

def le(df):
    for col in df.columns:
        if df[col].dtype=='object':
            label_encoder = LabelEncoder()
            df[col]= label_encoder.fit_transform(df[col])
le(txt_data)
_data['class'] = ['normal' if pred == 1 else 'anormal' for pred in tableau]
#output_data = pd.concat([_data, pd.DataFrame({'class': _data['class']})], axis=1)
print(_data)