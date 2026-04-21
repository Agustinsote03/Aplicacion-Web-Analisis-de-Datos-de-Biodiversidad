def es_coordenada_valida(valor, limite_min, limite_max):
    #Quitamos espacios en blanco
    valor = valor.strip()
    #Si está vacío se retorna False directamente
    if not valor:
        return False   
    #Se convierte  en float() para comparar
    numero = float(valor)
    es_valida = limite_min <= numero <= limite_max

    return es_valida