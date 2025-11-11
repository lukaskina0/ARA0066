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

def verificar_feriados():
    caminho_pdf = entry_pdf.get()
    if not caminho_pdf:
        messagebox.showwarning("Aviso", "Escolha um arquivo PDF primeiro!")
        return

    datas_pdf = ler_pdf(caminho_pdf)
    if not datas_pdf:
        messagebox.showinfo("Aviso", "Nenhuma data encontrada no PDF.")
        return

    datas_br = []
    for d in datas_pdf:
        if "-" in d:
            partes = d.split("-")
            datas_br.append(f"{partes[2]}/{partes[1]}/{partes[0]}")
        else:
            datas_br.append(d)

    anos = sorted(set([d.split("/")[-1] for d in datas_br]))

    feriados_por_ano = {}
    for ano in anos:
        feriados_por_ano[ano] = obter_feriados(ano)

    resultados = []
    for data in datas_br:
        ano = data.split("/")[-1]
        if data in feriados_por_ano.get(ano, []):
            resultados.append(data)

    texto_resultado.delete("1.0", tk.END)
    if resultados:
        texto_resultado.insert(tk.END, "Datas separadas que são feriados:\n\n")
        for d in resultados:
            texto_resultado.insert(tk.END, f"{d}\n")
    else:
        texto_resultado.insert(tk.END, "Nenhuma data do PDF é feriado nacional.")

janela = tk.Tk()
janela.title("Verificador de Feriados")
janela.geometry("400x300")

label_instrucao = tk.Label(janela, text="Escolha o arquivo PDF:")
label_instrucao.pack(pady=5)

entry_pdf = tk.Entry(janela, width=40)
entry_pdf.pack()

btn_escolher = tk.Button(janela, text="Selecionar PDF", command=escolher_arquivo)
btn_escolher.pack(pady=5)

btn_verificar = tk.Button(janela, text="Verificar Feriados", command=verificar_feriados)
btn_verificar.pack(pady=5)

texto_resultado = tk.Text(janela, height=10, width=45)
texto_resultado.pack(pady=10)

janela.mainloop()