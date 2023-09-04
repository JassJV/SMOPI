import torch
import cv2
from matplotlib import pyplot as plt
from PIL import Image
import os
# Ruta al archivo .pt del modelo YOLOv5
model_path = '/' 


# Cargar el modelo YOLOv5
model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)


# Ruta del directorio que contiene las fotos a analizar
directorio_fotos = "/"

#Ruta del directorio de imagen procesadas y logs
directorio="/"
logs = "/"
# Verificar existencia de directorios
os.makedirs(directorio, exist_ok=True)
os.makedirs(logs, exist_ok=True)

# Obtener la lista de archivos en el directorio de logs
archivos_existentes = os.listdir(logs)

count=0 
process=len(archivos_existentes) + 1

if os.path.exists(directorio_fotos):

    for nombre_archivo in os.listdir(directorio_fotos):
        ruta_archivo = os.path.join(directorio_fotos, nombre_archivo)
        
        if os.path.isfile(ruta_archivo):
            try:
              # Cargar la imagen de entrada
              image = cv2.imread(ruta_archivo)

              # Realizar la deteccion de objetos con YOLOv5
              results = model(image)

              # Obtener las coordenadas y las etiquetas de los objetos detectados
              pred = results.pandas().xyxy[0]  # Obtener las predicciones en formato pandas
              boxes = pred[['xmin', 'ymin', 'xmax', 'ymax']].values
              labels = pred['name'].tolist()

               

              # Iterar sobre las regiones detectadas y extraer el texto utilizando EasyOCR
              for box, label in zip(boxes, labels):
                xmin, ymin, xmax, ymax = box
                cropped_image = image[int(ymin):int(ymax), int(xmin):int(xmax)]
                nombre_imagen = f"energy_meter_{count}.jpg"
                ruta_imagen = os.path.join(directorio, nombre_imagen)
                cv2.imwrite(ruta_imagen, cropped_image)
                count +=1 

              # Dibujar los cuadros delimitadores y mostrar el texto detectado
              for box in boxes:
                xmin, ymin, xmax, ymax = box
                cv2.rectangle(image, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)

              # Guardar la imagen procesada
              
              # Verificar si el archivo ya existe y buscar un nombre unico
              nombre_imagen_logs = f"imagen_procesada_{process}.jpg"
              ruta_imagen_logs=os.path.join(logs, nombre_imagen_logs)
              while os.path.exists(ruta_imagen_logs):
                process+= 1
                nombre_imagen_logs = f"imagen_procesada_{process}.jpg"
                ruta_imagen_logs = os.path.join(logs, nombre_imagen_logs)
              
              cv2.imwrite(ruta_imagen_logs, image)
              process+=1
            except Exception as e:
                print(f"Error al abrir {ruta_archivo}: {e}")
else:
    print("El directorio no existe.")



