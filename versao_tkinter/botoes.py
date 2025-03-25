import tkinter as tk

class Botao:
    def __init__(self, master, text, row, column, jogo):

        self.master = master
        self.jogo = jogo
        self.button = tk.Button(master, text=text, width=5, height=2, bg='green')
        self.button.grid(row=row, column=column, padx=0, pady=0)
        self.button.bind("<Button-1>", self.on_click)
        self.button.bind("<Button-3>", self.on_right_click)
        self.right_click_flag = False

    def on_click(self, event):
        '''
        Função que realiza o clique no botão.\n
        BotaoBomba: Mostra a bomba quando clicado.\n
        BotaoNumero: Mostra a quantidade de bombas que encosta nele.\n
        BotaoVazio: Clique em todos os botões vazios em volta até que seja um BotaoNumero.
        '''
        
        if self.button.cget("state") == "disabled":
            return
        
        self.jogo.add_contagem_on_click()
        self.button.config(state="disabled")
    
    def on_right_click(self, event):

        self.jogo.add_contagem_on_right_click(self.right_click_flag)

        if self.right_click_flag:
            self.button.config(text="")
        else:
            self.button.config(text="X")

        self.right_click_flag = not self.right_click_flag


class BotaoBomba(Botao):
    
    def on_click(self, event):
        super().on_click(event)

        self.button.config(text="Bomba!", bg="#EB1D1D", fg="#DEDDDD")
        self.jogo.define_fim_do_jogo_derrota()


class BotaoNumero(Botao):
    def __init__(self, master, text, row, column, jogo, numero):
        super().__init__(master, text, row, column, jogo)
        self.numero = numero

    def on_click(self, event):
        super().on_click(event)

        self.button.config(text=str(self.numero), bg='#EBE0D0')


class BotaoVazio(Botao):

    def __init__(self, master, text, row, column, jogo):
        super().__init__(master, text, row, column, jogo)
        self.matriz_botoes = jogo.matriz_botoes


    def on_click(self, event):
        super().on_click(event)

        self.button.config(text="", bg="white")
        self.expandir_vazio(self.button.grid_info()["row"], self.button.grid_info()["column"])
    
    def expandir_vazio(self, bt_linha, bt_coluna):
        '''
        Função vai buscar em volta do botão clicado se existe mais botões vazios na matriz_botoes.
        A cada novo botão vazio ele clica no botão, gerando uma recursão, onde o caso base é o clique em um BotaoNumero.

        Args:
            bt_linha (int): Número da linha para indentificar a posição do botão que está sendo clicado. 
            bt_coluna (int): Número da coluna para indentificar a posição do botão que está sendo clicado.

        '''
        for i in range(bt_linha-1, bt_linha+2):
            for j in range(bt_coluna-1, bt_coluna+2):
                if (i >= 0 and i < len(self.matriz_botoes)) and (j >= 0 and j < len(self.matriz_botoes)) and (i, j) != (bt_linha, bt_coluna) and self.matriz_botoes[i][j].button.cget("state") != "disabled":
                        self.matriz_botoes[i][j].on_click(None)


