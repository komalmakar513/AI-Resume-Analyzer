from flask import Flask, render_template, request
import PyPDF2

app = Flask(__name__)

def extract_text(file):
    pdf = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text.lower()

def analyze_resume(text):
    skills_list = ["python", "java", "c++", "html", "css", "javascript"]

    found_skills = []
    score = 0

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)
            score += 15

    return score, found_skills

@app.route("/", methods=["GET", "POST"])
def index():
    score = None
    skills = None

    if request.method == "POST":
        file = request.files["resume"]
        text = extract_text(file)
        score, skills = analyze_resume(text)

    return render_template("index.html", score=score, skills=skills)

if __name__ == "__main__":
    app.run(debug=True)