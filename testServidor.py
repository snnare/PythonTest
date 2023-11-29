import socket
from PIL import Image
from io import BytesIO

# Función para recibir la imagen, guardarla, rotarla 90 grados y enviarla de vuelta al cliente
def recibir_rotar_y_reenviar_imagen(ip_servidor, puerto):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        tamano_buffer = 4096
        
        s.bind((ip_servidor, puerto))
        s.listen()
        print(f"Esperando la conexión en el puerto {puerto}...")
        conn, addr = s.accept()
        with conn:
            print(f"Conectado a {addr}")

            # ====== Recibe por 1era Vez
            # Recibir el tamaño del archivo
            tamano_archivo = int(conn.recv(1024).decode())

            # Recibir la imagen
            imagen_data = b''
            while len(imagen_data) < tamano_archivo:
                imagen_data += conn.recv(tamano_buffer)

            # Convertir los datos recibidos en una imagen
            imagen_recibida = Image.open(BytesIO(imagen_data))

            # Guardar la imagen recibida en la ruta "RecibidasDeCliente"
            ruta_recibidas_cliente = "RecibidoDeCliente/imagenDeCliente01.png"
            imagen_recibida.save(ruta_recibidas_cliente)
            print(f"IMG recibida de Cliente: {ruta_recibidas_cliente}")


            # ====== Envia por 1era Vez
            # Rotar la imagen recibida 90 grados
            imagen_rotada = imagen_recibida.rotate(90)

            # Guardar la imagen rotada en la ruta "RotadaEnServidor"
            ruta_rotada_servidor = "RotadaEnServidor/imagen_rotada.png"
            imagen_rotada.save(ruta_rotada_servidor)
            #print(f"Rotada y guardada como {ruta_rotada_servidor}")

            # Enviar la imagen rotada de vuelta al cliente
            with open(ruta_rotada_servidor, "rb") as f:
                imagen_data_rotada = f.read()
                tamano_archivo_rotada = len(imagen_data_rotada)
                conn.sendall(str(tamano_archivo_rotada).encode())
                conn.sendall(imagen_data_rotada)
                print("Imagen  enviada al cliente")
         

ip_servidor = "192.168.100.45"
# Puerto en el que el servidor escuchará
puerto_servidor = 12345

# Iniciar el servidor
recibir_rotar_y_reenviar_imagen(ip_servidor, puerto_servidor)
