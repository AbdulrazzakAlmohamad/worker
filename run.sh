sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export flask=app.py  && flask run 
gunicorn --bind 0.0.0.0:5000 wsgi:app

# you can run the following command for showing list of routes
# flask routes