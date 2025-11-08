import tkinter as tk
from tkinter import messagebox, filedialog 
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import math
class TextWithLineNumbers(ttk.Frame):
    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs) 
        self.text = tk.Text(self, font=("Consolas", 11), wrap="word", borderwidth=0, highlightthickness=0)
        self.linenumbers = tk.Canvas(self, width=40, borderwidth=0, highlightthickness=0)
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)
        self.text.bind("<<Modified>>", self._on_text_modify)
        self.text.bind("<Configure>", self._on_text_modify)
        try:
            style = ttk.Style()
            text_fg_color = style.lookup("TLabel", "foreground", ("secondary",))
            bg_color = style.lookup("TFrame", "background") 
            
            self.text.config(fg=text_fg_color, bg=bg_color) 
            
            self.linenumbers.config(bg=bg_color)
            
            self.ln_fg_color = "#000000"
        except:
            self.text.config(fg="#606060", bg="#ffffff")
            self.linenumbers.config(bg="#f0f0f0")
            self.ln_fg_color = "#000000"


    def _on_text_modify(self, event=None):
        self.linenumbers.delete("all")
        i = self.text.index("@0,0")
        while True :
            dline= self.text.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.linenumbers.create_text(2, y, anchor="nw", text=linenum, fill=self.ln_fg_color, font=("Consolas", 11))
            i = self.text.index("%s+1line" % i)
        self.text.edit_modified(False)

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        self.text.insert(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.text.delete(*args, **kwargs)

class MiniCompilador:
    def __init__(self, root, janela_principal):
        self.root = root
        self.janela_principal = janela_principal
        self.root.title("Compilo Python - Interpretador")
        self.root.geometry("1100x600")

        top_bar_frame = ttk.Frame(root, padding=(10, 10))
        top_bar_frame.pack(fill="x")
        
        button_container = ttk.Frame(top_bar_frame)
        button_container.pack() 

        btn_width = 12 
        
        self.abrir_btn = ttk.Button(button_container, text="Abrir", command=self.abrir_arquivo, bootstyle="info-outline", width=btn_width)
        self.abrir_btn.pack(side="left", padx=5)

        self.salvar_btn = ttk.Button(button_container, text="Salvar", command=self.salvar_arquivo, bootstyle="info-outline", width=btn_width)
        self.salvar_btn.pack(side="left", padx=5)

        self.executar_btn = ttk.Button(button_container, text="Executar", command=self.iniciar_execucao, bootstyle="success-outline", width=btn_width)
        self.executar_btn.pack(side="left", padx=5)

        self.voltar_btn = ttk.Button(button_container, text="Voltar", command=self.voltar_para_inicio, bootstyle="secondary-outline", width=btn_width)
        self.voltar_btn.pack(side="left", padx=5)
        
        self.limpar_btn = ttk.Button(button_container, text="Limpar Tudo", command=self.limpar_tudo, bootstyle="danger-outline", width=btn_width)
        self.limpar_btn.pack(side="left", padx=5)

        paned_window = ttk.Panedwindow(root, orient=tk.HORIZONTAL)
        paned_window.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        codigo_frame = ttk.Frame(paned_window, width=400, height=500, padding=5)
        ttk.Label(codigo_frame, text="Código Fonte").pack(anchor="w", padx=5, pady=(0,5))
        self.codigo_area = TextWithLineNumbers(codigo_frame)
        self.codigo_area.pack(fill="both", expand=True)
        paned_window.add(codigo_frame, weight=1) 
        
        saida_frame = ttk.Frame(paned_window, width=400, height=600, padding=5)
        ttk.Label(saida_frame, text="Saída").pack(anchor="w", padx=5, pady=(0,5))
        
        self.saida_area = tk.Text(saida_frame, state="disabled", font=("Consolas", 11), wrap="word", borderwidth=0)
        
        try:
            style = ttk.Style()
            bg_color = style.lookup("TFrame", "background")
            self.saida_area.config(bg=bg_color)
        except:
            self.saida_area.config(bg="#f0f0f0")
            
        self.saida_area.pack(fill="both", expand=True)
        paned_window.add(saida_frame, weight=1)
        
        self.saida_area.tag_config("sucesso", foreground="#4CAF50")
        self.saida_area.tag_config("erro", foreground="#F44336")
        self.saida_area.tag_config("info", foreground="#2196F3")

        self.codigo_area.insert("1.0",
"""# Comandos de exemplo (válidos)
-Constantes (4 comandos)
pi 
e   
inf
nan

-Potência e Logaritmo (7 comandos)
sqrt 
pow  
exp  
log  
log10
log2 

-Trigonometria e Conversão (8 comandos)
sin    
cos    
tan    
asin   
acos   
atan   
degrees
radians

-Funções Hiperbólicas (3 comandos)
sinh 
cosh 
tanh 

-Arredondamento e Manipulação (4 comandos)
ceil 
floor
fabs 
trunc 

-Combinatória e Teoria dos Números (5 comandos)
factorial
gcd      
lcm      
comb     
perm     

-Checagem de Ponto Flutuante (3 comandos)
isfinite 
isinf    
isnan    
"""
        )
    
    def abrir_arquivo(self):
        filepath = filedialog.askopenfilename(
            title="Abrir arquivo",
            filetypes=[("Arquivos Python", "*.py"), ("Todos os arquivos", "*.*")]
        )
        if not filepath:
            return
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            self.codigo_area.delete("1.0", tk.END)
            self.codigo_area.insert("1.0", content)
        except Exception as e:
            messagebox.showerror("Erro ao Abrir", f"Não foi possível ler o arquivo:\n{e}", parent=self.root)

    def salvar_arquivo(self):
        filepath = filedialog.asksaveasfilename(
            title="Salvar arquivo como",
            defaultextension=".py",
            filetypes=[("Arquivos Python", "*.py"), ("Todos os arquivos", "*.*")]
        )
        if not filepath:
            return
            
        try:
            content = self.codigo_area.get("1.0", tk.END)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("Sucesso", f"Arquivo salvo em:\n{filepath}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Erro ao Salvar", f"Não foi possível salvar o arquivo:\n{e}", parent=self.root)

    def limpar_tudo(self):
        self.codigo_area.delete("1.0", tk.END)
        self.saida_area.config(state="normal")
        self.saida_area.delete("1.0", tk.END)
        self.saida_area.config(state="disabled")

    def voltar_para_inicio(self):
        self.root.destroy()
        self.janela_principal.deiconify()
        
    def iniciar_execucao(self):
        loading_window = tk.Toplevel(self.root)
        loading_window.title("Executando")
        loading_window.geometry("200x150")
        loading_window.transient(self.root)
        loading_window.grab_set()
        loading_window.resizable(False, False)

        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        pos_x = root_x + (root_width // 2) - (200 // 2)
        pos_y = root_y + (root_height // 2) - (150 // 2)
        loading_window.geometry(f"+{pos_x}+{pos_y}")

        ttk.Label(loading_window, text="Executando código...", font=("Arial", 14)).pack(expand=True, pady=20)

        self.executar_btn.config(state="disabled")
        self.voltar_btn.config(state="disabled")
        self.limpar_btn.config(state="disabled")
        self.abrir_btn.config(state="disabled")
        self.salvar_btn.config(state="disabled")
        self.root.update_idletasks()
        self.root.after(200, self.processar_codigo, loading_window)

    def processar_codigo(self, loading_window):
        self.saida_area.config(state="normal")
        self.saida_area.delete("1.0", tk.END)
        
        # --- INÍCIO: Leitura e Validação ---
        linhas = self.codigo_area.get("1.0", tk.END).strip().split("\n")

        for linha in linhas:
            linha = linha.strip()
            
            if not linha or linha.startswith("-") or linha.startswith("#"):
                continue
            # --- FIM: Leitura e Validação ---

            # --- INÍCIO: Análise Léxica / Tokenização ---
            partes = linha.split()
            cmd = partes[0]
            # --- FIM: Análise Léxica / Tokenização ---

            try:
                # --- INÍCIO: Análise Sintática e Execução ---
                if cmd == "print":
                    self.saida_area.insert(tk.END, " ".join(partes[1:]) + "\n", "info")
                elif cmd == "msg":
                    messagebox.showinfo("Mensagem", " ".join(partes[1:]), parent=self.root)
                    self.saida_area.insert(tk.END, "Mensagem exibida\n", "info")
                elif cmd == "pi":
                    self.saida_area.insert(tk.END, f"{math.pi}\n", "sucesso")
                elif cmd == "e":
                    self.saida_area.insert(tk.END, f"{math.e}\n", "sucesso")
                elif cmd == "inf":
                    self.saida_area.insert(tk.END, f"{math.inf}\n", "sucesso")
                elif cmd == "nan":
                    self.saida_area.insert(tk.END, f"{math.nan}\n", "sucesso")
                elif cmd == "sqrt":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.sqrt(x)}\n", "sucesso")
                elif cmd == "cbrt":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{x ** (1/3)}\n", "sucesso")
                elif cmd == "pow":
                    x, y = float(partes[1]), float(partes[2])
                    self.saida_area.insert(tk.END, f"{math.pow(x, y)}\n", "sucesso")
                elif cmd == "exp":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.exp(x)}\n", "sucesso")
                elif cmd == "log":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.log(x)}\n", "sucesso")
                elif cmd == "log10":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.log10(x)}\n", "sucesso")
                elif cmd == "log2":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.log2(x)}\n", "sucesso")
                elif cmd == "sin":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.sin(x)}\n", "sucesso")
                elif cmd == "cos":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.cos(x)}\n", "sucesso")
                elif cmd == "tan":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.tan(x)}\n", "sucesso")
                elif cmd == "asin":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.asin(x)}\n", "sucesso")
                elif cmd == "acos":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.acos(x)}\n", "sucesso")
                elif cmd == "atan":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.atan(x)}\n", "sucesso")
                elif cmd == "degrees":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.degrees(x)}\n", "sucesso")
                elif cmd == "radians":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.radians(x)}\n", "sucesso")
                elif cmd == "sinh":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.sinh(x)}\n", "sucesso")
                elif cmd == "cosh":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.cosh(x)}\n", "sucesso")
                elif cmd == "tanh":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.tanh(x)}\n", "sucesso")
                elif cmd == "ceil":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.ceil(x)}\n", "sucesso")
                elif cmd == "floor":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.floor(x)}\n", "sucesso")
                elif cmd == "fabs":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.fabs(x)}\n", "sucesso")
                elif cmd == "trunc":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.trunc(x)}\n", "sucesso")
                elif cmd == "factorial":
                    x = int(partes[1])
                    self.saida_area.insert(tk.END, f"{math.factorial(x)}\n", "sucesso")
                elif cmd == "gcd":
                    x, y = int(partes[1]), int(partes[2])
                    self.saida_area.insert(tk.END, f"{math.gcd(x, y)}\n", "sucesso")
                elif cmd == "lcm":
                    x, y = int(partes[1]), int(partes[2])
                    self.saida_area.insert(tk.END, f"{math.lcm(x, y)}\n", "sucesso")
                elif cmd == "comb":
                    n, k = int(partes[1]), int(partes[2])
                    self.saida_area.insert(tk.END, f"{math.comb(n, k)}\n", "sucesso")
                elif cmd == "perm":
                    n, k = int(partes[1]), int(partes[2])
                    self.saida_area.insert(tk.END, f"{math.perm(n, k)}\n", "sucesso")
                elif cmd == "isfinite":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.isfinite(x)}\n", "sucesso")
                elif cmd == "isinf":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.isinf(x)}\n", "sucesso")
                elif cmd == "isnan":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.isnan(x)}\n", "sucesso")
                elif cmd == "max":
                    nums = [float(n) for n in partes[1:]]
                    self.saida_area.insert(tk.END, f"{max(nums)}\n", "sucesso")
                elif cmd == "min":
                    nums = [float(n) for n in partes[1:]]
                    self.saida_area.insert(tk.END, f"{min(nums)}\n", "sucesso")
                else:
                    self.saida_area.insert(tk.END, f"Comando não reconhecido: {linha}\n", "erro")
                # --- FIM: Análise Sintática e Execução ---
            
            # --- INÍCIO: Tratamento de Erros ---
            except IndexError:
                self.saida_area.insert(tk.END, f"Erro em '{linha}': Por favor, insira o(s) valor(es) para o comando.\n", "erro")
            except ValueError:
                self.saida_area.insert(tk.END, f"Erro em '{linha}': Argumento inválido. Verifique se os números estão corretos.\n", "erro")
            except Exception as e:
                self.saida_area.insert(tk.END, f"Erro ao executar '{linha}': {e}\n", "erro")
            # --- FIM: Tratamento de Erros ---
        
        self.saida_area.config(state="disabled")
        self.executar_btn.config(state="normal")
        self.voltar_btn.config(state="normal")
        self.limpar_btn.config(state="normal")
        self.abrir_btn.config(state="normal")
        self.salvar_btn.config(state="normal")
        loading_window.destroy()

class TelaBoasVindas:
    def __init__(self, root):
        self.root = root
        self.root.title("Boas-Vindas ao Compilo Python")
        self.root.geometry("700x550")
        self.root.resizable(True, True) 
        
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10)

        top_frame = ttk.Frame(root)
        top_frame.pack(side="top", fill="x", pady=20, padx=10)

        title_label = ttk.Label(top_frame, text="Bem-vindo ao Compilo Python!", font=("Arial", 18, "bold"), bootstyle="primary")
        title_label.pack(pady=5)

        self.content_frame = ttk.Frame(root)
        self.content_frame.pack(fill="both", expand=True, pady=20, padx=20)

        welcome_text = (
            "Este compilador foi desenvolvido pelo grupo:\n"
            "Aaron, Walisson, Jonathan, Marcos e Victor.\n\n"
            "Aqui você poderá utilizar diversos comandos para aprender e praticar programação.\n"
            "Clique nos botões abaixo para conhecer mais sobre o compilador."
        )
        self.welcome_label = ttk.Label(self.content_frame, text=welcome_text, justify="center", font=("Arial", 14), anchor="center")
        self.welcome_label.pack(pady=20, fill="x", expand=True)

        explicacao_btn = ttk.Button(self.content_frame, text="Sobre o Compilador", command=self.mostrar_explicacao, bootstyle="info-outline")
        explicacao_btn.pack(pady=10)

        avancar_btn = ttk.Button(self.content_frame, text="Avançar para o Compilador", command=self.avancar_para_compilador, bootstyle="success")
        avancar_btn.pack(pady=10)

        footer_label = ttk.Label(root, text="Integrantes: Aaron, Walisson, Jonathan, Marcos e Victor", font=("Arial", 10), bootstyle="secondary")
        footer_label.pack(side="bottom", pady=10)

        self.content_frame.bind('<Configure>', self._on_resize)

    def _on_resize(self, event):
        nova_largura = event.width - 20 
        self.welcome_label.config(wraplength=nova_largura)
    
    def mostrar_explicacao(self):
        messagebox.showinfo(
            "Sobre o Compilador",
            "Nosso compilador possui no mínimo 30 comandos que permitem criar e executar programas de forma eficiente. "
            "Ele foi desenvolvido para facilitar a programação e otimizar o aprendizado dos conceitos fundamentais.",
            parent=self.root
        )

    def avancar_para_compilador(self):
        self.root.withdraw()
        compilador_window = tk.Toplevel(self.root)
        app_compilador = MiniCompilador(compilador_window, self.root)
        compilador_window.protocol("WM_DELETE_WINDOW", self.root.destroy)

if __name__ == "__main__":
    main_root = ttk.Window(themename="superhero")
    
    app = TelaBoasVindas(main_root)
    main_root.mainloop()