import json
import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import *
import os
import pathlib
from platform import system
import whatsappBackEnd
from time import sleep
from threading import *


diretorio = os.getcwd()
tem_anexo = False
listaClientes = [f.split(".")[0] for f in os.listdir(r"{dir}/contatos".format(dir=diretorio)) if os.path.isfile(os.path.join(r"{dir}/contatos".format(dir=diretorio), f))]
scriptRodando = False

def anexo(path):
    global tem_anexo
    global path_anexo
    if path != None:
        tem_anexo = True
    path_anexo = path
    outputFinal('Imagem {anexo} anexada'.format(anexo=path.split("\\")[-1]))


class ToolTip(object):  # Classe on hover tooltip

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def CreateToolTip(widget, text):  # Função para criar on hover text
    tool_tip = ToolTip(widget)

    def enter(event):
        tool_tip.showtip(text)

    def leave(event):
        tool_tip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


def copyImage(path: str) -> None:
    if system().lower() == "linux":
        if pathlib.Path(path).suffix in (".PNG", ".png"):
            os.system(f"copyq copy image/png - < {path}")
        elif pathlib.Path(path).suffix in (".jpg", ".JPG", ".jpeg", ".JPEG"):
            os.system(f"copyq copy image/jpeg - < {path}")
        else:
            raise Exception(
                f"Formato de arquivo {pathlib.Path(path).suffix} nao e suportado!"
            )
    elif system().lower() == "windows":
        from io import BytesIO
        import win32clipboard
        from PIL import Image
        try:
            image = Image.open(path)
            output = BytesIO()
            image.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]
            output.close()
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()
        except AttributeError:
            pass
    elif system().lower() == "darwin":
        if pathlib.Path(path).suffix in (".jpg", ".jpeg", ".JPG", ".JPEG"):
            os.system(
                f"osascript -e 'set the clipboard to (read (POSIX file \"{path}\") as JPEG picture)'"
            )
        else:
            raise Exception(
                f"Tipo de arquivo {pathlib.Path(path).suffix} nao e suportado!"
            )
    else:
        raise Exception(f"Sistema operacional nao suportado: {system().lower()}")

            
def closing():
    try:
        whatsappBackEnd.driver.quit()
    except:
        pass
    janela_principal.destroy()
    
    
def selecionaArquivo(tipo="", ext=""):  # Abrir file explorer
    filename = filedialog.askopenfilename(initialdir=".",
                                          title="Seleciona um arquivo",
                                          filetypes=((tipo,
                                                      ext),
                                                     ("all files",
                                                      "*.*")))
    if filename:
        filepath = os.path.abspath(filename)
        return filepath


def criarContato(arquivo):  # Cria arquivos json para os contatos baseado em uma planilha do excel
    try:
        infos = pd.read_excel(arquivo).to_json(orient='records')
        parsed = json.loads(infos)
        
        iniciarProgresso("indeterminate")
        barraProgresso.start()
        
        for client in parsed:
            try:
                with open(r"{dir}\contatos\{nome}.json".format(
                        nome=client['Nome'], dir=diretorio), "w") as outfile:
                    outfile.write(json.dumps(client, indent=4, ensure_ascii=True))
            except:
                pass
                
        global listaClientes
        listaClientes = [f.split(".")[0] for f in os.listdir(r"{dir}/contatos".format(dir=diretorio)) if os.path.isfile(os.path.join(r"{dir}/contatos".format(dir=diretorio), f))]
        
        outputFinal('Contatos criados!')
        
        barraProgresso.stop()
        janela_principal.after(10000, lambda: [barraProgresso.destroy(), mensagemEmProgresso.destroy()])
        
    except ValueError:
        outputFinal('')


# Interface
def mudarEstadoBotaoParar():
    if scriptRodando:
        botaoParar['state'] = 'normal'
    if not scriptRodando:
        botaoParar['state'] = 'disabled'


def pararEnvio():
    global scriptRodando
    scriptRodando = False
    outputFinal("Parando envio")


def outputFinal(txt: str, tempo=3):
    outputAtual = tk.Label(janela_principal, text=txt)
    outputAtual.place(x=80, y=360)
    janela_principal.after(tempo * 1000, outputAtual.destroy)


def enviarMensagem(listaDeClientes: list, mensagem: str):
    global tem_anexo, scriptRodando
    scriptRodando = True
    mudarEstadoBotaoParar()
    iniciarProgresso("determinate")
    if tem_anexo:
        for cliente in listaDeClientes:
            if scriptRodando:
                try:
                    copyImage(path_anexo)
                    outputFinal("Enviando mensagem para {Contato}!".format(Contato=cliente['Nome']))
                    janela_principal.update()
                    whatsappBackEnd.sendWhatsappMsgAnexo(str(cliente['Telefone']), mensagem)
                    if barraProgresso['value'] < 100:
                        barraProgresso['value'] += 100/len(listaDeClientes)
                        janela_principal.update_idletasks()
                        
                    sleep(2)
                    
                except:
                    whatsappBackEnd.is_connected()
                    sleep(10)
            else:
                tem_anexo = False
                scriptRodando = False
                mudarEstadoBotaoParar()
                janela_principal.after(10000, lambda: [barraProgresso.destroy(), mensagemEmProgresso.destroy()])
                break
    else:
        for cliente in listaDeClientes:
            if scriptRodando:
                try:
                    outputFinal("Enviando mensagem para {Contato}!".format(Contato=cliente['Nome']))
                    janela_principal.update()
                    whatsappBackEnd.sendWhatsappMsg(str(cliente['Telefone']), mensagem)
                    if barraProgresso['value'] < 100:
                        barraProgresso['value'] += 100/len(listaDeClientes)
                        janela_principal.update_idletasks()
                        
                    sleep(2)
                    
                except:
                    whatsappBackEnd.is_connected()
                    sleep(10)
            else:
                tem_anexo = False
                scriptRodando = False
                mudarEstadoBotaoParar()
                janela_principal.after(10000, lambda: [barraProgresso.destroy(), mensagemEmProgresso.destroy()])
                break
            
    tem_anexo = False
    scriptRodando = False
    mudarEstadoBotaoParar()
    janela_principal.after(10000, lambda: [barraProgresso.destroy(), mensagemEmProgresso.destroy()])


def pegarInput():
    INPUT = input_box.get("1.0", "end-1c")
    texto_formatado = INPUT.format(Nome="Jefferson")
    return texto_formatado
    

def iniciarProgresso(modo: str):
    global mensagemEmProgresso, barraProgresso
    mensagemEmProgresso = tk.Label(janela_principal, text="Progresso:")
    barraProgresso = ttk.Progressbar(
    janela_principal,
    orient='horizontal',
    mode=modo,
    length=200,
)
    mensagemEmProgresso.place(x=80, y=315)
    barraProgresso.place(x=80, y=335)
    

def confirmarSelecao():
    clientesSelecionados = []
    for i in caixaSelecao.curselection():
        clientesSelecionados.append(caixaSelecao.get(i))
    
    return clientesSelecionados


def dictClientes(list):
    dictList = []
    j = list
    for i in j:
        f = open(r'{dir}/contatos/{contato}.json'.format(dir=diretorio, contato = i))
        dictList.append(json.load(f))
    
    return dictList


def abrirCaixaSelecao():
    global caixaSelecao
    global novaJanela
    novaJanela = tk.Toplevel()
    novaJanela.title("Seleção de contatos")
    caixaSelecao = Listbox(novaJanela, selectmode= "multiple")
    for cadaCliente in range(len(listaClientes)):
        caixaSelecao.insert(END, listaClientes[cadaCliente])
        
        caixaSelecao.itemconfig(cadaCliente,
                bg = "#e0dfdc" if cadaCliente % 2 == 0 else "white")
    caixaSelecao.pack()
    
    botaoConfirmar = tk.Button(novaJanela, text="Confirmar seleção", command=lambda: [Thread(target = lambda: enviarMensagem(dictClientes(confirmarSelecao()), pegarInput())).start()])
    botaoSelecionarTodos = tk.Button(novaJanela, text="Enviar para todos", command=lambda: [Thread(target = lambda: enviarMensagem(dictClientes(listaClientes), pegarInput())).start()])
    botaoSelecionarTodos.pack()
    botaoConfirmar.pack()

   
janela_principal = tk.Tk()
pausar_icon = tk.PhotoImage(file=r"{dir}\icons\pause-icon.png".format(dir=diretorio))
continuar_icon = tk.PhotoImage(file=r"{dir}\icons\continuar-icon.png".format(dir=diretorio))
contato_icon = tk.PhotoImage(file=r"{dir}\icons\contato.png".format(dir=diretorio))
anexo_icon = tk.PhotoImage(file=r"{dir}\icons\anexo-icon.png".format(dir=diretorio))
send_icon = tk.PhotoImage(file=r"{dir}\icons\send-icon.png".format(dir=diretorio))


botaoContato = tk.Button(janela_principal, image=contato_icon, height=50,
                          width=50,
                          text="Show",
                          command=lambda: Thread(target = lambda: criarContato(selecionaArquivo("Planilha do Microsoft Excel", "*.xlsx"))).start())

botaoAnexo = tk.Button(janela_principal, image=anexo_icon, height=25,
                        width=130,
                        text="Show",
                        command=lambda: anexo(selecionaArquivo("Arquivos de imagem", "*.jpg *.jpeg *.png *.gif")))

botaoEnviar = tk.Button(janela_principal, image=send_icon, height=25,
                        width=130,
                        text="Show",
                        command=abrirCaixaSelecao)

botaoParar = tk.Button(janela_principal, text="Parar", image = pausar_icon, height=25, width=130, state="disabled", command=pararEnvio)

janela_principal.title("ZaptZaptSender")
janela_principal.geometry("500x400")
janela_principal.iconbitmap('icons\icon.ico')
input_box = tk.Text(janela_principal, height = 15, width = 42, bg="#7affb6")
janela_principal.resizable(width=False, height=False)
botaoContato.place(x=444, y=344)
botaoAnexo.place(x=350, y=80)
botaoEnviar.place(x=350, y=38)
input_box.place(x=10,y=15)
botaoParar.place(x=350, y=122)
CreateToolTip(botaoContato, text="Criar contatos")
CreateToolTip(botaoAnexo, text="Anexar arquivo")
janela_principal.protocol("WM_DELETE_WINDOW", closing)
janela_principal.mainloop()
