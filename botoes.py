from nicegui import ui
from nicegui.events import MouseEventArguments

class Botao:
    def __init__(self, linha, coluna, jogo):

        self.linha = linha
        self.coluna = coluna
        self.id = "bt"+str(linha)+str(coluna)
        self.jogo = jogo
        self.ativo = True
        self.flag_clique_btdireito = False
        self.img_adv = None
        self.button = ui.button('', on_click=self.acao_clique).props(f'id="{self.id}"').style('width:32px; height:32px;')
        self.button.on('mousedown', lambda e: self.acao_clique_btdireito(e))

        ui.timer(0, self.acaojs_clique_btdireito, once=True)

    def acao_clique(self, _):
        '''
        Função que realiza o clique no botão, desabilita ele e adiciona contagem de clique no jogo.\n
        BotaoProcesso: Mostra o processo quando clicado e aciona fim de jogo.\n
        BotaoNumero: Mostra a quantidade de processos que estão encostados nele.\n
        BotaoVazio: Clique em todos os botões vazios em volta até que seja um BotaoNumero.
        '''
        
        if self.ativo and not self.flag_clique_btdireito:
            self.ativo = 0
            self.button.classes('disabled')

            

    def acao_clique_btdireito(self, event: MouseEventArguments):
        '''
        Função que executa ação no clique do botão direito.
        Adiciona ou remove um advogado do botão e atualiza a contagem de advogados no jogo.
        
        Args:
            event (MouseEventArguments): Evento do clique do botão.
        '''

        # Verifica se foi um clique com o botão direito
        if event.args['button'] == 2:  


            if not self.flag_clique_btdireito:

                if self.jogo.qtd_advogado > 0:
                    self.jogo.add_contagem_clique_btdireito(self.flag_clique_btdireito)
                    self.flag_clique_btdireito = not self.flag_clique_btdireito
                    self.button.props('color=orange-3')
                    with self.button:
                        self.img_adv = ui.image('https://img.icons8.com/ios-filled/50/1A1A1A/lawyer.png').style("width: 20px; height: 20px;")
            else:
                self.jogo.add_contagem_clique_btdireito(self.flag_clique_btdireito)
                self.flag_clique_btdireito = not self.flag_clique_btdireito
                self.button.props('color=primary')
                self.img_adv.delete()
    
    def acaojs_clique_btdireito(self):
        '''
        Função que executa JavaScript para desabilitar o clique direito do mouse que abre menu no navegador.
        '''

        ui.run_javascript(f'''

            const bt = document.querySelector("#{self.id}");
                     
            bt.addEventListener("contextmenu", event => {{
                event.preventDefault(); // Permite o drop
            }});

        ''')

class BotaoProcesso(Botao):
    
    def acao_clique(self, event, clique_automatico=False):
        super().acao_clique(event)

        if not self.flag_clique_btdireito:
            self.button.props('color=red')
            self.button.update()

            ui.run_javascript(f'''

                const bt = document.querySelector("#{self.id}");         
                bt.innerHTML = '<img width="20" height="20" src="https://img.icons8.com/ios-filled/50/1A1A1A/policy-document.png" alt="policy-document"/>'; 

            ''')

            if not clique_automatico:
                self.jogo.define_fim_do_jogo_derrota()

class BotaoNumero(Botao):
    def __init__(self, linha, coluna, jogo, numero):
        super().__init__(linha, coluna, jogo)
        self.numero = numero

    def acao_clique(self, event):
        super().acao_clique(event)

        if not self.flag_clique_btdireito:
            self.jogo.add_contagem_acao_clique()
            self.button.text = str(self.numero)
            self.button.update()

class BotaoVazio(Botao):

    def __init__(self, linha, coluna, jogo):
        super().__init__(linha, coluna, jogo)
        self.matriz_botoes = jogo.matriz_botoes

    def acao_clique(self, event):
        super().acao_clique(event)

        if not self.flag_clique_btdireito:
            self.jogo.add_contagem_acao_clique()
            self.button.props('color=grey-3')
            self.button.update()
            self.expandir_vazio(self.linha, self.coluna)
        
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
                if (i >= 0 and i < len(self.matriz_botoes)) and (j >= 0 and j < len(self.matriz_botoes)) and (i, j) != (bt_linha, bt_coluna) and self.matriz_botoes[i][j].ativo:
                        self.matriz_botoes[i][j].acao_clique(None)


