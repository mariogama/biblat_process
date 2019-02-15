# biblat_process

Proceso de datos de ALEPH a mongoDB

# Instalación

python setup.py

# Configuración

## Variables de entorno

BIBLATP_REMOTE_ADDR: Dirección IP del servidor ALEPH, default: 127.0.0.1

BIBLATP_REMOTE_USER: Usuario del servidor ALEPH; default: aleph

BIBLATP_REMOTE_PATH: Directorio remoto para descargar datos, default: /exlibris/aleph/a21_1/alephm/sql_report/anexo/biblat_process

BIBLATP_LOCAL_PATH: Directorio local para guardar los datos, default: ./data

# Uso

```bash
usage: claper_dump [-h] [--logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                   [--until_date UNTIL_DATE] [--clase] [--periodica]
                   [--exec {list,dump,pull,all}]

Cosecha de archivos

optional arguments:
  -h, --help            show this help message and exit
  --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}, -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Logging level
  --until_date UNTIL_DATE, -u UNTIL_DATE
                        Fecha en formato ISO como 20190201
  --clase               Procesar solo CLASE
  --periodica           Procesar solo PERIÓDICA
  --exec {list,dump,pull,all}, -e {list,dump,pull,all}
                        Seleccione proceso a ejecutar
```
