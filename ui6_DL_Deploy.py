import streamlit as st
import pytesseract
from PIL import Image
import re

# Configuration for Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
config = ('-l eng+sin+typew --oem 1 --psm 3')

# Function to extract information from image
def extract_information(image):
    # Extract text from the image
    text = pytesseract.image_to_string(image, config=config)
    text = text.lower()  # Convert text to lowercase for easier matching
    
    # Define regex patterns for information extraction
    name_pattern = r'(?<=\d,\d\. )(.+)'
    dl_id_pattern = r'5\. b([^\s]+)'
    nic_pattern = r'4a: (\d{9,12})'
    dob_pattern = r'3\. (\d{2}\.\d{2}\.\d{4})'
    address_pattern = r'8(.+)'

    # Extract information using regex patterns
    name_match = re.search(name_pattern, text)
    dl_id_match = re.search(dl_id_pattern, text)
    nic_match = re.search(nic_pattern, text)
    dob_match = re.search(dob_pattern, text)
    address_match = re.search(address_pattern, text)

    # Initialize variables to store extracted information
    name = name_match.group(1).strip().upper() if name_match else None
    dl_id = "B" + dl_id_match.group(1).upper() if dl_id_match else None
    nic = nic_match.group(1) if nic_match else None
    dob = dob_match.group(1) if dob_match else None
    address = address_match.group(1).strip().upper() if address_match else None

    return name, dl_id, nic, dob, address, text

# Streamlit app
st.title('Document Information Extractor')

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # Extract information from the uploaded image
    name, dl_id, nic, dob, address, extracted_text = extract_information(image)
    
    # Display extracted information
    if name:
        st.write("Name:", name)
    if dl_id:
        st.write("Driving License ID:", dl_id)
    if nic:
        st.write("NIC Number:", nic)
    if dob:
        st.write("Date of Birth:", dob)
    if address:
        st.write("Address:", address)
    
    # Button to display extracted text
    if st.button('Show Extracted Text'):
        st.write("Extracted Text:")
        st.write(extracted_text)
