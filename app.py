from config import *
from model.data import *
from web_contollers import *

if __name__ == "__main__":
    with app.app_context():
        Base.metadata.create_all(e)
        app.run(host='0.0.0.0', port=4997, debug=True)
        