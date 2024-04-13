from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import pytesseract
import re
import pandas as pd
from PyPDF2 import PdfFileReader
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')

# Function to extract email ID and contact number from text
def extract_info(text):
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
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']

        # If user does not select file, browser also submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file:
            # Save the uploaded file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Extract data from the uploaded file
            data = []
            cv_text = ''
            if file.filename.endswith('.pdf'):
                # Handle PDF files using PyPDF2
                with open(file_path, 'rb') as pdf_file:
                    pdf_reader = PdfFileReader(pdf_file)
                    for page_num in range(pdf_reader.numPages):
                        cv_text += pdf_reader.getPage(page_num).extractText()

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
            output_file = os.path.join(app.config['UPLOAD_FOLDER'], 'output.xlsx')
            df.to_excel(output_file, index=False)

            # Provide download link for the output file
            return redirect(url_for('download', file_name='output.xlsx'))

    # Render the upload form if no file is uploaded or on GET request
    return render_template('index.html')

@app.route('/download/<path:file_name>')
def download(file_name):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
