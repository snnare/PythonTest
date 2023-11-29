import socket
from PIL import Image
from io import BytesIO

def enviar_y_recibir_imagen(imagen, host, puerto, iteraciones=4):
    for _ in range(iteraciones):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, puerto))

            # Guardar la imagen en un archivo temporal
            imagen_temporal = "RotadaEnCliente/imgRotadaCliente.png"
            imagen.save(imagen_temporal)

            # Enviar el tamaño del archivo
            tamano_archivo = len(open(imagen_temporal, "rb").read())
            s.sendall(str(tamano_archivo).encode())

            # Enviar la imagen
            with open(imagen_temporal, "rb") as f:
                fragmento = f.read(4096)
                while fragmento:
                    s.sendall(fragmento)
                    fragmento = f.read(4096)

            # Recibir el tamaño del archivo de vuelta
            tamano_archivo_recibido = int(s.recv(1024).decode())

            # Recibir la imagen de vuelta
            imagen_data_recibida = b''
            while len(imagen_data_recibida) < tamano_archivo_recibido:
                imagen_data_recibida += s.recv(4096)

            # Convertir los datos recibidos en una imagen
            imagen_recibida = Image.open(BytesIO(imagen_data_recibida))

            # Guardar la imagen recibida de vuelta
            ruta_recibido_servidor = f"RecibidoDeServidor/imagenDeServidor{_ + 1}.png"
            imagen_recibida.save(ruta_recibido_servidor)
            print(f"IMG recibida de Servidor ({_ + 1}): {ruta_recibido_servidor}")

# Ruta de la imagen original
ruta_original = "Original/pikachu.png"

# Cargar la imagen y rotarla 90 grados
imagen_original = Image.open(ruta_original)
imagen_rotada = imagen_original.rotate(90)

# Especificar la dirección IP y el puerto del servidor
direccion_servidor = "127.0.0.1"  # Cambia a la dirección IP del servidor si es diferente
puerto_servidor = 12345  # Cambia al puerto en el que el servidor está escuchando

# Enviar y recibir la imagen en un bucle por 4 iteraciones
enviar_y_recibir_imagen(imagen_rotada, direccion_servidor, puerto_servidor, iteraciones=4)
