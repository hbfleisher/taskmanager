from core.kivybase import TaskApp
from core.settings import Session


def start_app():
    session = Session()
    app = TaskApp()
    app.run()
    session.close()

if __name__ == "__main__":
    start_app()
