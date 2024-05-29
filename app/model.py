import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler, LabelEncoder  

class Model():


    
    def prediction(file_path):
        def le(df):
            for col in df.columns:
                if df[col].dtype == 'object':
                    label_encoder = LabelEncoder()
                    df[col] = label_encoder.fit_transform(df[col])
            return df
        _data = pd.read_csv(file_path)
        data = _data.copy()

        selected_features=['duration','hot', 'count','protocol_type','service','src_bytes','dst_bytes','flag','land','wrong_fragment','urgent']

        newdata = data[selected_features]

        # Apply LabelEncoder to object columns
        newdata_encoded = le(newdata)

        # Scale the data using StandardScaler
        scale = StandardScaler()
        newdata_scaled = scale.fit_transform(newdata_encoded)

        # Load the model
        # dt_loaded = load('anomalie.pkl')
        with open('C:\\Users\\MKT\\Documents\\tfc\\crssri_app\\network-monitoring-system-with-ML\\anomalie.pkl', 'rb') as f:
            dt_loaded = pickle.load(f)

        predictions = dt_loaded.predict(newdata_scaled)
        _data['class'] = ['normal' if pred == 1 else 'anormal' for pred in predictions]
        return _data

