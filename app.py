from flask import Flask, render_template, request
import PyPDF2

app = Flask(__name__)

skills_db = ["python", "java", "c++", "machine learning", "sql", "html", "css", "javascript"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['resume']

    if file.filename == '':
        return "No file uploaded"

    if not file.filename.endswith('.pdf'):
        return "Invalid file format (Only PDF allowed)"

    pdf_reader = PyPDF2.PdfReader(file)
    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text().lower()

    present = []
    missing = []

    for skill in skills_db:
        if skill in text:
            present.append(skill)
        else:
            missing.append(skill)

    suggestions = ""
    if missing:
        suggestions = "Try to learn: " + ", ".join(missing)
    else:
        suggestions = "Great! Your resume looks strong 🚀"

    return render_template("result.html",
                           present_skills=", ".join(present),
                           missing_skills=", ".join(missing),
                           suggestions=suggestions)

if __name__ == "__main__":
    app.run(debug=True)