from core.settings import Session

def start_app():
    session = Session()
    # Your application logic here
    session.close()