import requests
import json

#Ruta del archivo con la informacion formateada a JSON
ruta_archivo = "/"

def main():
    with open(ruta_archivo, 'r') as file:
        contenido_existente = file.read()
    # Cargar el contenido existente como un diccionario
    contenido_diccionario = json.loads(contenido_existente)
    
    # URL del endpoint para hacer el POST
    url = 'https://'
    
    try:
        # Realiza la solicitud POST
        response = requests.post(url, json=contenido_diccionario)
        
        # Verifica si la solicitud fue exitosa (codigo de estado 200)
        if response.status_code == 200:
            print('Solicitud POST exitosa.')
        else:
            print(f'Error en la solicitud POST. Codigo de estado: {response.status_code}')
    
    except requests.exceptions.RequestException as e:
        print(f'Error en la solicitud POST: {e}')

if __name__ == "__main__":
    main()
