import ctypes  
import cv2
import mediapipe as mp
import time

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

# Índices de los puntos del ojo derecho e izquierdo
OJOS_DER = [374, 386]  # Párpado superior e inferior del ojo derecho
OJOS_IZQ = [145, 159]  # Párpado superior e inferior del ojo izquierdo

# Obtener el tamaño de la pantalla
pantalla_ancho = ctypes.windll.user32.GetSystemMetrics(0)
pantalla_alto = ctypes.windll.user32.GetSystemMetrics(1)

# Tiempo del último guiño detectado
ultimo_guiño = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb_frame)

    if result.multi_face_landmarks:
        for face_landmarks in result.multi_face_landmarks:
            ojo_derecho = face_landmarks.landmark[468]  # Punto de referencia del ojo derecho
            parpado_der_superior = face_landmarks.landmark[OJOS_DER[1]]
            parpado_der_inferior = face_landmarks.landmark[OJOS_DER[0]]
            parpado_izq_superior = face_landmarks.landmark[OJOS_IZQ[1]]
            parpado_izq_inferior = face_landmarks.landmark[OJOS_IZQ[0]]

            # Calcular la distancia entre los párpados de cada ojo
            distancia_ojo_der = abs(parpado_der_superior.y - parpado_der_inferior.y)
            distancia_ojo_izq = abs(parpado_izq_superior.y - parpado_izq_inferior.y)

            # **Ajustar la sensibilidad** (Multiplicar por un número mayor para más sensibilidad)
            escala_x = 8000  # Aumenta el valor para menos movimiento de la cabeza
            escala_y = -6000  # Aumenta para mejorar la sensibilidad vertical

            pantalla_x = int(ojo_derecho.x * escala_x - escala_x / 2 + pantalla_ancho / 2)
            pantalla_y = int(ojo_derecho.y * escala_y - escala_y / 2 + pantalla_alto / 2)
            
            # **Mover el cursor**
            ctypes.windll.user32.SetCursorPos(pantalla_x, pantalla_y)

            # **Detectar guiño (clic con ojo derecho cerrado)**
            if distancia_ojo_der < 0.015 and distancia_ojo_izq > 0.02:  
                if time.time() - ultimo_guiño > 0.5:  # Evita múltiples clics seguidos
                    print("🖱 Clic detectado (Guiño del ojo derecho)")
                    ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0) 
                    ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0) 
                    ultimo_guiño = time.time() 

    cv2.imshow('Control de Mouse', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
