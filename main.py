import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd
import os
import json
from datetime import datetime

ARQUIVO_DADOS = 'clientes.json'

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
            try:
                dados = json.load(f)
                df = pd.DataFrame(dados)
                if 'ID' not in df.columns:
                    df['ID'] = range(1, len(df) + 1)
                return df
            except json.JSONDecodeError:
                return pd.DataFrame(columns=['ID', 'Nome', 'Objeto', 'Data', 'Valor'])
    return pd.DataFrame(columns=['ID', 'Nome', 'Objeto', 'Data', 'Valor'])

def salvar_dados_em_arquivo():
    df_clientes.to_json(ARQUIVO_DADOS, orient='records', indent=4, force_ascii=False)

df_clientes = carregar_dados()

ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("Sistema de Clientes")
app.geometry("1300x500")  

frame_top = tk.Frame(app)
frame_top.pack(fill="x", pady=10, padx=10)

filtro_pesquisa = tk.StringVar()
entry_pesquisa = tk.Entry(frame_top, textvariable=filtro_pesquisa, width=50)
entry_pesquisa.pack(side="left", padx=(0, 10))

btn_novo_cliente = tk.Button(frame_top, text="Novo Cliente", command=lambda: abrir_tela_de_registro())
btn_novo_cliente.pack(side="right")

frame_tabela = tk.Frame(app)
frame_tabela.pack(fill="both", expand=True, padx=10)

colunas = ["ID", "Nome", "Objeto", "Data", "Valor", "Editar", "Excluir", "Adicionar Valor", "Subtrair Valor"]
for i, col in enumerate(colunas):
    tk.Label(frame_tabela, text=col, borderwidth=1, relief="solid", width=18).grid(row=0, column=i)

linhas_widgets = []

def atualizar_tabela():
    for linha in linhas_widgets:
        for w in linha:
            w.destroy()
    linhas_widgets.clear()

    df_ordenado = df_clientes.copy()
    try:
        df_ordenado = df_ordenado.sort_values(by=['Nome', 'Valor'], key=lambda col: col.astype(str)).reset_index(drop=True)
    except KeyError:
        pass

    filtro = filtro_pesquisa.get().lower()

    visual_row_index = 0

    for _, row in df_ordenado.iterrows():
        if filtro and filtro not in str(row['Nome']).lower():
            continue

        real_id = row['ID']

        widgets_linha = []
        for i, campo in enumerate(['ID', 'Nome', 'Objeto', 'Data', 'Valor']):
            lbl = tk.Label(frame_tabela, text=row.get(campo, ''), borderwidth=1, relief="solid", width=18)
            lbl.grid(row=visual_row_index + 1, column=i)
            widgets_linha.append(lbl)

        btn_editar = tk.Button(frame_tabela, text="Editar", command=lambda i=real_id: abrir_tela_de_registro(i))
        btn_editar.grid(row=visual_row_index + 1, column=5)
        widgets_linha.append(btn_editar)

        btn_excluir = tk.Button(frame_tabela, text="Excluir", fg="red", command=lambda i=real_id: excluir_cliente(i))
        btn_excluir.grid(row=visual_row_index + 1, column=6)
        widgets_linha.append(btn_excluir)

        btn_add = tk.Button(frame_tabela, text="+", command=lambda i=real_id: alterar_valor(i, 'add'))
        btn_add.grid(row=visual_row_index + 1, column=7)
        widgets_linha.append(btn_add)

        btn_sub = tk.Button(frame_tabela, text="-", command=lambda i=real_id: alterar_valor(i, 'sub'))
        btn_sub.grid(row=visual_row_index + 1, column=8)
        widgets_linha.append(btn_sub)

        linhas_widgets.append(widgets_linha)
        visual_row_index += 1

def obter_indice_por_id(id_cliente):
    global df_clientes
    indices = df_clientes.index[df_clientes['ID'] == id_cliente].tolist()
    if indices:
        return indices[0]
    else:
        raise ValueError("ID do cliente não encontrado.")

def alterar_valor(id_cliente, operacao):
    global df_clientes
    try:
        idx = obter_indice_por_id(id_cliente)
        valor_atual = float(df_clientes.loc[idx, 'Valor'])
        valor_str = simpledialog.askstring("Valor", f"Digite o valor para {'adicionar' if operacao == 'add' else 'subtrair'}:")
        if valor_str is None:
            return
        valor_digitado = float(valor_str)
        novo_valor = valor_atual + valor_digitado if operacao == 'add' else valor_atual - valor_digitado
        df_clientes.at[idx, 'Valor'] = novo_valor
        salvar_dados_em_arquivo()
        atualizar_tabela()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def excluir_cliente(id_cliente):
    global df_clientes
    try:
        idx = obter_indice_por_id(id_cliente)
        confirm = messagebox.askyesno("Confirmar exclusão", f"Tem certeza que deseja excluir o cliente ID {id_cliente}?")
        if confirm:
            df_clientes = df_clientes.drop(idx).reset_index(drop=True)
            salvar_dados_em_arquivo()
            atualizar_tabela()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def abrir_tela_de_registro(id_edicao=None):
    nova = tk.Toplevel()
    nova.title("Registro")

    tk.Label(nova, text="Nome:").grid(row=0, column=0)
    entry_nome = tk.Entry(nova)
    entry_nome.grid(row=0, column=1)

    tk.Label(nova, text="Objeto:").grid(row=1, column=0)
    entry_objeto = tk.Entry(nova)
    entry_objeto.grid(row=1, column=1)

    tk.Label(nova, text="Data (DD/MM/AAAA):").grid(row=2, column=0)
    entry_data = tk.Entry(nova)
    entry_data.grid(row=2, column=1)

    tk.Label(nova, text="Valor:").grid(row=3, column=0)
    entry_valor = tk.Entry(nova)
    entry_valor.grid(row=3, column=1)

    if id_edicao is not None:
        try:
            idx = obter_indice_por_id(id_edicao)
            cliente = df_clientes.loc[idx]
            entry_nome.insert(0, cliente.get('Nome', ''))
            entry_objeto.insert(0, cliente.get('Objeto', ''))
            entry_data.insert(0, cliente.get('Data', ''))
            entry_valor.insert(0, cliente.get('Valor', ''))
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            nova.destroy()
            return

    def salvar():
        global df_clientes
        try:
            valor = float(entry_valor.get())
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido")
            return

        try:
            data_formatada = datetime.strptime(entry_data.get(), "%d/%m/%Y").strftime("%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro", "Data inválida. Use o formato DD/MM/AAAA.")
            return

        novo = {
            'Nome': entry_nome.get(),
            'Objeto': entry_objeto.get(),
            'Data': data_formatada,
            'Valor': valor
        }

        if id_edicao is not None:
            try:
                idx = obter_indice_por_id(id_edicao)
                for k, v in novo.items():
                    df_clientes.at[idx, k] = v
            except Exception as e:
                messagebox.showerror("Erro", str(e))
                return
        else:
            novo['ID'] = df_clientes['ID'].max() + 1 if not df_clientes.empty else 1
            novo_df = pd.DataFrame([novo], columns=df_clientes.columns)
            df_clientes = pd.concat([df_clientes, novo_df], ignore_index=True)

        salvar_dados_em_arquivo()
        atualizar_tabela()
        nova.destroy()

    tk.Button(nova, text="Salvar", command=salvar).grid(row=4, columnspan=2, pady=10)

entry_pesquisa.bind('<KeyRelease>', lambda e: atualizar_tabela())
atualizar_tabela()
app.mainloop()
