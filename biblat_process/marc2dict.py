# -*- coding: utf-8 -*-
import os
import gzip
import re
from biblat_process.settings import config


class Marc2Dict:
    """Clase para convertir registros MARC en un diccionario"""

    def __init__(self):
        # Patrones compilados
        self.record_pattern = re.compile(r'(^\d{9})\s(.{3})(.{2})\sL\s(.+?$)')
        self.el_val_pattern = re.compile(r'\$\$([a-zA-Z0-9])')
        self.sequence_pattern = re.compile(r"^\(([0-9]+?)\)$")

    def get_lines(self):
        """
        Regresa las lineas de los archivos en formato ALEPH secuencial
        por medio del generador yield
        """
        for db_file in config.DB_FILES:
            db_file = os.path.join(config.LOCAL_PATH, db_file)
            with gzip.open(db_file, mode='rt',
                           encoding='utf-8', errors='ignore') as process_file:
                for line in process_file:
                    # Eliminamos el salto de linea al final de la cadena
                    yield line.strip()

    def get_dict(self):
        """Regresar un registro MARC en formato de diccionario"""
        marc_dict = {}
        current = ""
        z = 0
        for line in self.get_lines():
            if line == 'EOF':
                z = 0
                current = ''
                return_dict = marc_dict
                marc_dict = {}
                yield return_dict

            # Con una expresión regular separamos cada linea en sistema,
            # etiqueta y valor
            result = self.record_pattern.match(line)
            # Si existe el patrón en la linea la procesamos
            if result:
                sistema = result.group(1)
                etiqueta = result.group(2)
                indicador = result.group(3)
                valor = result.group(4)
                # Evaluamos si es un registro diferente para regresar el
                # registro
                if current != '' and sistema != current:
                    z = 0
                    return_dict = marc_dict
                    marc_dict = {}
                    yield return_dict
                # Asignamos el valor del registro actual
                current = sistema
                # Inicializamos un diccionario para almacenar los elementos
                # de la etiqueta
                subtags = {}
                subtag = {}
                # Dividimos cada elemento en sub-campo y valor
                values = self.el_val_pattern.split(valor.strip())
                if '' in values:
                    values.remove('')
                for key, val in zip(values[::2], values[1::2]):
                    val = re.sub('[.,]$', '', val)
                    if etiqueta == '100' and key in subtag \
                            and self.sequence_pattern.match(val) is not None:
                        key = 'z'
                    # Si existe más de un sub-campo con la misma llave y el
                    # valor del sub-campo actual es una cadena, creamos una
                    # lista para almacenar los valores de los sub-campos con
                    # la misma llave
                    if key in subtag and isinstance(subtag[key], str):
                        subtag[key] = [subtag[key], val]
                    # Si existe más de un sub-campo con la misma llave
                    # almacenamos los valores en la lista creada anteriormente
                    elif key in subtag:
                        subtag[key].append(val)
                    # Si el valor no es una cadena vacía lo almacenamos
                    elif val.strip():
                        subtag[key] = val

                # Incrementamos el valor de z cuando existe en la etiqueta 120
                if etiqueta == '120':
                    z += 1
                    subtag.update({'z': '(%d)' % z})
                # Ajustamos el valor de la etiqueta 120 cuando esta dentro
                # de la etiqueta 100
                if etiqueta == '100' and \
                        any(key in subtag for key in ['u', 'v', 'w', 'x']) \
                        and any(key in subtag for key in ['a', '6']):
                    z += 1
                    subtag.update({'z': '(%d)' % z})
                    subtags['100'] = dict(
                        (k, subtag[k]) for k in ['a', '6', 'z'] if k in subtag
                    )
                    subtags['120'] = dict((k, subtag[k]) for k in
                                          ['u', 'v', 'w', 'x', 'z'] if
                                          k in subtag)
                    marc_dict['120in100'] = True
                elif etiqueta == '100' \
                        and any(key in subtag for key in ['u', 'v', 'w', 'x']):
                    z += 1
                    subtag.update({'z': '(%d)' % z})
                    subtags['120'] = subtag
                    marc_dict['120in100'] = True
                elif etiqueta == 'CAT':
                    subtags[etiqueta] = subtag
                elif not self.el_val_pattern.match(valor):
                    subtags[etiqueta] = {}
                    subtags[etiqueta]['#'] = valor
                elif len(subtag) > 0:
                    subtags[etiqueta] = subtag

                for etiqueta, subtag in subtags.items():
                    if indicador.strip():
                        subtag['@ind'] = indicador

                    # Si la etiqueta no esta en el diccionario del registro
                    # inicializamos una lista y agregamos las sub-etiquetas
                    marc_dict.setdefault(etiqueta, []).append(subtag)
