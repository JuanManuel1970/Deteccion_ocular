# Detección Ocular y Control del Sistema con Python

Este repositorio contiene scripts en Python que utilizan **OpenCV** y **Mediapipe** para la detección ocular y el control del sistema. Se pueden realizar acciones como el control del volumen, el brillo de la pantalla y la detección de parpadeos.

## Características del Proyecto
✅ Detección en tiempo real utilizando la cámara web.
✅ Control de volumen con el movimiento de los ojos.
✅ Control de brillo de pantalla según la posición ocular.
✅ Conteo de parpadeos.
✅ Uso de **Mediapipe** para la detección facial y de ojos.
✅ Funciona en **Python 3.10**.

---

## Instalación y Configuración
### 1. Clonar el Repositorio
```bash
git clone https://github.com/JuanManuel1970/deteccion_ocular.git
cd deteccion_ocular
```

### 2. Crear un Entorno Virtual (Opcional, Recomendado)
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate  # En Windows
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar los Scripts
- Para el control de volumen:
  ```bash
  python control_volumen.py
  ```
- Para la detección de parpadeo:
  ```bash
  python deteccion_parpadeo.py
  ```
- Para el control de brillo:
  ```bash
  python control_pantalla.py
  ```

---

## Requisitos del Sistema
- **Python 3.10**
- **Webcam** (integrada o externa)
- **Sistema operativo:** Windows, Linux o macOS

---

## Dependencias
El archivo `requirements.txt` contiene todas las librerías necesarias. Entre ellas:
- `opencv-python`
- `mediapipe`
- `numpy`
- `screen-brightness-control` (para modificar el brillo de la pantalla en Windows)
- `pycaw` (para modificar el volumen en Windows)

---

## Licencia
Este proyecto se distribuye bajo la licencia **MIT**.

## Autor
📌 Desarrollado por [Juan MAnuel](https://github.com/JuanMAnuel1970)

¡Contribuciones y mejoras son bienvenidas! 🚀


