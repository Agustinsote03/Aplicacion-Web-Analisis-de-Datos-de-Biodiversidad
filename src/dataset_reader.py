import csv 

def imprimir_primeras_filas(ruta_archivo, separador="\t"):
    with open(ruta_archivo, encoding="utf-8") as archivo:
        lector = csv.reader(archivo, delimiter=separador)
        
        contador = 0
        for fila in lector:
            print(fila)
            contador += 1
            
            if contador == 10:
                return