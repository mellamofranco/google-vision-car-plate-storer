"""
@author:Franco Mosquera Bonasorte
"""
import cv2
import sys
from skimage.io import imsave
import analisis
import configparser
from datetime import datetime, time
import time

config = configparser.ConfigParser()
config.read('config.ini')

start_time = datetime.strptime(config['main']['start_time'], '%H:%M:%S').time()
end_time = datetime.strptime(config['main']['end_time'], '%H:%M:%S').time()

#funcion de horario laboral
def horario_laboral(start_time, end_time, check_time=None):
    # hace el check de horario con config.ini y deuvleve true 
    check_time = check_time or datetime.now().time()
    if start_time < end_time:
        return start_time <= check_time <= end_time
    else:  # o false
        return check_time >= start_time or check_time <= end_time
    
def frame_processing(frame):
    # Mostramos el frame con el visor de OpenCV
    #cv2.imshow("video", frame)
    # Convertimos la imagen a RGB y la guardamos en un fichero(opecCV usa BGR)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    imsave("stills/"+f"frame_rgb_{round(time.time())}.jpg", frame_rgb)
    
    ##LLAMADA AL SCRIPT MAIN DONDE SE ANAIZA Y GUARDA EL FRAME--------------------------------
    analisis.main("stills/"+f"frame_rgb_{round(time.time())}.jpg")

def webcam_capture_test(camera_device):
    capture = cv2.VideoCapture(camera_device)
    #capture = cv2.VideoCapture("samples/1_.mp4")
    #capture.set(cv2.CAP_PROP_FPS, 30)
    #capture.set(cv2.CAP_PROP_BUFFERSIZE, 3)
    
    if not capture.isOpened():
        print("Cannot open source")
        return

    # TIEMPO ENTRE UNA CAPTURA Y OTRA
    recording_time = 3  # segundos

    #Bucle
    while True:
        if (horario_laboral(start_time, end_time)):
            print("captura en hora actual : ", datetime.now().time())
            ret, frame = capture.read()  # ret: (True/False)
            if ret:  # ret = False --> no hay frame capturado
                # procesamiento de frames
                frame_processing(frame)
                # 2000 ms --> espera 2 segundos
                key = cv2.waitKey(recording_time*1000) & 0xFF
                # bucle antes del tiempo establecido
                if key > 0 and chr(key) == "q":
                    break
        # liberar cámara
    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
	camera_device = 0
	if (len(sys.argv) > 1):
		camera_device = int(sys.argv[1])
	webcam_capture_test(camera_device)
