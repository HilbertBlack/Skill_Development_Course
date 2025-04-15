
from transformers import pipeline
from newspaper import Article
import gradio as gr
import textwrap
import time

# Load summarizer
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")  # faster model

# Chunk long text into smaller pieces
def chunk_text(text, max_chunk_words=600):
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len((current_chunk + sentence).split()) < max_chunk_words:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

# Extract article text from URL
def get_article_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        return f"Error fetching article: {str(e)}"

# Main summarization function with progress
def summarize_input(input_text_or_url, progress=gr.Progress(track_tqdm=True)):
    input_text_or_url = input_text_or_url.strip()

    if input_text_or_url.startswith("http"):
        article_text = get_article_text(input_text_or_url)
        if article_text.startswith("Error"):
            return article_text
    else:
        article_text = input_text_or_url

    if len(article_text.split()) < 50:
        return "Please provide a longer article (50+ words)."

    chunks = chunk_text(article_text)
    total = len(chunks)

    full_summary = ""

    for i, chunk in enumerate(progress.tqdm(chunks, desc="Summarizing")):
        try:
            summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
            full_summary += f"Part {i+1}/{total}:\n{summary}\n\n"
        except Exception as e:
            full_summary += f"Error summarizing part {i+1}: {str(e)}\n\n"
        time.sleep(0.1)  # Optional: simulate processing delay

    return full_summary.strip()

# Gradio interface
interface = gr.Interface(
    fn=summarize_input,
    inputs=gr.Textbox(lines=6, label="Enter article text or URL (up to ~10,000 words)"),
    outputs=gr.Textbox(lines=20, label="AI Summary"),
    title="Long Article Summarizer with Progress",
    description="Paste article text or a URL. This AI handles long content, shows progress, and returns summaries by section."
)

interface.launch()
