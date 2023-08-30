from flask import Flask, request, render_template, jsonify
import os
import pdfplumber
import re

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        resume_pdf = request.files['resume']
        if resume_pdf and resume_pdf.filename.endswith('.pdf'):
            resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_pdf.filename)
            resume_pdf.save(resume_path)

            resume_data = extract_resume_data(resume_path)
            return render_template('result.html', resume_data=resume_data)

    return render_template('index.html')

def extract_resume_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    extracted_data = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "education": extract_education(text),
        "experience": extract_experience(text)
        # ... other fields
    }

    return extracted_data

def extract_name(text):
    lines = text.split('\n')
    return lines[0].strip()

def extract_email(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    if match:
        return match.group()
    return ""

def extract_phone(text):
    phone_pattern = r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
    match = re.search(phone_pattern, text)
    if match:
        return match.group()
    return ""

def extract_education(text):
    education_pattern = r'Education[^\n]+'
    match = re.search(education_pattern, text, re.IGNORECASE)
    if match:
        return match.group()
    return ""

def extract_experience(text):
    experience_pattern = r'Experience[^\n]+'
    match = re.search(experience_pattern, text, re.IGNORECASE)
    if match:
        return match.group()
    return ""

if __name__ == '__main__':
    app.run(debug=True)
