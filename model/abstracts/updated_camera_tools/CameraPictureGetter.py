from model.abstracts.updated_camera_tools.VideoCaptureHolder import VideoCaptureHolder
from model.data.Camera import Camera
from time import sleep
class CameraPictureGetter:
    """
    Это просто интерфейс для работы внутри этого \n
    приложения (но его легко интегрировать)
    """
    @classmethod
    def getPicture(cam: Camera):
        if cam.id:
            ch:VideoCaptureHolder = VideoCaptureHolder.getInstance()
            res = ch.addConnection(cam.id, cam.route)
            if res == 1 or res == 2:
                pic_res = ch.getPicture(cam.id)
                return pic_res[0], pic_res[1], 'ок'
            elif res == 3:
                sleep(0.2)
                res = ch.addConnection(cam.id, cam.route)
                if res == 1 or res == 2:
                    pic_res = ch.getPicture(cam.id)
                    return pic_res[0], pic_res[1], 'со второго раза, но ок'
                return False, None, 'повторное подключение не дало результатов, попробуй позже'
            elif res == 4:
                return False, None, 'еблан (ты) пытается запихнуть не тот route под существующим identifyer'
            else:
                return False, None, 'какой-то косяк'
        return False, None, 'ПОШЕЛ НАХУЙ, ID ПУСТОЙ'