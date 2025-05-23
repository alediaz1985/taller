import os
import PyPDF2

'''
# PARA BUSQUEDA DE ARCHIVOS INCLUYENDO LA EXTENCIÓN EJEMPLO  ad678ds.pdf
def buscar_archivos_pdf(nombre_archivo, directorio):
    archivos_pdf = []
    for root, _, archivos in os.walk(directorio):
        for archivo in archivos:
            if archivo.lower() == nombre_archivo.lower() and archivo.endswith('.pdf'):
                archivos_pdf.append(os.path.join(root, archivo))
    return archivos_pdf

'''

def buscar_archivos_pdf(nombre_archivo, directorio):
    archivos_pdf = []
    for root, _, archivos in os.walk(directorio):
        for archivo in archivos:
            nombre_sin_extension, extension = os.path.splitext(archivo)
            if nombre_sin_extension.lower() == nombre_archivo.lower() and extension.lower() == '.pdf':
                archivos_pdf.append(os.path.join(root, archivo))
    return archivos_pdf

def extraer_texto(pdf_archivo):
    texto = ""
    with open(pdf_archivo, 'rb') as archivo:
        lector_pdf = PyPDF2.PdfReader(archivo)
        for pagina in range(len(lector_pdf.pages)):
            texto += lector_pdf.pages[pagina].extract_text()
    return texto
