from nicegui import app, ui
import random
from botoes import BotaoProcesso, BotaoNumero, BotaoVazio

class Jogo:

    def __init__(self):

        ui.add_css('css/styles.css') # Definindo arquivo de estilo
        self.matriz_botoes = []
        self.list_tamanhos_matriz = {'10x10': 10, '15x15': 15, '20x20': 20}
        self.list_dificuldades = {'Fácil': 1, 'Médio': 2, 'Difícil': 3}
        self.tamanho_matriz = '10x10'
        self.dificuldade = 'Fácil'
        self.quantidade_processos = self.list_tamanhos_matriz[self.tamanho_matriz]*self.list_dificuldades[self.dificuldade] # tamanho * dificuldade
        self.label_qtd_adv = None
        self.tamanho_img_capa = 160

        self.qtd_botoes_clicados = 0 # Se igual qtd maxima de botoes - qtd de processos, define fim do jogo
        self.qtd_advogado = self.quantidade_processos

        # Div principal
        self.container = ui.element('div').classes('p-4 border rounded shadow-md')
        print("Info - Jogo Iniciado!")
        self.inicia_interface(self.tamanho_matriz, self.dificuldade)

        ui.run(reload=False)

    def inicia_interface(self, tamanho_matriz, dificuldade):
        '''
        Inicia construção da interface do jogo.
        Imagem de capa, botões de configuração e botões do jogo.

        Args:
            tamanho_matriz (str): Tamanho da matriz do jogo. {10x10, 15x15, 20x20}
            dificuldade (str): Dificuldade do jogo. {Fácil, Médio, Difícil}
        '''

        # Definindo parametros de jogo na interface
        with self.container:  
            ui.button('x', on_click=self.encerrar_jogo).style("align-self: flex-end; width: 30px; height: 10px;").props('color=red-5 text-color=white')
            ui.image('img/Capa.png').style(f"width: 100%; height: {self.tamanho_img_capa}px; margin-left: 10px;")

            with ui.row().classes('div-parametros'):  
                with ui.column():
                    ui.label("Dificuldade:")
                    ui.select(['Fácil', 'Médio', 'Difícil'], value=dificuldade, on_change=lambda e: self.mudar_config_jogo(self.tamanho_matriz, e.value)).style("width: 100px;")

                with ui.column():
                    ui.label("Tamanho do Campo:")
                    ui.select(['10x10', '15x15', '20x20'], value=tamanho_matriz, on_change=lambda e: self.mudar_config_jogo(e.value, self.dificuldade)).style("width: 100px;")

                with ui.column():
                    ui.label("Quantidade de Advogados:")
                    with ui.row():
                        ui.image('img/adv.png').style("width: 25px; height: 25px; margin-left: 10px;")
                        self.label_qtd_adv = ui.label(f"Número: {self.qtd_advogado}").style("margin-left: 10px; font-size: 18px;")

            ui.button('Reiniciar', on_click=lambda e: self.mudar_config_jogo(self.tamanho_matriz, self.dificuldade)).style("width: 100px; height: 25px; margin-top: 10px;").props('color=orange-5 text-color=white')

            self.definir_botoes(self.list_tamanhos_matriz[self.tamanho_matriz], self.quantidade_processos)

    def mudar_config_jogo(self, tamanho_matriz, dificuldade):
        '''
        Muda configuração do jogo.
        Toda ação de configuração ou de fim de jogo, recarrega a interface.

        Args:
            tamanho_matriz (str): Tamanho da matriz do jogo. {10x10, 15x15, 20x20}
            dificuldade (str): Dificuldade do jogo. {Fácil, Médio, Difícil}
        '''
        self.tamanho_matriz = tamanho_matriz
        self.dificuldade = dificuldade
        self.matriz_botoes = []
        self.qtd_botoes_clicados = 0
        self.quantidade_processos = self.list_tamanhos_matriz[self.tamanho_matriz]*self.list_dificuldades[self.dificuldade]
        self.qtd_advogado = self.quantidade_processos
        self.label_qtd_adv.set_text(f"Número: {self.qtd_advogado}")
        self.tamanho_img_capa = tamanho_matriz*16 # Tamanho muda de acordo com tamanho do campo.
        self.container.clear()

        print("Info - Jogo Reiniciado!")
        self.inicia_interface(self.tamanho_matriz, self.dificuldade)

    def definir_botoes(self, tamanho_matriz, quantidade_processos):
        '''
        Definição de posição dos botões bombas, números e vazios.

        Args:
            tamanho_matriz (int): Tamanho da matriz do jogo. {10, 15, 20}
            quantidade_processos (int): Quantidade de bombas no jogo.
        '''

        # Pegar posicao dos processos
        posicoes_processos = []

        while quantidade_processos != 0:
            
            # i e j aleatorios.
            posicao_linha = random.randint(0, tamanho_matriz-1)
            posicao_coluna = random.randint(0, tamanho_matriz-1)

            # Repetir sorteio caso a posição já tenha sido sorteada
            if (posicao_linha, posicao_coluna) not in posicoes_processos:
                posicoes_processos.append((posicao_linha, posicao_coluna))
                quantidade_processos -= 1

        # Pegar posicao dos botoes numero
        posicao_numeros = []

        # Para cada posição processo, pegar posicoes em volta para definir os numeros
        for posicao_processo in posicoes_processos:

            for posicao_i in range(posicao_processo[0]-1, posicao_processo[0]+2):
                for posicao_j in range(posicao_processo[1]-1, posicao_processo[1]+2):
                    if (posicao_i >= 0 and posicao_i < tamanho_matriz) and (posicao_j >= 0 and posicao_j < tamanho_matriz) and (posicao_i, posicao_j) != posicao_processo:
                        posicao_numeros.append((posicao_i, posicao_j))

        # Mesclar posicoes repetidas em posicao_numeros
        contagem_posicoes_repetidas = {}
        for tupla in posicao_numeros:
            if tupla in contagem_posicoes_repetidas:
                contagem_posicoes_repetidas[tupla] += 1
            else:
                contagem_posicoes_repetidas[tupla] = 1

        # Criando os botões e inserindo em uma matriz
        with ui.grid(columns=tamanho_matriz).classes('gap-2'):
            for i in range(tamanho_matriz):
                linha_botoes = []
                for j in range(tamanho_matriz):
                    if (i,j) in posicoes_processos:
                        botao = BotaoProcesso(linha=i, coluna=j, jogo=self)
                    elif (i,j) in contagem_posicoes_repetidas:
                        botao = BotaoNumero(linha=i, coluna=j, jogo=self, numero=contagem_posicoes_repetidas[(i,j)])
                    else:
                        botao = BotaoVazio(linha=i, coluna=j, jogo=self)
                    linha_botoes.append(botao)
                self.matriz_botoes.append(linha_botoes)

    def add_contagem_acao_clique(self):
        '''
        Para todo botão clicado com o botão esquerdo, incrementa a quantidade de botões clicados.
        '''

        self.qtd_botoes_clicados += 1
        self.define_fim_do_jogo_vitoria() # Verifica se o jogo acabou
        print(f"Info - Botoes clicados: {self.qtd_botoes_clicados}")

    def add_contagem_clique_btdireito(self, flag_clique_btdireito):
        '''
        Para todo botão clicado com o botão direito, incrementa ou decrementa a quantidade
        de bombas marcadas.

        Args:
            flag_clique_btdireito (bool): Flag que indica se o botão foi clicado com o botão direito.
        '''

        if flag_clique_btdireito:
            self.qtd_advogado += 1
            print(f"Info - Advogado removido: {self.qtd_advogado}")
        else:
            self.qtd_advogado -= 1
            print(f"Info - Advogado inserido: {self.qtd_advogado}")
        
        self.label_qtd_adv.set_text(f"Número: {self.qtd_advogado}")

        self.define_fim_do_jogo_vitoria() # Verifica se o jogo acabou
        
    def define_fim_do_jogo_vitoria(self):
        '''
        Se todos os botões foram clicados e todos os processos foram marcados, define o fim do jogo com vitória.
        '''
        
        if self.qtd_botoes_clicados == (self.list_tamanhos_matriz[self.tamanho_matriz]**2)-self.quantidade_processos and self.qtd_advogado == 0:

            modal_vitoria = ui.dialog().props('width=300 height=200 color=white') 
            
            # Adicionando conteúdo de vitoria ao modal
            with modal_vitoria:

                div = ui.element('div').classes('p-4 border rounded shadow-md modal vitoria')
                with div:
                    ui.image('img/adv-paloma.jpg').style(f"width: 213px; height: 236px; padding: 10px;")
                    ui.label('Parabéns! Você acionou um advogado para todos os processos e ganhou!')
                    ui.button('Fechar', on_click=modal_vitoria.close).props('color=green-5 text-color=white')

            modal_vitoria.open()
            print("Info - Parabéns! Você acionou um advogado para todos os processos e ganhou!")
                
    def define_fim_do_jogo_derrota(self):
        '''
        Se clicou em um processo, define o fim do jogo com derrota.
        '''

        modal_derrota = ui.dialog().props('width=300 height=200 color=white')  
        
        # Adicionando conteúdo de derrota ao modal
        with modal_derrota:

            div = ui.element('div').classes('p-4 border rounded shadow-md modal derrota')
            with div:
                ui.image('img/Processo.jpg').style(f"width: 213px; height: 236px; padding: 10px;")
                ui.label('Que pena! Você recebeu um processo e perdeu!')
                ui.button('Fechar', on_click=modal_derrota.close).props('color=red-5 text-color=white')

        # Aciona clique em todos os botoes
        for linha in self.matriz_botoes:
            for botao in linha:

                if botao.ativo:
                    if type(botao) == BotaoProcesso:
                        botao.acao_clique(None, True)
                    else:
                        botao.acao_clique(None)
                
        modal_derrota.open()
        print("Info - Que pena! Você recebeu um processo e perdeu!")

    def encerrar_jogo(self):
        '''
        Encerra a execução do nicegui e fecha o navegador.
        '''

        ui.run_javascript('window.close();')
        app.shutdown()

if __name__ in {"__main__", "__mp_main__"}:
    Jogo()