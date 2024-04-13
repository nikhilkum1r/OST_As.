
### CV Data Extraction Web App

This is a Flask web application that allows users to upload CV files PDF to extract email IDs, contact numbers, and text from them.

## Features

- Supports uploading CV files in PDF, JPG, or PNG format.
- Uses PyPDF2 for PDF file handling and Tesseract OCR for image file handling.
- Extract email IDs and contact numbers from the uploaded CVs.
- Saves extracted data to an Excel file for download.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nikhilkum1r/OST_As..git
   ```

2. Navigate to the project directory:
   ```bash
   cd OST_As.
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Flask app:
   ```bash
   python app.py
   ```

2. Access the web app in your browser at `http://localhost:5003`.

3. Upload a CV file (PDF, JPG, or PNG) and click the "Upload" button.

4. Wait for the extraction process to complete, and then download the output Excel file.

## File Structure

- `app.py`: Flask application code.
- `templates/`: HTML templates for the web app.
- `static/uploads/`: Directory to store uploaded files.
- `requirements.txt`: Python package dependencies.

## Dependencies

- Flask
- PyPDF2
- pandas
- Pillow
- pytesseract
- regex

## Screenshots


## License



## Contributions

Contributions are welcome! If you encounter any issues or have suggestions, please open an issue or submit a pull request.
```

Feel free to customize this template to fit your project's specific details, such as adding screenshots, updating installation instructions, or providing more information about how to use the web app.
