import pandas as pd
import http.client
import zipfile

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

    # Establecer la conexión con el servidor
    conn = http.client.HTTPSConnection(host)

    # Realizar la solicitud GET
    conn.request("GET", path, headers=headers)

    # Obtener la respuesta
    response = conn.getresponse()

    # Leer el contenido de la respuesta
    if response.status == 200:
        with open("descarga.zip", "wb") as f:
            f.write(response.read())
        print("Archivo descargado exitosamente.")
    else:
        print("Error al descargar el archivo:", response.status)

    # Cerrar la conexión
    conn.close()

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
    df.to_excel("difuntos.xlsx",index=False)