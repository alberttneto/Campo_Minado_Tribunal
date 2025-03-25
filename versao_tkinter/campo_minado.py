import tkinter as tk
import random
from botoes import BotaoBomba, BotaoNumero, BotaoVazio

class Jogo:

    def __init__(self, tamanho_matriz, quantidade_bombas):

        self.tamanho_matriz = tamanho_matriz
        self.quantidade_bombas = quantidade_bombas
        self.matriz_botoes = []
        self.qtd_botoes_clicados = 0
        self.qtd_bombas_marcadas = 0

        # Definindo a interface do jogo
        self.janela = tk.Tk()
        frame_botoes = tk.Frame(self.janela)
        frame_botoes.pack()

        self.definir_botoes(quantidade_bombas, tamanho_matriz, frame_botoes=frame_botoes)
        self.janela.mainloop()

    def definir_botoes(self, quantidade_bombas, tamanho_matriz, frame_botoes):

        # Pegar posicao das bombas
        posicoes_bombas = []

        while quantidade_bombas != 0:

            posicao_linha = random.randint(0, tamanho_matriz-1)
            posicao_coluna = random.randint(0, tamanho_matriz-1)

            # Repetir sorteio caso a posição já tenha sido sorteada
            if (posicao_linha, posicao_coluna) not in posicoes_bombas:
                posicoes_bombas.append((posicao_linha, posicao_coluna))
                quantidade_bombas -= 1

        # Pegar posicao dos botoes numero
        posicao_numeros = []

        for posicao_bomba in posicoes_bombas:

            for posicao_i in range(posicao_bomba[0]-1, posicao_bomba[0]+2):
                for posicao_j in range(posicao_bomba[1]-1, posicao_bomba[1]+2):
                    if (posicao_i >= 0 and posicao_i < tamanho_matriz) and (posicao_j >= 0 and posicao_j < tamanho_matriz) and (posicao_i, posicao_j) != posicao_bomba:
                        posicao_numeros.append((posicao_i, posicao_j))

        # Mesclar posicoes repetidas em posicao_numeros
        contagem_posicoes_repetidas = {}
        for tupla in posicao_numeros:
            if tupla in contagem_posicoes_repetidas:
                contagem_posicoes_repetidas[tupla] += 1
            else:
                contagem_posicoes_repetidas[tupla] = 1

        # Criando os botões
        for i in range(tamanho_matriz):
            linha_botoes = []
            for j in range(tamanho_matriz):
                if (i,j) in posicoes_bombas:
                    botao = BotaoBomba(frame_botoes, text=f"", row=i, column=j, jogo=self)
                elif (i,j) in contagem_posicoes_repetidas:
                    botao = BotaoNumero(frame_botoes, text=f"", row=i, column=j, jogo=self, numero=contagem_posicoes_repetidas[(i,j)])
                else:
                    botao = BotaoVazio(frame_botoes, text=f"", row=i, column=j, jogo=self)
                linha_botoes.append(botao)
            self.matriz_botoes.append(linha_botoes)

    def inicia_interface(self, janela):

        # Criando a janela principal
        janela.title("Campo Minado")

        # Criando o frame superior
        frame_superior = tk.Frame(janela, height=50, bg="white")
        frame_superior.pack(fill=tk.X)

        # Adicionando o botão de opções no canto direito do frame superior
        botao_opcoes = tk.Button(frame_superior, text="Opções")
        botao_opcoes.pack(side=tk.RIGHT, padx=10, pady=10)

        # Criando um frame para os botões da matriz
        frame_botoes = tk.Frame(janela)
        frame_botoes.pack()

        return frame_botoes

    def add_contagem_on_click(self):

        self.qtd_botoes_clicados += 1
        self.define_fim_do_jogo_vitoria()
        print(f"Bomba Marcada: {self.qtd_bombas_marcadas}")
        print(f"Botoes clicados: {self.qtd_botoes_clicados}")

    def add_contagem_on_right_click(self, right_click_flag):

        if right_click_flag:
            self.qtd_bombas_marcadas -= 1
        else:
            self.qtd_bombas_marcadas += 1

        self.define_fim_do_jogo_vitoria()
        print(f"Teste 1: {self.qtd_botoes_clicados == (self.tamanho_matriz**2)-self.quantidade_bombas} \n"+
              f"Teste 2: {self.qtd_bombas_marcadas == self.quantidade_bombas}")
        print(f"Bomba Marcada: {self.qtd_bombas_marcadas}")

    def define_fim_do_jogo_vitoria(self):

        if self.qtd_botoes_clicados == (self.tamanho_matriz**2)-self.quantidade_bombas and self.qtd_bombas_marcadas == self.quantidade_bombas:
            print("Fim do jogo. Você ganhou!")
            
    def define_fim_do_jogo_derrota(self):

        print("Que pena. Você perdeu!")



if __name__ == "__main__":
    Jogo(20, 40)