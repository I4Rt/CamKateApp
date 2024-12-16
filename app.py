from config import *
from model.data import *
from web_contollers import *
from model.abstracts.CameraApi import *
from model.abstracts.updated_camera_tools.CameraPictureGetter import *
from model.abstracts.updated_camera_tools.PictureCapture import *
from model.abstracts.DefectsThread import *
from tools import FullAnalize

if __name__ == "__main__":
    # MANAGER = Manager()
    # PictureCapture.setManager(MANAGER)
    # cam = Camera('route','name',[1,2,3],[4,5,6])
    # cam.save()
    # cam_last = Camera.getLast()
    # cam_last.delete()
    # cam_last1 = Camera.getLast()
    # print(cam_last1)
    # print(cam_last.id == cam_last1.id)

    with app.app_context():
        MANAGER = Manager()
        PictureCapture.setManager(MANAGER)
        # FullAnalize.run()
        # defectsThread = DefectsThread()
        # defectsThread.run()
        
        Base.metadata.create_all(e)
        app.run(host='0.0.0.0', port=4997, debug=True)
        
    