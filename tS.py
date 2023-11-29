import socket
from PIL import Image
from io import BytesIO

def recibir_rotar_y_reenviar_imagen(ip_servidor, puerto, iteraciones=4):
    for _ in range(iteraciones):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((ip_servidor, puerto))
            s.listen()
            print(f"Esperando la conexión en el puerto {puerto}...")
            conn, addr = s.accept()
            with conn:
                print(f"Conectado a {addr}")

                # Recibir el tamaño del archivo
                tamano_archivo = int(conn.recv(1024).decode())

                # Recibir la imagen
                imagen_data = b''
                while len(imagen_data) < tamano_archivo:
                    imagen_data += conn.recv(4096)

                # Convertir los datos recibidos en una imagen
                imagen_recibida = Image.open(BytesIO(imagen_data))

                # Guardar la imagen recibida
                ruta_recibida_cliente = f"RecibidoDeCliente/imagenDeCliente{_ + 1}.png"
                imagen_recibida.save(ruta_recibida_cliente)
                print(f"IMG recibida de Cliente ({_ + 1}): {ruta_recibida_cliente}")

                # Rotar la imagen recibida 90 grados
                imagen_rotada = imagen_recibida.rotate(90)

                # Guardar la imagen rotada
                ruta_rotada_servidor = "RotadaEnServidor/imagen_rotada.png"
                imagen_rotada.save(ruta_rotada_servidor)

                # Enviar la imagen rotada de vuelta al cliente
                with open(ruta_rotada_servidor, "rb") as f:
                    fragmento = f.read(4096)
                    while fragmento:
                        conn.sendall(fragmento)
                        fragmento = f.read(4096)
                print("Imagen enviada al cliente")

# Dirección IP y puerto del servidor
ip_servidor = "127.0.0.1"
puerto_servidor = 12345

# Iniciar el servidor en un bucle por 4 iteraciones
recibir_rotar_y_reenviar_imagen(ip_servidor, puerto_servidor, iteraciones=4)
