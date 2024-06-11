import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

# Função para lidar com o clique no botão de cadastro
def cadastrar():
    codigo_funcional = entry_codigo_funcional.get()
    chave_pix = entry_chave_pix.get()
    
    if codigo_funcional and chave_pix:
        # Salva os dados em um arquivo JSON
        dados = {
            'codigo_funcional': codigo_funcional,
            'chave_pix': chave_pix
        }
        with open('cadastros.json', 'a') as file:
            json.dump(dados, file)
            file.write('\n')
        messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso!")
        abrir_tela_upload()
    else:
        messagebox.showwarning("Erro", "Todos os campos são obrigatórios!")

# Função para abrir a tela de upload de imagens
def abrir_tela_upload():
    # Fecha a janela de cadastro
    root.destroy()
    
    # Cria a janela de upload
    upload_root = tk.Tk()
    upload_root.title("Upload de Imagens")
    upload_root.geometry("400x300")
    
    def upload_imagens():
        arquivos = filedialog.askopenfilenames(
            title="Selecione as imagens",
            filetypes=(("Arquivos de imagem", "*.jpg;*.jpeg;*.png"),)
        )
        if arquivos:
            # Caminho para o modelo salvo
            caminho_do_modelo = 'recyclai.h5'
            
            # Carregar modelo TensorFlow
            model = tf.keras.models.load_model(caminho_do_modelo)
            
            for arquivo in arquivos:
                # Carregar e processar a imagem
                img = image.load_img(arquivo, target_size=(224, 224))  # Ajuste o tamanho conforme necessário
                img_array = image.img_to_array(img)
                img_array = np.expand_dims(img_array, axis=0)
                img_array = img_array / 255.0  # Normalizar a imagem

                # Fazer previsão
                prediction = model.predict(img_array)
                print(f"Imagem: {arquivo} - Previsão: {prediction}")
            
            messagebox.showinfo("Upload", "Imagens carregadas e analisadas com sucesso!")
        else:
            messagebox.showwarning("Erro", "Nenhuma imagem selecionada.")
    
    label_info = tk.Label(upload_root, text="Carregue suas imagens para análise:")
    label_info.pack(pady=20)
    
    btn_upload = tk.Button(upload_root, text="Carregar Imagens", command=upload_imagens)
    btn_upload.pack(pady=20)
    
    upload_root.mainloop()

# Criação da janela principal
root = tk.Tk()
root.title("Tela de Cadastro")
root.geometry("400x300")

# Labels e campos de entrada
label_codigo_funcional = tk.Label(root, text="Código Funcional:")
label_codigo_funcional.pack(pady=5)

entry_codigo_funcional = tk.Entry(root)
entry_codigo_funcional.pack(pady=5)

label_chave_pix = tk.Label(root, text="Chave Pix:")
label_chave_pix.pack(pady=5)

entry_chave_pix = tk.Entry(root)
entry_chave_pix.pack(pady=5)

# Botão de cadastro
btn_cadastrar = tk.Button(root, text="Cadastrar", command=cadastrar)
btn_cadastrar.pack(pady=20)

# Executa o loop principal da interface gráfica
root.mainloop()
