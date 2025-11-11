import tkinter as tk
from tkinter import filedialog, messagebox

def escolher_arquivo():
    caminho = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if caminho:
        entry_pdf.delete(0, tk.END)
        entry_pdf.insert(0, caminho)

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