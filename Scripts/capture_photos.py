import cv2
import os
import time
import datetime as dt

# Crear instancia de la camara USB
cap = cv2.VideoCapture(0)

# Verificar si la camara se ha activado correctamente
if not cap.isOpened():
    print("Error al abrir la camara")
    exit()

# Definir la cantidad de fotos a tomar
num_fotos = 5

# Directorios de las imagenes
directorio = "/home/integradora/SMOPI_YOLO_ENERGY/Capture"
logs = "/home/integradora/SMOPI_YOLO_ENERGY/Logs/Images"

# Verificar existencia de directorios
os.makedirs(directorio, exist_ok=True)
os.makedirs(logs, exist_ok=True)

# Obtener la lista de archivos en el directorio de logs
archivos_existentes = os.listdir(logs)

# Obtener el valor inicial de los contadores
contador=1
contador_logs = len(archivos_existentes) + 1

# Establecer tiempo actual
tiempoA = dt.datetime.now()

# Tomar las fotos
while num_fotos>0:
    # Leer un fotograma del flujo de video
    ret, frame = cap.read()

    # Verificar si se ha leido correctamente el fotograma
    if not ret:
        print("Error al leer el fotograma")
        break

    if (ret == True):
        # Almacenar el tiempo actual
        tiempoB = dt.datetime.now()
        # Calcular tiempo transcurrido
        tiempo_transcurrido = tiempoB - tiempoA
        #Verificar si ya transcurrieron los 5 segundos
        if tiempo_transcurrido.seconds >= 5:
            # Generar el nombre de las imagenes
            nombre_imagen = f"energy_meter_{contador}.jpg"
            nombre_imagen_logs = f"energy_meter_{contador_logs}.jpg"
            ruta_imagen = os.path.join(directorio, nombre_imagen)
            ruta_imagen_logs=os.path.join(logs, nombre_imagen_logs)

            # Verificar si el archivo ya existe y buscar un nombre unico
            while os.path.exists(ruta_imagen_logs):
                contador_logs += 1
                nombre_imagen_logs = f"energy_meter_{contador_logs}.jpg"
                ruta_imagen_logs = os.path.join(logs, nombre_imagen_logs)

            # Guardar las imagenes 
            cv2.imwrite(ruta_imagen, frame)
            cv2.imwrite(ruta_imagen_logs, frame)
            print(f"Imagen {contador} guardada correctamente en Capture")
            print(f"Imagen {contador_logs} guardada correctamente en Logs")
            # Incrementar los contadores
            contador+=1
            contador_logs += 1
            tiempoA = dt.datetime.now()
            # Disminuir el numero de fotos
            num_fotos -= 1

        if (cv2.waitKey(1) == ord('s')):
            break
    else:
        break

# Liberar la camara
cap.release()
