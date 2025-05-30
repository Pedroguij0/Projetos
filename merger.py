import PyPDF2 as py
import os

#Guide: to use the Archive Merger you just need to put the archives that you want to merge in the directory 'archives' and run the code bellow.

merger = py.PdfMerger()
lista_arquivos = os.listdir("arquivos")
lista_arquivos.sort()

for arquivos in lista_arquivos:
    if arquivos.endswith(".pdf"):
        merger.append(f"arquivos/{arquivos}")

merger.write("MergedPDF.pdf")