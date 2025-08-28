python -m venv legal_ai_env
call legal_ai_env\Scripts\activate
pip install --upgrade pip
pip install streamlit fastapi uvicorn openai python-docx pandas pydantic python-multipart requests python-dotenv black flake8
echo ✅ Setup complete! Activate with: legal_ai_env\Scripts\activate
