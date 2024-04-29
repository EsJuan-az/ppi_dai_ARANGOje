import re

def extract_field_from_integrity(error_msg):
    """Esta función extrae datos de los Integrity Errors.
    Args:
        error_msg (str): Mensaje de error a extraer.
    Returns:
        str: Extrae el campo del error.
    """
    match = re.search(r"Key \((\w+)\)=\([^\)]+\) already exists.", error_msg)
    if match:
        return match.group(1)  # El nombre del campo
    return None