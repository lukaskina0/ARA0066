import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import re
import requests

def escolher_arquivo():
    caminho = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if caminho:
        entry_pdf.delete(0, tk.END)
        entry_pdf.insert(0, caminho)

def ler_pdf(caminho_pdf):
    leitor = PyPDF2.PdfReader(caminho_pdf)
    texto = ""
    for pagina in leitor.pages:
        texto += pagina.extract_text()
    datas = re.findall(r"\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}", texto)
    return datas

def obter_feriados(ano):
    url = f"https://date.nager.at/api/v3/PublicHolidays/{ano}/BR"
    r = requests.get(url)
    if r.status_code == 200:
        feriados = []
        for f in r.json():
            data = f["date"]
            feriados.append(f"{data[8:10]}/{data[5:7]}/{data[0:4]}")
        return feriados
    return []

janela = tk.Tk()
janela.title("Verificador de Feriados")
janela.geometry("400x300")

label_instrucao = tk.Label(janela, text="Escolha o arquivo PDF:")
label_instrucao.pack(pady=5)

entry_pdf = tk.Entry(janela, width=40)
entry_pdf.pack()

btn_escolher = tk.Button(janela, text="Selecionar PDF", command=escolher_arquivo)
btn_escolher.pack(pady=5)

# Botão de verificar (ainda sem funcionalidade completa)
btn_verificar = tk.Button(janela, text="Verificar Feriados")
btn_verificar.pack(pady=5)

# Área de texto para resultados (ainda vazia)
texto_resultado = tk.Text(janela, height=10, width=45)
texto_resultado.pack(pady=10)

janela.mainloop()