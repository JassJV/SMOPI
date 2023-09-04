import requests
from PIL import Image
from transformers import TrOCRProcessor
from transformers import VisionEncoderDecoderModel
import os
import json


#lista_datos=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
lista_prueba=[0,0,0,0,0,0,0]

#Insertar la ruta de los modelos pre-entrenados
processor = TrOCRProcessor.from_pretrained("/")

#Insertar la ruta de los codificadores y decodificadores de los modelos pre-entrenados
model = VisionEncoderDecoderModel.from_encoder_decoder_pretrained("/codificador", "/decodificador")

#Insertar la ruta del directorio de los recortes
directorio_fotos = "/"

if os.path.exists(directorio_fotos):
    for nombre_archivo in os.listdir(directorio_fotos):
        ruta_archivo = os.path.join(directorio_fotos, nombre_archivo)
        if os.path.isfile(ruta_archivo):
            try:
              image = Image.open(ruta_archivo).convert("RGB")
              pixel_values = processor(image, return_tensors="pt").pixel_values
              generated_ids = model.generate(pixel_values)
              generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
              trans=generated_text.replace(" ", "")
              print(trans)
              n,t,d=nombre_archivo.split("_")
              indice,tipo=d.split(".")
              i=int(indice)
              try:
                numero = float(trans)
                lista_prueba[i]=numero  #cambiar lista
              except ValueError:
                lista_prueba[i]=0       #cambiar lista
              
            except Exception as e:
                print(f"Error al abrir {ruta_archivo}: {e}")
else:
    print("El directorio no existe.")


print(lista_prueba) #Cambiar lista (eliminar)

diccionario_datos = {}
for i in range(0, len(lista_prueba), 2):
    if i + 1 < len(lista_prueba):
        diccionario_datos[int(lista_prueba[i+1])] = lista_prueba[i]

data = {
    #Id de la plataforma
    "id": "id",
    "data": [],
    "sensedAt": ""
}


for key, value in diccionario_datos.items():
    entry = {
        "val": value,
        "type": str(key)
    }
    data["data"].append(entry)

json_data = json.dumps(data, indent=4)

#Rutas de los archivos txt en donde se guardara la informacion

ruta_archivo = "/translation_formatted.txt"
ruta_archivo_logs = "/translation_logs"
with open(ruta_archivo, 'w') as file:
    file.write(json_data)


with open(ruta_archivo_logs, 'a') as file:
    file.write(json.dumps(diccionario_datos) + '\n')
    
print("Traducción Completada")

