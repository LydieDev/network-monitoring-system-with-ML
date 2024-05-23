import pickle
import numpy as np

# Define the custom dtype to match the expected dtype
custom_dtype = np.dtype([
    ('left_child', '<i8'),
    ('right_child', '<i8'),
    ('feature', '<i8'),
    ('threshold', '<f8'),
    ('impurity', '<f8'),
    ('n_node_samples', '<i8'),
    ('weighted_n_node_samples', '<f8'),
    ('missing_go_to_left', 'u1')  # Add the missing field with an appropriate dtype
])

try:
    # Load the pickle file with the custom dtype
    with open('anomalie.pkl', 'rb') as f:
        node_array = np.load(f, allow_pickle=True).astype(custom_dtype)
except Exception as e:
    print(f"Error loading the model: {e}")
    # Handle the error appropriately, such as logging or raising an exception
else:
    print("Model loaded successfully")
    # Proceed with using the loaded model
