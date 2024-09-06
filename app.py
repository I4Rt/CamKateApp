from config import *
from model.data import *
# from web_contollers import *
from model.abstracts.CameraApi import *

if __name__ == "__main__":

    # cam = Camera('route','name',[1,2,3],[4,5,6])
    # cam.save()
    # cam_last = Camera.getLast()
    # cam_last.delete()
    # cam_last1 = Camera.getLast()
    # print(cam_last1)
    # print(cam_last.id == cam_last1.id)

    with app.app_context():
        Base.metadata.create_all(e)
        app.run(host='0.0.0.0', port=4997, debug=True)
        
    