from config import *
from model.data import *
from tools.CameraSettings import CameraSettings
# from web_contollers import *
import numpy as np

if __name__ == "__main__":

    # matrix, coefs = CameraSettings.get_coefs('images/camera_settings_imgs', (7,7))
    # cam = Camera('1', '1', matrix, coefs)
    # cam.save()

    cam = Camera.getLast()
    matrix, coefs = cam.getCorrectValues()
    print(matrix, coefs)
    
    CameraSettings.get_correct_img('images/camera_settings_imgs', 'images/ready_data', cam, True)



    # with app.app_context():
    #     Base.metadata.create_all(e)
    #     app.run(host='0.0.0.0', port=4997, debug=True)


        