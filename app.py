from flask import Flask, render_template, request, send_file
import os
import pytesseract
import regex as re
import pandas as pd
from PIL import Image
from PyPDF2 import PdfReader

app = Flask(__name__)

# Path to the folder containing CVs
cv_folder = 'Sample'
output_file = 'output.xlsx'

# Function to extract email ID and contact number from text
def extract_info(text):
    # Regular expressions to match email and phone number patterns
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'(\+\d{1,2}\s?)?(\d{10}|\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'

    email_match = re.search(email_pattern, text)
    phone_match = re.search(phone_pattern, text)

    email = email_match.group() if email_match else ''
    phone = phone_match.group() if phone_match else ''

    return email, phone

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle file upload
        file = request.files['file']
        if file.filename != '':
            # Save the uploaded file
            file_path = os.path.join(cv_folder, file.filename)
            file.save(file_path)

            # Extract data from the uploaded file
            data = []
            cv_text = ''
            if file.filename.endswith('.pdf'):
                # Handle PDF files using PyPDF2
                pdf_reader = PdfReader(file_path)
                for page_num in range(len(pdf_reader.pages)):
                    cv_text += pdf_reader.pages[page_num].extract_text()

            elif file.filename.endswith(('.jpg', '.png')):
                # Handle image files using Tesseract OCR
                cv_text = pytesseract.image_to_string(Image.open(file_path))

            # Extract email ID and contact number
            email, phone = extract_info(cv_text)

            # Append extracted data to list
            data.append({'CV Name': file.filename, 'Email ID': email, 'Contact No.': phone, 'Text': cv_text})

            # Create DataFrame from the list of dictionaries
            df = pd.DataFrame(data)

            # Export DataFrame to Excel
            df.to_excel(output_file, index=False)

            # Provide download link for the output file
            return render_template('output.html', file_name=output_file)

    # Render the upload form if no file is uploaded or on GET request
    return render_template('index.html')

@app.route('/download')
def download():
    # Provide download link for the output file
    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
