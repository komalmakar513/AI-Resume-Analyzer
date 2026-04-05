from flask import Flask, render_template, request
import PyPDF2

app = Flask(__name__)

# Required skills list
required_skills = [
    "python", "machine learning", "sql", "data structures",
    "communication", "git", "problem solving"
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    
    # File validation
    if 'resume' not in request.files:
        return "❌ No file uploaded"

    file = request.files['resume']

    if file.filename == '':
        return "❌ No selected file"

    if not file.filename.endswith('.pdf'):
        return "❌ Invalid file format! Please upload a PDF."

    # Read PDF safely
    try:
        pdf_reader = PyPDF2.PdfReader(file)
    except:
        return "❌ Error reading file. Please upload a valid PDF."

    # Extract text
    resume_text = ""
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            resume_text += text

    resume_text = resume_text.lower()

    # Skill analysis
    missing_skills = []
    for skill in required_skills:
        if skill not in resume_text:
            missing_skills.append(skill)

    # Suggestions
    suggestions = []

    if "project" not in resume_text:
        suggestions.append("Add projects to strengthen your resume")

    if "internship" not in resume_text:
        suggestions.append("Include internships or real-world experience")

    if "achievement" not in resume_text:
        suggestions.append("Mention achievements or certifications")

    # Score system
    score = 100 - (len(missing_skills) * 10)
    if score < 0:
        score = 0

    # Final result
    result = f"📊 Resume Score: {score}/100\n\n"

    if missing_skills:
        result += "🔴 Missing Skills:\n- " + "\n- ".join(missing_skills)
    else:
        result += "✅ Great! You have most required skills\n"

    if suggestions:
        result += "\n\n💡 Suggestions:\n- " + "\n- ".join(suggestions)

    return f"<pre>{result}</pre>"


if __name__ == '__main__':
    app.run(debug=True)