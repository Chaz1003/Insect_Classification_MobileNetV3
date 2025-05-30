import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import pickle

st.title("Insect Classifier")

# Load model
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("insect_classification_model.keras")
    with open("model_metadata.pkl", "rb") as f:
        class_indices = pickle.load(f)
    return model, class_indices

model, metadata = load_model()
class_indices = metadata["class_names"]

# debugging parameters
# st.write(class_indices)

# Create a list of class names
# class_names = [None] * len(class_indices)
# for idx, label in class_indices.items():
#     class_names[idx] = label
class_names = class_indices


# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Preprocess - THIS IS THE KEY FIX
    img = image.resize((224, 224))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    
    # Use EfficientNet preprocessing - same as in your training
    img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)

    # Predict
    prediction = model.predict(img_array)
    predicted_class_idx = np.argmax(prediction[0])
    predicted_class = class_names[predicted_class_idx]
    confidence = prediction[0][predicted_class_idx] * 100

    st.write(f"### Prediction: {predicted_class}")
    st.write(f"Confidence: {confidence:.2f}%")