# Gerador de CPF - Versão Desktop com Tkinter
# IMPORTANTE: Use esses CPFs apenas para ambientes de teste e desenvolvimento.

import tkinter as tk
from tkinter import ttk, messagebox
import random
import pandas as pd
from datetime import datetime
import os

class GeradorCPF:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Gerador de CPFs")
        self.window.geometry("600x600")
        self.window.resizable(False, False)
        
        # Dicionário de estados e seus respectivos dígitos
        self.estados = {
            "Rio Grande do Sul": "0",
            "Distrito Federal, Goiás, Mato Grosso, Mato Grosso do Sul e Tocantins": "1",
            "Amazonas, Pará, Roraima, Amapá, Acre e Rondônia": "2",
            "Ceará, Maranhão e Piauí": "3",
            "Paraíba, Pernambuco, Alagoas e Rio Grande do Norte": "4",
            "Bahia e Sergipe": "5",
            "Minas Gerais": "6",
            "Rio de Janeiro e Espírito Santo": "7",
            "São Paulo": "8",
            "Paraná e Santa Catarina": "9",
            "Aleatório": "random"
        }
        
        # Configuração do estilo
        self.style = ttk.Style()
        self.style.configure('TButton', padding=5)
        self.style.configure('TLabel', padding=5)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Título
        titulo = ttk.Label(self.window, text="Gerador de CPFs Válidos", font=('Helvetica', 16, 'bold'))
        titulo.pack(pady=20)
        
        # Aviso
        aviso = ttk.Label(self.window, text="Use estes dados apenas para ambientes de teste e desenvolvimento",
                         foreground='red')
        aviso.pack(pady=10)
        
        # Frame para entrada de dados
        input_frame = ttk.Frame(self.window)
        input_frame.pack(pady=20, padx=20, fill='x')
        
        # Quantidade de CPFs
        ttk.Label(input_frame, text="Quantidade de CPFs:").grid(row=0, column=0, padx=5, sticky='w')
        self.quantidade = ttk.Spinbox(input_frame, from_=1, to=1000, width=10)
        self.quantidade.set(10)
        self.quantidade.grid(row=0, column=1, padx=5, sticky='w')
        
        # Seleção de Estado
        ttk.Label(input_frame, text="Estado do CPF:").grid(row=1, column=0, padx=5, pady=10, sticky='w')
        self.estado_var = tk.StringVar()
        self.estado_combobox = ttk.Combobox(input_frame, textvariable=self.estado_var, 
                                          values=list(self.estados.keys()), 
                                          width=50, state='readonly')
        self.estado_combobox.set("Aleatório")
        self.estado_combobox.grid(row=1, column=1, columnspan=2, padx=5, pady=10, sticky='w')
        
        # Checkbox para formatação
        self.formatar_var = tk.BooleanVar(value=True)
        self.formatar_check = ttk.Checkbutton(input_frame, text="Formatar CPFs (ex: 123.456.789-00)", 
                                            variable=self.formatar_var)
        self.formatar_check.grid(row=2, column=0, columnspan=2, pady=10, sticky='w')
        
        # Botão gerar
        ttk.Button(self.window, text="Gerar CPFs", command=self.gerar_cpfs).pack(pady=10)
        
        # Área de texto para resultados
        self.resultado_text = tk.Text(self.window, height=15, width=50)
        self.resultado_text.pack(pady=10)
        
        # Botão salvar
        ttk.Button(self.window, text="Salvar em Excel", command=self.salvar_excel).pack(pady=10)
        
    def calcular_digitos_verificadores(self, base_cpf):
        """Calcula os dois dígitos verificadores de um CPF."""
        # Cálculo do primeiro dígito verificador (DV1)
        soma_dv1 = sum(int(num) * (10 - i) for i, num in enumerate(base_cpf))
        resto_dv1 = (soma_dv1 * 10) % 11
        dv1 = str(0 if resto_dv1 == 10 else resto_dv1)
        
        # Cálculo do segundo dígito verificador (DV2)
        base_com_dv1 = base_cpf + [dv1]
        soma_dv2 = sum(int(num) * (11 - i) for i, num in enumerate(base_com_dv1))
        resto_dv2 = (soma_dv2 * 10) % 11
        dv2 = str(0 if resto_dv2 == 10 else resto_dv2)
        
        return dv1, dv2

    def gerar_cpf_valido(self):
        """Gera um número de CPF válido para o estado selecionado."""
        # Gera os 8 primeiros dígitos aleatoriamente
        base_cpf = [str(random.randint(0, 9)) for _ in range(8)]
        
        # Obtém o dígito do estado selecionado
        estado_selecionado = self.estado_var.get()
        digito_estado = self.estados[estado_selecionado]
        
        # Se for aleatório, gera um dígito aleatório, senão usa o dígito do estado
        if digito_estado == "random":
            base_cpf.append(str(random.randint(0, 9)))
        else:
            base_cpf.append(digito_estado)
        
        # Calcula os dígitos verificadores
        dv1, dv2 = self.calcular_digitos_verificadores(base_cpf)
        return "".join(base_cpf) + dv1 + dv2
    
    def formatar_cpf(self, cpf_str):
        """Aplica a formatação XXX.XXX.XXX-XX a um CPF."""
        return f"{cpf_str[0:3]}.{cpf_str[3:6]}.{cpf_str[6:9]}-{cpf_str[9:11]}"
    
    def gerar_cpfs(self):
        """Gera os CPFs e exibe na interface."""
        try:
            quantidade = int(self.quantidade.get())
            if not 1 <= quantidade <= 1000:
                messagebox.showerror("Erro", "A quantidade deve estar entre 1 e 1000")
                return
            
            self.resultado_text.delete(1.0, tk.END)
            self.cpfs_gerados = []
            
            for _ in range(quantidade):
                cpf = self.gerar_cpf_valido()
                if self.formatar_var.get():
                    cpf_display = self.formatar_cpf(cpf)
                else:
                    cpf_display = cpf
                self.cpfs_gerados.append((cpf_display, cpf))
                self.resultado_text.insert(tk.END, cpf_display + "\n")
            
            messagebox.showinfo("Sucesso", f"{quantidade} CPFs gerados com sucesso!")
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número válido")
    
    def salvar_excel(self):
        """Salva os CPFs gerados em um arquivo Excel com informações adicionais."""
        if not hasattr(self, 'cpfs_gerados') or not self.cpfs_gerados:
            messagebox.showwarning("Aviso", "Gere CPFs primeiro antes de salvar")
            return
        
        try:
            data = []
            estado_selecionado = self.estado_var.get()
            
            for cpf_formatado, cpf_numerico in self.cpfs_gerados:
                digito_estado = cpf_numerico[8]  # Nono dígito
                estado_real = "Desconhecido"
                
                # Determina o estado com base no nono dígito
                for estado, digito in self.estados.items():
                    if digito == digito_estado and digito != "random":
                        estado_real = estado
                        break
                
                data.append({
                    "CPF Formatado": cpf_formatado if self.formatar_var.get() else cpf_numerico,
                    "CPF (Apenas Números)": cpf_numerico,
                    "Estado": estado_real,
                    "Região Selecionada": estado_selecionado
                })
            
            # Cria o DataFrame com as informações
            df = pd.DataFrame(data)
            
            # Gera nome do arquivo com timestamp e estado
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            estado_arquivo = estado_selecionado.split(",")[0].replace(" ", "_")[:20]
            filename = f"cpfs_gerados_{estado_arquivo}_{timestamp}.xlsx"
            
            # Configura o writer do Excel para formatar a planilha
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='CPFs Gerados')
                worksheet = writer.sheets['CPFs Gerados']
                
                # Ajusta a largura das colunas
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    worksheet.column_dimensions[column_letter].width = max_length + 2
            
            # Abre o diretório onde o arquivo foi salvo
            os.startfile(os.path.dirname(os.path.abspath(filename)))
            messagebox.showinfo("Sucesso", f"Arquivo salvo com sucesso:\n{filename}\n\nO diretório foi aberto automaticamente.")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar arquivo:\n{str(e)}")
    
    def run(self):
        """Inicia a aplicação."""
        self.window.mainloop()

if __name__ == "__main__":
    app = GeradorCPF()
    app.run()