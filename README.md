# Campus to Career Platform
A Flask-based web application connecting students with companies for job and internship opportunities.

## Prerequisites
Before you begin, ensure you have the following installed on your system:
- **Python** (version 3.8 or higher)
- **Git**

## Step-by-Step Installation Guide

### 1. Clone the Repository
Open your terminal or command prompt and run the following command to download the project to your local machine:
```bash
git clone https://github.com/pranjalyt/campustocareer.git
cd campustocareer
```

### 2. Create a Virtual Environment (Recommended)
It's a best practice to create a virtual environment to keep the project's dependencies separate from your global Python installation.
```bash
# On macOS and Linux:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
With your virtual environment activated, install the required packages (like Flask and Werkzeug) using `pip`:
```bash
pip install -r requirements.txt
```

### 4. Initialize the Database (If required)
The project uses SQLite for the database (`campustocareer.db`). It might already have some initial data. If you ever need to reset or initialize it from scratch, you can run the provided script inside the `flask_app` folder:
```bash
cd flask_app
python init_db.py
cd ..
```
*(Skip this step if the `campustocareer.db` file already exists and you want to use the existing data).*

### 5. Run the Application
Start the Flask development server:
```bash
cd flask_app
python app.py
```
*(Or, from the root folder, you can run `python api/index.py` to test the Vercel entry setup).*

### 6. View the Site
Open your web browser and go to:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

---
### Note for Vercel Deployment
This repository is configured to deploy seamlessly to Vercel via the `api/index.py` serverless function and `vercel.json` routing configuration in the root directory.

*Note: Since Vercel runs in a serverless, read-only environment, local SQLite databases (`.db` files) will not persist updates after deployment. For a production environment on Vercel, consider migrating to a hosted database solution like PostgreSQL or Supabase.*
