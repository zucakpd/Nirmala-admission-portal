# Nirmala Admission Portal 🎓

Automates college admission merit calculation. Upload applicant data -> Get ranked merit list in seconds.

**The Problem**  
College staff manually calculate 400+ applications in Excel. It’s slow and error-prone during admission season.

**The Solution**  
A Flask web app for my BCA final year project. Staff upload a CSV, the system applies merit formulas, ranks candidates, and exports results.

## Live Demo
**App Link**: https://nirmala-admission-portal.onrender.com
**Login**: `Username: admin`  `Password: admin123` 

Note: This is a demo account with limited access for testing.

## Tech Stack
`Python` • `Flask` • `SQLite` • `HTML` • `CSS` 

## Run Locally
```bash
git clone https://github.com/yourusername/Nirmala-admission-portal.git
cd Nirmala-admission-portal

python -m venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
python app.py
