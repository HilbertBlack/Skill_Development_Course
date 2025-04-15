# Install required packages
!pip install gradio PyMuPDF transformers --quiet

import gradio as gr
import fitz  # PyMuPDF
import re
import time
from transformers import pipeline

# Load a basic zero-shot classifier to assist analysis
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Extract text from uploaded PDF file
def extract_text_from_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

# Analyze resume content and return suggestions
def analyze_resume(file, progress=gr.Progress(track_tqdm=True)):
    progress(0, desc="Reading resume...")
    resume_text = extract_text_from_pdf(file.name)
    time.sleep(1)
    progress(0.2, desc="Analyzing content...")

    suggestions = []

    # Basic checks (can be expanded!)
    if len(resume_text.split()) < 150:
        suggestions.append("❌ Resume seems too short. Aim for at least 300 words.")

    if not re.search(r"(summary|objective)", resume_text, re.IGNORECASE):
        suggestions.append("📝 Add a professional summary or career objective at the top.")

    if not re.search(r"(skills)", resume_text, re.IGNORECASE):
        suggestions.append("💡 Include a 'Skills' section to highlight your technical and soft skills.")

    if not re.search(r"(experience|work history)", resume_text, re.IGNORECASE):
        suggestions.append("💼 Add a 'Work Experience' section with relevant accomplishments.")

    if not re.search(r"(education)", resume_text, re.IGNORECASE):
        suggestions.append("🎓 Don't forget to include your 'Education' section.")

    progress(0.5, desc="Checking job readiness...")

    # Optional: use AI to suggest improvements
    labels = ["well-structured", "needs more keywords", "poor formatting", "lacks clarity", "excellent resume"]
    classification = classifier(resume_text, candidate_labels=labels)

    top_label = classification['labels'][0]
    if top_label == "needs more keywords":
        suggestions.append("🔍 Try including more job-specific keywords and technologies.")
    elif top_label == "poor formatting":
        suggestions.append("📄 Improve formatting: use bullet points, consistent fonts, and sections.")
    elif top_label == "lacks clarity":
        suggestions.append("✏️ Rewrite some sections to improve clarity and flow.")
    elif top_label == "excellent resume":
        suggestions.append("✅ Your resume looks strong! Just ensure it's tailored to the job you're applying for.")

    progress(1.0, desc="Done!")

    return "\n\n".join(suggestions)

# Gradio interface
resume_analyzer = gr.Interface(
    fn=analyze_resume,
    inputs=gr.File(label="Upload your resume (PDF)"),
    outputs=gr.Textbox(label="AI Suggestions for Improvement", lines=15),
    title="AI Resume Analyzer",
    description="Upload a PDF resume. The AI will analyze it, show progress, and give actionable feedback."
)

resume_analyzer.launch()
