import numpy as np
import cv2
import glob


class CameraSettings():

    @classmethod
    def get_coefs(cls, imgs_path, cells):
        args = {'--square_size': 1.0}
        img_mask = f'{imgs_path}/*.png'
        img_names = glob.glob(img_mask)
        square_size = float(args.get('--square_size'))

        pattern_size = cells # example: (7, 7) -- cells_x - 1, cells_y - 1
        pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
        pattern_points[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
        pattern_points *= square_size

        obj_points = []
        img_points = []
        h, w = 0, 0
        print(f'img_names \n {img_names}')
        for fn in img_names:
            print('processing %s... ' % fn, end='')
            img = cv2.imread(fn, 0)
            
            if img is None:
                print("Failed to load", fn)
                continue

            h, w = img.shape[:2]
            found, corners = cv2.findChessboardCorners(img, pattern_size)
            if found:
                term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
                cv2.cornerSubPix(img, corners, (5, 5), (-1, -1), term)

            if not found:
                print('chessboard not found')
                continue

            img_points.append(corners.reshape(-1, 2))
            obj_points.append(pattern_points)

            print('ok')

        # print(obj_points, img_points)

        rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, (w, h), None, None)

        print("\nRMS:", rms)
        print("camera matrix:\n", camera_matrix)
        print("distortion coefficients: ", dist_coefs.ravel())
        return camera_matrix.tolist(), dist_coefs.tolist()

    @classmethod
    def get_correct_img(cls, imgs_path, save_path, camera, show_img=False):
        img_names_undistort = [img for img in glob.glob(f"{imgs_path}/*.png")]
        save_path = f'{save_path}/'

        camera_matrix, dist_coefs = camera.getCorrectValues()
        camera_matrix = np.array(camera_matrix)
        dist_coefs = np.array(dist_coefs)

        print(camera_matrix)

        i = 0

        while i < len(img_names_undistort):
            img = cv2.imread(img_names_undistort[i])
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            h,  w = img.shape[:2]
            newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coefs, (w, h), 1, (w, h))

            dst = cv2.undistort(img, camera_matrix, dist_coefs, None, newcameramtx)

            dst = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)

            x, y, w, h = roi
            dst = dst[y:y+h, x:x+w]

            name = img_names_undistort[i].split("\\")
            name = name[-1].split(".")
            name = name[0]
            full_name = save_path + name + '.jpg'

            if show_img:
                imS = cv2.resize(dst, (960, 540)) 
                cv2.imshow('1', imS)
                cv2.waitKey(0)

            print('Undistorted image written to: %s' % full_name)
            cv2.imwrite(full_name, dst)
            i = i + 1