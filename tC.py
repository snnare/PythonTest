import socket
from PIL import Image
from io import BytesIO

# Función para enviar la imagen al servidor y recibirla de vuelta
def enviar_y_recibir_imagen(imagen, host, puerto):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, puerto))
        # ====== Envia por 1era Vez
        # Guardar la imagen en un archivo temporal
        imagen_temporal = "imagen_a_enviarC.png"
        imagen.save(imagen_temporal)

        # Enviar el tamaño del archivo
        tamano_archivo = len(open(imagen_temporal, "rb").read())
        s.sendall(str(tamano_archivo).encode())

        # Enviar la imagen
        with open(imagen_temporal, "rb") as f:
            s.sendall(f.read())

        # ====== Recibe por 1era vez
        # Recibir el tamani o del archivo de vuelta
        tamano_archivo_recibido = int(s.recv(1024).decode())

        # Recibir la imagen de vuelta
        imagen_data_recibida = b''
        while len(imagen_data_recibida) < tamano_archivo_recibido:
            imagen_data_recibida += s.recv(1024)

        # Convertir los datos recibidos en una imagen
        imagen_recibida = Image.open(BytesIO(imagen_data_recibida))

        # Guardar la imagen recibida de vuelta en la ruta "RecibidoDeServidor"
        ruta_recibido_servidor = "RecibidoDeServidor/imagenDeServidor01.png"
        imagen_recibida.save(ruta_recibido_servidor)
        print(f"IMG recibida de Servidor: {ruta_recibido_servidor}")


        # ====== Envia por 2da Vez
        imagen_rotada =  imagen_recibida.rotate(90)
        ruta_rotada_cliente = "RotadaEnCliente/imagen_rotada.png"
        imagen_rotada.save(ruta_rotada_cliente)

        with open(ruta_rotada_cliente, "rb") as f:
            imagen_data_rotada = f.read()
            tamano_archivo_rotada = len(imagen_data_rotada)
            s.sendall(str(tamano_archivo_rotada).encode())
            s.sendall(imagen_data_rotada)
            print("Imagen enviada al servidor")
        
        # ====== Recibe por 2da vez
        # Recibir el tamani o del archivo de vuelta
        tamano_archivo_recibido = int(s.recv(1024).decode())

        # Recibir la imagen de vuelta
        imagen_data_recibida = b''
        while len(imagen_data_recibida) < tamano_archivo_recibido:
            imagen_data_recibida += s.recv(1024)

        # Convertir los datos recibidos en una imagen
        imagen_recibida = Image.open(BytesIO(imagen_data_recibida))

        # Guardar la imagen recibida de vuelta en la ruta "RecibidoDeServidor"
        ruta_recibido_servidor = "RecibidoDeServidor/imagenDeServidor02.png"
        imagen_recibida.save(ruta_recibido_servidor)
        print(f"IMG recibida de Servidor: {ruta_recibido_servidor}")


        
        

# Ruta de la imagen original
ruta_original = "Original/pikachu.png"

# Cargar la imagen y rotarla 90 grados
imagen_original = Image.open(ruta_original)
imagen_rotada = imagen_original.rotate(90)

# Especificar la dirección IP y el puerto del servidor
direccion_servidor = "127.0.0.1"  # Cambia a la dirección IP del servidor si es diferente
puerto_servidor = 12345  # Cambia al puerto en el que el servidor está escuchando

# Enviar la imagen rotada al servidor y recibirla de vuelta
enviar_y_recibir_imagen(imagen_rotada, direccion_servidor, puerto_servidor)