import cv2
import mediapipe as mp

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

# Índices de los puntos de los ojos 
OJOS_IZQ = [145, 159]  # Puntos del ojo izquierdo
OJOS_DER = [374, 386]  # Puntos del ojo derecho

# Variables para contar parpadeos
contador_parpadeos = 0
ojos_cerrados = False  # Para evitar contar múltiples parpadeos seguidos

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("⚠️ No se pudo leer el fotograma.")
        break

    # Convertir el frame a RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar el frame con Mediapipe
    result = face_mesh.process(rgb_frame)

    if result.multi_face_landmarks:
        for face_landmarks in result.multi_face_landmarks:
            # Obtener coordenadas de los ojos
            def obtener_punto(id):
                return int(face_landmarks.landmark[id].x * frame.shape[1]), int(face_landmarks.landmark[id].y * frame.shape[0])
            
            # Distancia entre párpados
            ojo_izq_arriba, ojo_izq_abajo = obtener_punto(OJOS_IZQ[0]), obtener_punto(OJOS_IZQ[1])
            ojo_der_arriba, ojo_der_abajo = obtener_punto(OJOS_DER[0]), obtener_punto(OJOS_DER[1])

            distancia_izq = abs(ojo_izq_arriba[1] - ojo_izq_abajo[1])
            distancia_der = abs(ojo_der_arriba[1] - ojo_der_abajo[1])

            # Dibujar los puntos de los ojos
            cv2.circle(frame, ojo_izq_arriba, 3, (0, 255, 0), -1)
            cv2.circle(frame, ojo_izq_abajo, 3, (0, 255, 0), -1)
            cv2.circle(frame, ojo_der_arriba, 3, (0, 255, 0), -1)
            cv2.circle(frame, ojo_der_abajo, 3, (0, 255, 0), -1)

            # Si la distancia es muy pequeña, el ojo está cerrado
            umbral = 4  # Ajusta según la distancia real de tu cara
            if distancia_izq < umbral and distancia_der < umbral:
                if not ojos_cerrados:
                    contador_parpadeos += 1
                    ojos_cerrados = True  # Evita contar múltiples veces el mismo parpadeo
            else:
                ojos_cerrados = False  # Resetea cuando el ojo se abre

    # Mostrar el contador de parpadeos en pantalla
    cv2.putText(frame, f"Parpadeos: {contador_parpadeos}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Mostrar la imagen con los puntos
    cv2.imshow('Detección de Parpadeos', frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Presiona ESC para salir
        break

cap.release()
cv2.destroyAllWindows()
