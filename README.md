# Medical Appointment No-Shows — Streamlit App

## Run locally
1. Install Python.
2. Open a terminal in this folder.
3. Install dependencies:
   `pip install -r requirements.txt`
4. Start the app:
   `streamlit run app.py`
5. Upload the CSV downloaded from Kaggle using the sidebar.

## Deploy
1. Create a GitHub repository.
2. Upload `app.py` and `requirements.txt`.
3. Open https://share.streamlit.io/ and sign in with GitHub.
4. Create an app and select the repository, branch, and `app.py`.
5. Deploy and copy the generated `*.streamlit.app` URL.

The app does not assume every dataset issue exists: it reports what it finds in the uploaded CSV.
