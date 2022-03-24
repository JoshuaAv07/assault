from app.main import app

#runs the app using gunicorn server by using main.py
if __name__ == '__main__':
    app.run(load_dotenv=True)