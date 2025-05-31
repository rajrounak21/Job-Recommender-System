## 🧠 Job-Recommender-System

An AI-powered Resume Analyzer and Job Recommender System built using **Flask**, **Google Gemini**, and **Apify**. This application helps users:

* Analyze their resumes
* Identify missing skills or gaps
* Get a personalized career roadmap
* Find relevant job opportunities from **LinkedIn** and **Naukri.com**

---

### 🚀 Features

* 📄 **Resume Upload (PDF)**
* 🧠 **AI-Powered Resume Summary**
* 🚧 **Skill Gap & Improvement Analysis**
* 🚤️ **Career Roadmap Generation**
* 🔎 **Live Job Recommendations**
* 🔐 **Secure and Session-Based Workflow**
* 🖥️ **Clean and Simple Flask Frontend**

---

### 💠 Tech Stack

* **Backend**: Flask, Python
* **AI Integration**: Google Gemini (Gemini 1.5 Flash)
* **Job Scraping**: Apify actors for LinkedIn and Naukri
* **PDF Parsing**: PyMuPDF (`fitz`)
* **Environment Management**: `python-dotenv`
* **Security**: Flask session with `SECRET_KEY`

---

### 📸 Screenshots

| Resume Upload                                                     | Resume Summary & Skills Gap                                       |
| ----------------------------------------------------------------- | ----------------------------------------------------------------- |
| ![upload](https://via.placeholder.com/400x200?text=Upload+Resume) | ![analysis](https://via.placeholder.com/400x200?text=AI+Analysis) |

---

### ⚙️ Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/your-username/Job-Recommender-System.git
cd Job-Recommender-System
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Set Up `.env` File**

```
GOOGLE_API_KEY=your_google_api_key
APIFY_API_TOKEN=your_apify_token
SECRET_KEY=your_flask_secret_key
```

4. **Run the App**

```bash
python app.py
```

App will run at: `http://127.0.0.1:5000/`

---

### 📄 File Structure

```
├── app.py                 # Flask application
├── templates/             # HTML templates
│   ├── index.html
│   ├── analysis.html
│   └── jobs.html
├── static/                # Static assets (CSS, JS)
├── requirements.txt
└── .env                   # Environment variables (not tracked)
```

---

### 💡 Future Improvements

* Add user authentication
* Support DOCX resume formats
* Enhance UI with Bootstrap or Tailwind
* Store analysis history per user
* Integrate additional job portals (Indeed, Monster, etc.)

---

### 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

### 📜 License

MIT License
