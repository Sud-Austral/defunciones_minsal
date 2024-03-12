import pandas as pd
import http.client
import zipfile
import time

def getZIP():
    # Definir los parámetros de la solicitud
    host = "repositoriodeis.minsal.cl"
    path = "/DatosAbiertos/VITALES/DEFUNCIONES_FUENTE_DEIS_2021_2024_12032024.zip"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
    headers = {
        "Host": host,
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "es-CL,es;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "TE": "trailers",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    }
    """
    # Establecer la conexión con el servidor
    conn = http.client.HTTPSConnection(host, timeout=1000)
    # Realizar la solicitud GET
    conn.request("GET", path, headers=headers)
    # Obtener la respuesta
    response = conn.getresponse()
    # Leer el contenido de la respuesta
    if response.status == 200:
        with open("descarga.zip", "wb") as f:
            f.write(response.read())
        print("Archivo descargado exitosamente.")
    #else:
    #    print("Error al descargar el archivo:", response.status)
    # Cerrar la conexión
    #conn.close()
    """
    for intento in range(3):  # Realizar hasta 3 intentos
        try:
            # Establecer la conexión con el servidor y configurar el tiempo de espera
            proxy_host = '45.225.207.186'
            proxy_port = 999  # Reemplazar con el puerto de tu proxy
            proxy_timeout = 1000  # Tiempo de espera en segundos

            # Establecer la conexión con el servidor utilizando el proxy y el timeout
            conn = http.client.HTTPSConnection(proxy_host, proxy_port, timeout=proxy_timeout)
            conn = http.client.HTTPSConnection(host, timeout=1000)  # Tiempo de espera de 10 segundos
            # Realizar la solicitud GET
            conn.request("GET", path, headers=headers)
            # Obtener la respuesta
            response = conn.getresponse()
            # Leer el contenido de la respuesta, manejarla como sea necesario
            if response.status == 200:
                with open("descarga.zip", "wb") as f:
                    f.write(response.read())
                print("Archivo descargado exitosamente.")
            else:
                print("Error al descargar el archivo:", response.status)
            # Cerrar la conexión
            conn.close()
            # Si la conexión y la solicitud tienen éxito, salir del bucle de intentos
            break

        except TimeoutError:
            # Si ocurre un error de tiempo de espera, esperar unos segundos antes de volver a intentarlo
            print("Tiempo de espera agotado. Reintentando conexión...")
            print(TimeoutError)
            time.sleep(5)  # Esperar 5 segundos antes de volver a intentarlo
            continue

        except Exception as e:
            print("Error:", e)
            break

    else:
        print("Se superó el número máximo de intentos. No se pudo establecer la conexión.")


        
def descomprimir():
    # Ruta del archivo ZIP
    archivo_zip = "descarga.zip"
    # Abre el archivo ZIP en modo lectura
    with zipfile.ZipFile(archivo_zip, 'r') as zip_ref:
        # Lista los contenidos del archivo ZIP
        contenidos = zip_ref.namelist()
        # Extrae todos los archivos del ZIP en la carpeta actual
        zip_ref.extractall()

if __name__ == '__main__':
    getZIP()
    descomprimir()
    df = pd.read_csv("DEFUNCIONES_FUENTE_DEIS_2021_2024_12032024.csv", encoding='latin-1',sep=";", header=None)
    df.columns = ['Año', 'Fecha', 'Sexo', 'Frecuencia', 'Edad', 'Codcom', 'Comuna',
       'Región', 'ID_DP', 'ID_Nivel 1', 'Nivel 1', 'ID_Nivel 2', 'Nivel 2',
       'ID_Nivel 3', ' Diagnóstico Principal', 'ID_DP1',
       ' Diagnóstico Principal INT', 'ID_OTRO', 'ID_CEXT (S-N)',
       'Causas externas (S-N)', 'ID_CEXTGRAL', 'Causas externas Gral',
       'ID_CEXTDETALLE', 'Causas externas de morbilidad y de mortalidad',
       'ID_CEXTDETALLEint',
       'Causas externas de morbilidad y de mortalidad INT', 'Lugar']
    df.to_excel("difuntos.xlsx",index=False)