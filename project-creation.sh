touch .env
# .gitignore creation and its content
touch .gitignore
echo ".env" >> .gitignore
echo "venv/" >> .gitignore
echo ".DS_Store" >> .gitignore
echo "__pycache__/" >> .gitignore


touch requirements.txt

touch setup.py

# project directory creation
mkdir app
touch app/__init__.py
mkdir app/utils
touch app/utils/__init__.py
touch app/utils/image_handler.py
touch app/utils/celebrity_detector.py
touch app/utils/qa_engine.py
touch app/routes.py
mkdir static
mkdir templates
