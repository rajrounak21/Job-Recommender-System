# app.py
from flask import Flask, render_template, request, redirect, url_for, session ,jsonify
import fitz
import os
from dotenv import load_dotenv
from apify_client import ApifyClient
from google.generativeai import GenerativeModel, configure
import tempfile
import shutil

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Configure AI models
configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = GenerativeModel("gemini-1.5-flash")
apify_client = ApifyClient(os.getenv("APIFY_API_TOKEN"))


# Helper functions (same as Streamlit version)
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def ask_gemini(prompt, max_token=1000):
    response = model.generate_content(
        contents=[{"role": "user", "parts": [{"text": prompt}]}],
        generation_config={
            "temperature": 0.3,  # Lower temperature for more focused results
            "max_output_tokens": max_token
        }
    )
    # Clean response
    return response.text.replace("*", "").replace("•", "").strip()

def fetch_linkedin_jobs(search_query, location="India", rows=60):
    run_input = {
        "title": search_query,
        "location": location,
        "rows": rows,
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"]
        }
    }
    run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
    jobs = list(apify_client.dataset(run['defaultDatasetId']).iterate_items())
    return jobs


# ... (same as Streamlit version)

def fetch_naukri_jobs(search_query, max_jobs=60):
    run_input = {
        "keyword": search_query,
        "maxJobs": max_jobs,
        "freshness": "all",
        "sortBy": "relevance",
        "experience": "all",
    }
    run = apify_client.actor("alpcnRV9YI9lYVPWk").call(run_input=run_input)
    jobs = list(apify_client.dataset(run['defaultDatasetId']).iterate_items())
    return jobs


# Routes
# app.py (additional routes)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file and file.filename.endswith('.pdf'):
            # Create temp directory
            temp_dir = tempfile.mkdtemp()
            file_path = os.path.join(temp_dir, file.filename)
            file.save(file_path)

            # Store results in session
            session['resume_text'] = extract_text_from_pdf(file_path)
            session['filename'] = file.filename
            session['file_size'] = round(os.path.getsize(file_path) / 1024, 1)
            session['temp_dir'] = temp_dir

            return redirect(url_for('index'))

    # Clear previous analysis when returning to index
    session.pop('summary', None)
    session.pop('gaps', None)
    session.pop('roadmap', None)

    return render_template('index.html',
                           filename=session.get('filename'),
                           file_size=session.get('file_size'))


@app.route('/delete', methods=['POST'])
def delete_file():
    # Cleanup session and temp files
    if 'temp_dir' in session:
        shutil.rmtree(session['temp_dir'])
        session.pop('temp_dir', None)
    session.pop('filename', None)
    session.pop('file_size', None)
    session.pop('resume_text', None)
    return jsonify({'status': 'success'}), 200


# app.py - Updated analyze route
import markdown
import bleach


@app.route('/analyze')
def analyze():
    if 'resume_text' not in session:
        return redirect(url_for('index'))

    resume_text = session['resume_text']

    try:
        # Get analysis from Gemini
        summary = ask_gemini(f"Summarize this resume:\n\n{resume_text}")
        gaps = ask_gemini(f"Analyze missing skills:\n\n{resume_text}")
        roadmap = ask_gemini(f"Suggest roadmap:\n\n{resume_text}")

        # Configure markdown conversion
        allowed_tags = ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'h3', 'h4']
        allowed_attributes = {}

        def safe_markdown(text):
            html = markdown.markdown(text)
            return bleach.clean(
                html,
                tags=allowed_tags,
                attributes=allowed_attributes,
                strip=True
            )

        # Convert and sanitize
        summary_html = safe_markdown(summary)
        gaps_html = safe_markdown(gaps)
        roadmap_html = safe_markdown(roadmap)

        # Cleanup temp files
        if 'temp_dir' in session:
            shutil.rmtree(session['temp_dir'])
            session.pop('temp_dir', None)

        return render_template('analysis.html',
                               summary=summary_html,
                               gaps=gaps_html,
                               roadmap=roadmap_html)

    except Exception as e:
        return f"Analysis error: {str(e)}", 500


@app.route('/jobs')
def get_jobs():
    # Get original resume text from session
    resume_text = session.get('resume_text')
    if not resume_text:
        return redirect(url_for('index'))

    # Extract keywords directly from resume text
    try:
        keyword_prompt = f"""
        Extract 5-7 most important job search keywords from this resume text.
        Focus on job titles, technical skills, and industries.
        Return ONLY comma-separated values, no explanations.

        RESUME TEXT:
        {resume_text[:3000]}  # Truncate to avoid token limits
        """

        keywords = ask_gemini(keyword_prompt)
        search_keywords = keywords.replace("\n", "").strip().lower()

        # Fetch jobs
        linkedin_jobs = fetch_linkedin_jobs(search_keywords)
        naukri_jobs = fetch_naukri_jobs(search_keywords)

        return render_template('jobs.html',
                               linkedin_jobs=linkedin_jobs,
                               naukri_jobs=naukri_jobs,
                               keywords=search_keywords)

    except Exception as e:
        return f"Job search error: {str(e)}", 500



if __name__ == '__main__':
    app.run(debug=True)