
from transformers import pipeline
import gradio as gr

# Load the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Function to summarize input text
def summarize_text(article):
    if len(article.strip()) == 0:
        return "Please enter an article to summarize."
    
    # Transformers models may have a token limit, so we handle long text carefully
    try:
        summary = summarizer(article, max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"Error: {str(e)}"

# Create Gradio interface
interface = gr.Interface(
    fn=summarize_text,
    inputs=gr.Textbox(lines=15, label="Enter Article Text"),
    outputs=gr.Textbox(label="Summary"),
    title="Article Summarizer",
    description="Paste your article text and get a concise summary using BART model."
)

interface.launch()
