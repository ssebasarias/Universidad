# Importar las librerías necesarias
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2
import csv

# Crear un cliente con tu clave de API de Clarifai
stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())

# Establecer tu clave de API y tu ID de aplicación
YOUR_CLARIFAI_API_KEY = "454edd0321184670bb946fed1a61673a"
YOUR_APPLICATION_ID = "my-first-application"

# Crear una lista con las URLs de las imágenes que quieres analizar
imagenes = ["https://samples.clarifai.com/metro-north.jpg",
            "https://samples.clarifai.com/dog2.jpeg",
            "https://samples.clarifai.com/wedding.jpg",
            "https://th.bing.com/th?id=OIP._1RFp6C4vdZ_dY8k5V-fAAHaEK&w=333&h=187&c=8&rs=1&qlt=90&o=6&dpr=1.3&pid=3.1&rm=2"
            "https://imagen.research.google/main_gallery_images/a-brain-riding-a-rocketship.jpg"
            "https://th.bing.com/th?id=OIP.b46MsMmCZN3oFUzs_dMmwQHaFj&w=288&h=216&c=8&rs=1&qlt=90&o=6&dpr=1.3&pid=3.1&rm=2"
            "https://th.bing.com/th?id=OIP.QLavrcMgYslbVsJR6y2E5QHaEh&w=319&h=195&c=8&rs=1&qlt=90&o=6&dpr=1.3&pid=3.1&rm=2"
            ]

# Crear un archivo CSV para guardar los datos
with open("datos.csv", "w") as archivo:
    # Crear un escritor de CSV
    escritor = csv.writer(archivo)
    # Escribir la fila de encabezados con los nombres de las columnas
    escritor.writerow(["Nombre de la Imagen", "URL", "Concepto", "Valor"])
    # Iterar sobre las imágenes y predecir conceptos para cada una
    for i in range(len(imagenes)):
        url = imagenes[i]
        nombre_imagen = f"Imagen {i+1}"
        # Crear una solicitud para predecir conceptos usando el modelo general de Clarifai
        request = service_pb2.PostModelOutputsRequest(
            model_id="general-image-recognition",
            user_app_id=resources_pb2.UserAppIDSet(app_id=YOUR_APPLICATION_ID),
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(image=resources_pb2.Image(url=url))
                )
            ],
        )
        # Enviar la solicitud y obtener la respuesta del servidor
        response = stub.PostModelOutputs(request, metadata=(("authorization", f"Key {YOUR_CLARIFAI_API_KEY}"),))
        # Verificar si la respuesta fue exitosa o no
        if response.status.code != status_code_pb2.SUCCESS:
            print(response)
            raise Exception(f"Request failed, status code: {response.status}")
        # Obtener la lista de conceptos predichos y sus valores de confianza
        conceptos = response.outputs[0].data.concepts
        # Escribir la fila con el Nombre de la imagen, URL y la cadena de conceptos en el archivo CSV
        for c in conceptos:
            escritor.writerow([nombre_imagen, url, c.name, c.value])