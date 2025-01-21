import PyPDF2 as py
import os

merger = py.PdfMerger()
lista_arquivos = os.listdir("arquivos")
lista_arquivos.sort()

for arquivos in lista_arquivos:
    if arquivos.endswith(".pdf"):
        merger.append(f"arquivos/{arquivos}")

merger.write("MergedPDF.pdf")