import datetime

def guardar_log(texto):  # para los errores de la bitacora del programa 
    """Registra eventos y errores en bitacora.txt"""
    with open("bitacora.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {texto}\n")
