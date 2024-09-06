from model.data import *

class TestsDB():

    def save_box(self):
        try:
            box = Box('test_name', 1, 1, 1, 1)
            cam_sec = CamSector.getLast()
            box.setCamSector(cam_sec)
            last_box = Box.getLast()
            return box.name == last_box.name
        except Exception:
            return False
    def save_camera(self):
        try:
            camera = Camera('test_route', 'test_name', [1,2,3], [4,5,6])
            camera.save()
            last_camera = Camera.getLast()
            return camera.name == last_camera.name
        except Exception:
            return False 
    def save_camera_sec(self):
        try:
            cam_sec = CamSector('test_name')
            cam_sec.save()
            last_cam_sec = CamSector.getLast()
            return cam_sec.name == last_cam_sec.name
        except Exception:
            return False
    
    def set_camera_sec_to_box(self):
        try:
            cam_sec = CamSector.getLast()
            box = Box.getLast()
            box.setCamSector(cam_sec)
            return cam_sec.id == box.cam_sector_id
        except Exception:
            return False
    def set_camera_sec_to_camera(self):
        try:
            cam_sec = CamSector.getLast()
            camera = Camera.getLast()
            camera.setCamSector(cam_sec)
            return cam_sec.id == camera.cam_sector_id
        except Exception:
            return False
    
    def get_all_cameras(self):
        try:
            camera = Camera.getAll()
            return len(camera) > 0
        except Exception:
            return False
    def get_all_camera_sectors(self):
        try:
            cam_sec = CamSector.getAll()
            return len(cam_sec) > 0
        except Exception:
            return False
    def get_all_boxes(self):
        try:
            box = Box.getAll()
            return len(box) > 0
        except Exception:
            return False
    
    def get_by_id_camera(self):
        try:
            camera = Camera.getLast()
            need_cam = Camera.getByID(camera.id)
            return camera.id == need_cam.id
        except Exception:
            return False
    def get_by_id_camera_sec(self):
        try:
            cam_sec = CamSector.getLast()
            need_cam_sec = CamSector.getByID(cam_sec.id)
            return cam_sec.id == need_cam_sec.id
        except Exception:
            return False
    def get_by_id_box(self):
        try:
            box = Box.getLast()
            need_box = Box.getByID(box.id)
            return box.id == need_box.id
        except Exception:
            return False
    
    def delete_camera(self):
        try:
            camera = Camera.getLast()
            camera.delete()
            try:
                return Camera.getLast().id != camera.id
            except AttributeError:
                return True
        except Exception:
            return False
    def delete_camera_sec(self):
        try:
            camera_sec = CamSector.getLast()
            camera_sec.delete()
            try:
                return CamSector.getLast().id != camera_sec.id
            except AttributeError:
                return True
        except Exception:
            return False
    def delete_box(self):
        try:
            box = Box.getLast()
            box.delete()
            try:
                return Box.getLast().id != box.id
            except AttributeError:
                return True
        except Exception:
            return False
    

    
