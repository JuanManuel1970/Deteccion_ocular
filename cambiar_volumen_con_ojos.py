import cv2
import mediapipe as mp
import screen_brightness_control as sbc  # Control de brillo
import pycaw.pycaw as pycaw  # Control de volumen
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import os


# Inicializar Mediapipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Detectar el índice correcto de la cámara
cam_index = None
for i in range(5):  
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
    if cap.isOpened():
        print(f"✅ Cámara encontrada en índice {i}")
        cam_index = i
        cap.release()
        break
else:
    print("❌ No se encontró ninguna cámara.")
    exit()

# Capturar video desde la webcam 
cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)

# Índices de los puntos de referencia de los ojos
OJOS_DER = [374, 386]  # Párpado superior e inferior del ojo derecho
OJOS_IZQ = [145, 159]  # Párpado superior e inferior del ojo izquierdo

# Configurar control de volumen del sistema (Windows)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Obtener volumen actual
vol_inicial = volume.GetMasterVolumeLevelScalar()  # Valor entre 0.0 y 1.0


pos_y_inicial = None  # Se calibrará con la primera detección

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb_frame)

    if result.multi_face_landmarks:
        for face_landmarks in result.multi_face_landmarks:
            # Obtener posición promedio de los ojos
            ojo_derecho = (face_landmarks.landmark[OJOS_DER[0]].y + face_landmarks.landmark[OJOS_DER[1]].y) / 2
            ojo_izquierdo = (face_landmarks.landmark[OJOS_IZQ[0]].y + face_landmarks.landmark[OJOS_IZQ[1]].y) / 2
            pos_y = (ojo_derecho + ojo_izquierdo) / 2  # Promedio de ambos ojos

            # Calibrar posición inicial en el primer frame
            if pos_y_inicial is None:
                pos_y_inicial = pos_y
                continue

            # Determinar cambio relativo de posición de los ojos
            diferencia = pos_y - pos_y_inicial

            # Control de volumen basado en la diferencia de posición
            if diferencia < -0.02:  # Si los ojos están más arriba de lo normal, sube volumen
                nuevo_volumen = min(vol_inicial + 0.05, 1.0)
                volume.SetMasterVolumeLevelScalar(nuevo_volumen, None)
                print(f"🔊 Subiendo volumen: {int(nuevo_volumen * 100)}%")
                vol_inicial = nuevo_volumen

            elif diferencia > 0.02:  # Si los ojos están más abajo de lo normal, baja volumen
                nuevo_volumen = max(vol_inicial - 0.05, 0.0)
                volume.SetMasterVolumeLevelScalar(nuevo_volumen, None)
                print(f"🔉 Bajando volumen: {int(nuevo_volumen * 100)}%")
                vol_inicial = nuevo_volumen

    cv2.imshow('Control de Volumen con la Mirada', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

    # Leer tecla presionada
    key = cv2.waitKey(1) & 0xFF

    if key == ord('f'):  # Si se presiona "F", fijar/desfijar volumen
        vol_fijado = not vol_fijado
        estado = "fijado" if vol_fijado else "activo"
        print(f"🔒 Volumen {estado}")

    if key == 27:  # Tecla ESC para salir
        break


cap.release()
cv2.destroyAllWindows()
