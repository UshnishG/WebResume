from flask import Flask, request, render_template, jsonify
import fitz  # PyMuPDF
import openai
import os

app = Flask(__name__)

# Function to extract text from PDF using PyMuPDF
def extract_text_from_pdf(pdf_file):
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

# Function to generate HTML resume using OpenAI API
def generate_html_resume(pdf_text, api_key):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="gpt-4",  # Ensure you are using the correct engine
        prompt=f"""You are an expert at generating HTML. Convert the following resume text into a clean, modern HTML format using best practices:
        
        1. Use semantic HTML5 elements like <header>, <main>, <section>, and <footer>.
        2. Include sections for Contact Information, Summary, Experience, Education, Skills, and Projects.
        3. Ensure proper headings for sections (e.g., <h1> for the name, <h2> for each section title).
        4. Format the content using basic CSS styles. Use a modern font (e.g., Arial or Roboto), and ensure the layout is responsive.
        5. For the CSS, include styling for margins, padding, fonts, and alignment to create a visually appealing resume.
        6. Ensure the contact information is at the top, and each section is clearly separated.
        7. Format dates, job titles, and company names clearly.
        8. For links (e.g., LinkedIn or GitHub), make them clickable.
        
        Here's the resume text:
        {pdf_text}
        """,
        max_tokens=3000
    )
    return response.choices[0].text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-html', methods=['POST'])
def generate_html():
    api_key = request.form['apiKey']
    pdf_file = request.files['pdfFile']

    # Extract text from the PDF
    pdf_text = extract_text_from_pdf(pdf_file)

    # Generate HTML resume using OpenAI API
    html_resume = generate_html_resume(pdf_text, api_key)

    # Save the generated HTML resume to a file
    with open("resume.html", "w") as html_file:
        html_file.write(html_resume)

    return jsonify({'success': True, 'htmlResume': html_resume})

if __name__ == '__main__':
    app.run(debug=True)
