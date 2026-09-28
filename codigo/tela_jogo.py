from constantes import *  # Você pode usar as constantes definidas em constantes.py, se achar útil
                          # Por exemplo, usar a constante CORACAO é o mesmo que colocar a string '❤'
                          # diretamente no código
import motor_grafico as motor  # Utilize as funções do arquivo motor_grafico.py para desenhar na tela
                               # Por exemplo: motor.preenche_fundo(janela, [0, 0, 0]) preenche o fundo de preto
import random


def desenha_parede(janela, estado, altura_tela, largura_tela): # desenha a parede
    mapa = estado["mapa"]
    deltax = (largura_tela - len(mapa[0]))//2
    deltay = (altura_tela - len(mapa))//2
    for parede in estado["paredes"]:
        motor.desenha_string(janela, parede[0] + deltax, parede[1] + deltay, PAREDE, CINZA_ESCURO_AZULADO, CINZA_MUITO_ESCURO_AZULADO)

def desenha_mapa(janela, estado, altura_tela, largura_tela): #desenha o mapa
    mapa = estado["mapa"]
    deltax = (largura_tela - len(mapa[0]))//2
    deltay = (altura_tela - len(mapa))//2
    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            if (i + j) % 2 == 0:
                motor.desenha_string(janela, j + deltax, i + deltay, '▯', CINZA_MEDIO_AZULADO, CINZA_ESCURO_AZULADO)
            else:
                motor.desenha_string(janela, j + deltax, i + deltay, '▯', CINZA_CLARO_AZULADO, CINZA_ESCURO_AZULADO)

def desenha_portal(janela, estado, altura_tela, largura_tela): #desenha o portal
    mapa = estado["mapa"]
    deltax = (largura_tela - len(mapa[0]))//2
    deltay = (altura_tela - len(mapa))//2
    motor.desenha_string(janela, 1 + deltax, deltay + 10, "░", ROXO2, ROXO)
    motor.desenha_string(janela, 1 + deltax, deltay + 9, "░", ROXO2, ROXO)
    motor.desenha_string(janela, 1 + deltax, deltay + 11, "░", ROXO2, ROXO)

def desenha_monstro(janela, estado, altura_tela, largura_tela):
    mapa = estado["mapa"]
    deltax = (largura_tela - len(mapa[0]))//2
    deltay = (altura_tela - len(mapa))//2
    for monstros in estado["monstros"]:
        if monstros["tipo"] != DRAGAO:
            motor.desenha_string(janela, monstros["posicao"][0] + deltax, monstros["posicao"][1]+ deltay, monstros["tipo"], CINZA_MEDIO_AZULADO, monstros["cor"])
        else:
            desenho = DRAGAO
            for linha in range(monstros["altura"]):
                for coluna in range(monstros["largura"]):
                    pixel = desenho[linha][coluna]
                    if pixel != " ":
                        motor.desenha_string(janela, monstros["posicao"][0] + deltax + coluna, linha + monstros["posicao"][1]+ deltay, pixel, CINZA_MEDIO_AZULADO, monstros["cor"])

def desenha_tela(janela, estado, altura_tela, largura_tela): #desenha toda a tela, chama as outras funcoes de desenho deste arquico
    motor.preenche_fundo(janela, PRETO)
    mapa = estado["mapa"]
    deltax = (largura_tela - len(mapa[0]))//2
    deltay = (altura_tela - len(mapa))//2
    desenha_mapa(janela, estado, altura_tela, largura_tela)
    motor.desenha_string(janela, estado["pos_jogador"][0] + deltax, estado["pos_jogador"][1]+ deltay, JOGADOR, CINZA_ESCURO_AZULADO, BRANCO)
    for objeto in estado["objetos"]:
        motor.desenha_string(janela, objeto["posicao"][0] + deltax, objeto["posicao"][1]+ deltay, objeto["tipo"], CINZA_MEDIO_AZULADO, objeto["cor"])  
    desenha_monstro(janela, estado, altura_tela, largura_tela)
    motor.desenha_string(janela, 0+ deltax, deltay-1, estado["max_vidas"]*'🤍', PRETO, BRANCO)
    motor.desenha_string(janela, 0+ deltax, deltay-1, estado["vidas"]*'🧡', PRETO, VERMELHO)
    desenha_parede(janela, estado, altura_tela, largura_tela)
    motor.desenha_string(janela, 0+ deltax, deltay+len(mapa), estado["mensagem"], PRETO, BRANCO)
    desenha_portal(janela, estado, altura_tela, largura_tela)
    motor.desenha_string(janela, len(mapa[0]) + deltax -13, deltay-1, f"nivel:{estado["nivel"]}  xp:{estado["xp"]}", PRETO, BRANCO)

def executa_batalha(estado, monstro): #essa funcao executa a batalha entre o jogador e o monstro quando eles se encontram, ela é chamada em move jogador
    if estado["jabateu"]:
        return False
    estado["jabateu"] = True
    #transforma os simbolos das constantes em nomes dos monstros
    nomes_monstros = {
        GOSMA: "gosma",
        ZUMBI: "zumbi",
        ESQUELETO: "esqueleto",
        DRAGAO: "dragao"
    }
    nome = nomes_monstros[monstro["tipo"]]
    probmonstro = monstro["probatk"] * 100
    sorteio = random.randint(1,100)
    if sorteio <= probmonstro:
        estado['vidas'] -= 1
        estado["mensagem"] = f"o monstro {nome} te atacou"
        if estado["vidas"] <= 0:
            #jogador morre e vai pra tela de fim de jogo
            estado["vidas"] = 5
            estado["tela_atual"] = TELA_GAMEOVER
    else:
        monstro["vida"] -= 1
        estado["mensagem"] = f"voce atacou o monstro {nome}"
        if monstro["vida"] <= 0:
            estado['monstros'].remove(monstro)
            quantixp = monstro["xp"]
            ganha_xp(estado, quantixp)
            if "SUBIU DE NIVEL" not in estado["mensagem"]:
                estado["mensagem"] = f"voce matou o monstro {nome} e ganhou {quantixp} de xp"
            return True
    return False
    
def move_jogador(estado, tecla): #funcao feita para que a funcao def atualiza estado nao fique tao grande, ela alem de mover o jogador, checa se ele encontrou um monstro ou uma parede
    posicaofut = estado["pos_jogador"][:]
    if tecla == "CIMA":
        posicaofut[1] -= 1
    if tecla == "BAIXO":
        posicaofut[1] += 1     
    if tecla == "ESQUERDA":
        posicaofut[0] -= 1
    if tecla == "DIREITA":
        posicaofut[0] += 1

    monstroencontrado = None #essa oarte vai verificar se a pessoa encontrou um monstro
    for monstros in estado["monstros"]:
        if monstros['posicao'] == posicaofut:
            monstroencontrado = monstros
            break
    if monstroencontrado:
        monstromorreu = executa_batalha(estado, monstros)
        if monstromorreu:
            estado["pos_jogador"] = posicaofut
    elif posicaofut not in estado["paredes"]:
        estado["pos_jogador"] = posicaofut
    else:
        estado["mensagem"] = "encontrou obstaculo"
    
def colisoes(estado): #funcao feita para que a funcao def atualiza estado nao fique tao grande, checa se o personagem colidiu com algum objeto do jogo
    for objeto in estado["objetos"]:
        if estado["pos_jogador"] == objeto["posicao"]:
            if objeto["tipo"] == CORACAO and estado["vidas"]<=4:
                estado["vidas"] += 1
                estado['mensagem'] = 'Ganhou uma vida!'
            if objeto["tipo"] == ESPINHO:
                estado["vidas"] -= 1
                if estado["vidas"] <= 0:
                    #jogador morre e vai pra tela de fim de jogo
                    estado["vidas"] = 5
                    estado["tela_atual"] = TELA_GAMEOVER
                else:
                    estado['mensagem'] = 'Perdeu uma vida, cuidado...'
            estado["objetos"].remove(objeto)

def move_gosma(estado, tecla): #essa é a funcao que move os monstros do tipo gosma no jogo
    for monstros in estado["monstros"]:
        posfutura = []
        if monstros["tipo"] == GOSMA:
            if tecla == "CIMA" or tecla == "BAIXO" or tecla == "ESQUERDA" or tecla == "DIREITA":
                x = random.randint(0,1)
                if x == 0:
                    posmonstros2 = monstros["posicao"][0] + random.randint(-1, 1)
                    posfutura.append(posmonstros2)
                    posfutura.append(monstros["posicao"][1])
                else:
                    posmonstros2 = monstros["posicao"][1] + random.randint(-1, 1)
                    posfutura.append(monstros["posicao"][0])
                    posfutura.append(posmonstros2)
                if posfutura not in estado["paredes"]:
                    monstros["posicao"] = posfutura

def move_zumbi(estado, tecla):# move o zumbi
    for monstros in estado["monstros"]:
        posfutura =[]
        if monstros["tipo"] == ZUMBI:
            if tecla == "CIMA" or tecla == "BAIXO" or tecla == "ESQUERDA" or tecla == "DIREITA":
                jogx = estado["pos_jogador"][0]
                jogy = estado["pos_jogador"][1]
                posx = monstros["posicao"][0]
                posy = monstros["posicao"][1]
                #verifica as distancias horizontal e vertical
                diferencax = jogx-posx 
                diferencay = jogy-posy
                distanciax = abs(jogx-posx) 
                distanciay = abs(jogy-posy)
                if abs(jogx-posx) + abs(jogy-posy) <= 5:#zumbi se mexe s e o jogador estiver ate a 5 casas de distancia
                    if distanciax > distanciay:
                        #esta mais longe na horizontal
                        if diferencax > 0:
                            dx = 1 # jogador esta para a direita, monstro anda 1 pra direita
                        else:
                            dx = -1 #jogador esta para a esquerda...
                        dy = 0
                    else: 
                        #esta mais longe na horizontal
                        if diferencay > 0:
                            dy = 1 # jogador esta para baixo
                        else:
                            dy = -1 #monstro vai pra baixo
                        dx = 0
                    posfutura = [posx + dx, posy + dy]
                    if posfutura == estado["pos_jogador"]:
                        executa_batalha(estado, monstros) 
                    elif posfutura not in estado["paredes"]:
                        monstros["posicao"] = posfutura

def move_esqueleto(estado, tecla):# move o esqueleto
    for monstros in estado["monstros"]:
        posfutura =[]
        if monstros["tipo"] == ESQUELETO:
            if tecla == "CIMA" or tecla == "BAIXO" or tecla == "ESQUERDA" or tecla == "DIREITA":
                jogx = estado["pos_jogador"][0]
                jogy = estado["pos_jogador"][1]
                posx = monstros["posicao"][0]
                posy = monstros["posicao"][1]
                #verifica as distancias horizontal e vertical
                diferencax = jogx-posx 
                diferencay = jogy-posy
                distanciax = abs(jogx-posx) 
                distanciay = abs(jogy-posy)
                if distanciax > distanciay:
                    #esta mais longe na horizontal
                    if diferencax > 0:
                        dx = 1 # jogador esta para a direita, monstro anda 1 pra direita
                    else:
                        dx = -1 #jogador esta para a esquerda...
                    dy = 0
                else: 
                    #esta mais longe na horizontal
                    if diferencay > 0:
                        dy = 1 # jogador esta para baixo
                    else:
                        dy = -1 #monstro vai pra baixo
                    dx = 0
                posfutura = [posx + dx, posy + dy]
                if posfutura == estado["pos_jogador"]:
                    executa_batalha(estado, monstros) 
                elif posfutura not in estado["paredes"]:
                    monstros["posicao"] = posfutura

def ganha_xp(estado, quantidade):
    estado["xp"] += quantidade
    while estado["xp"] >= estado["xp_proximo_nivel"]:
        estado["xp"] -= estado["xp_proximo_nivel"]  # Consome o XP do nível atual
        estado["nivel"] += 1                        # Aumenta o nível
        estado["max_vidas"] += 1                    # Aumenta +1 na vida máxima
        estado["vidas"] = estado["max_vidas"]
        estado["xp_proximo_nivel"] = 5 * estado["nivel"]
        estado["mensagem"] = f"SUBIU DE NIVEL E GANHOU UMA VIDA! esta no nivel {estado["nivel"]}!"

def move_dragao(estado, tecla): #essa é a funcao que move os monstros do tipo gosma no jogo
    for monstros in estado["monstros"]:
        posfutura = []
        if monstros["tipo"] == DRAGAO:
            if tecla == "CIMA" or tecla == "BAIXO" or tecla == "ESQUERDA" or tecla == "DIREITA":
                x = random.randint(0,1)
                if x == 0:
                    posmonstros2 = monstros["posicao"][0] + random.randint(-1, 1)
                    posfutura.append(posmonstros2)
                    posfutura.append(monstros["posicao"][1])
                else:
                    posmonstros2 = monstros["posicao"][1] + random.randint(-1, 1)
                    posfutura.append(monstros["posicao"][0])
                    posfutura.append(posmonstros2)
                podemover = True
                for linha in range(monstros["altura"]): #esse negocio checa cada caractere um por vez se ele bate na aprede
                    for coluna in range(monstros["largura"]):
                        bloco = posfutura[0] + coluna, posfutura[1] + linha
                        if bloco in estado["paredes"] or list(bloco) in estado["paredes"]:
                            podemover = False
                            break
                if podemover:
                    monstros["posicao"] = posfutura
    

def atualiza_estado(estado, tecla): # funcao que atualiza o estado do jogo
    estado["jabateu"] = False
    move_gosma(estado, tecla)
    move_zumbi(estado, tecla)
    move_esqueleto(estado,tecla)
    move_dragao(estado,tecla)
    move_jogador(estado, tecla)
    colisoes(estado)
    
    portal = [[1,10],[1,11],[1,9]]
    if estado["pos_jogador"] in portal:
        estado["tela_atual"] = TELA_SALA_SECRETA
    if tecla == 'i':
        estado['tela_atual'] = TELA_INVENTARIO
    # Termina o jogo se o jogador apertar ESC ou 'q'
    elif tecla == motor.ESCAPE or tecla =='q':
        estado['tela_atual'] = SAIR
    
