from random import randint

from constantes import *  # Você pode usar as constantes definidas em constantes.py, se achar útil
                          # Por exemplo, usar a constante CORACAO é o mesmo que colocar a string '❤'
                          # diretamente no código


def gera_posicao_desocupada(posicoes_ocupadas, largura_mapa, altura_mapa):
    while True:
        x = randint(1, largura_mapa - 2)
        y = randint(1, altura_mapa - 2)
        posicao = [x, y]
        if posicao not in posicoes_ocupadas:
            posicoes_ocupadas.append(posicao)
            return posicao

def gera_objetos(quantidade, tipo, cor, largura_mapa, altura_mapa, posicoes_ocupadas):
    objetos = []

    for i in range(quantidade):
        posicao = gera_posicao_desocupada(posicoes_ocupadas, largura_mapa, altura_mapa)
        objetos.append({
            'tipo': tipo,
            'posicao': posicao,
            'cor': cor,
        })

    return objetos

def gera_monstros(quantidade, tipo, cor, vida, probatk, xp, largura, altura, largura_mapa, altura_mapa, posicoes_ocupadas): #essa funcao é uma replica da gera objetos com informacoes a mais, vida e probabilidade de ataque
    monstros = []

    for i in range(quantidade):
        posicao = gera_posicao_desocupada(posicoes_ocupadas, largura_mapa, altura_mapa)
        monstros.append({
            'tipo': tipo,
            'posicao': posicao,
            'cor': cor,
            "vida": vida,
            "probatk": probatk,
            "xp": xp,
            "largura": largura,
            "altura": altura
        })

    return monstros

def gera_paredes(): #essa funcao usa o arquivo txt para criar uma lista com paredes
    with open("mapa.txt", "r") as arquivo:
        mapa = arquivo.read()
    paredes = []
    mapa_linha = mapa.split()
    for y in range(len(mapa_linha)):
        linha = mapa_linha[y]
        for x in range(len(linha)):
            pixel = linha[x]
            if pixel == "X":
                paredes.append([x, y])
    return paredes

def gera_paredessecreta(): #essa funcao é uma replica da acima que cria paredes para a sala secreta
    with open("sala_secreta.txt", "r") as arquivo:
        mapa = arquivo.read()
    paredes = []
    mapa_linha = mapa.split()
    for y in range(len(mapa_linha)):
        linha = mapa_linha[y]
        for x in range(len(linha)):
            pixel = linha[x]
            if pixel == "X":
                paredes.append([x, y])
    return paredes

def inicializa_estado():
    mapa = [
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,    
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
    ]
    
    largura_mapa = len(mapa[0])
    altura_mapa = len(mapa)

    
    # Você pode colocar o jogador em outro lugar, se preferir
    pos_jogador = [largura_mapa//2, altura_mapa//2]  # Meio do mapa
    
    # Cria outros objetos do mapa
    posicoes_ocupadas = [pos_jogador]
    objetos = []
    objetos += gera_objetos(11, CORACAO, VERMELHO, largura_mapa, altura_mapa, posicoes_ocupadas)
    objetos += gera_objetos(12, ESPINHO, MARROM_ESCURO, largura_mapa, altura_mapa, posicoes_ocupadas)

    dragao = gera_monstros(1, DRAGAO, VERMELHO, 20, 0.6, 30, 8, 3, largura_mapa, altura_mapa, posicoes_ocupadas)
    dragao[0]["posicao"] = [26, 4]

    monstros = []
    monstros += gera_monstros(12, GOSMA, VERDE_CLARO, 2, 0.1, 1, 1, 1, largura_mapa, altura_mapa, posicoes_ocupadas)
    monstros += gera_monstros(8, ZUMBI, VERDE_ESCURO, 5, 0.4, 5, 1, 1, largura_mapa, altura_mapa, posicoes_ocupadas)
    monstros += gera_monstros(6, ESQUELETO, BRANCO, 3, 0.2, 3, 1, 1, largura_mapa, altura_mapa, posicoes_ocupadas)
    monstros += dragao
    
    return {
        'tela_atual': TELA_INICIO,
        'pos_jogador': pos_jogador,
        'pos_jogadorsecreta': [2,5],
        'vidas': 5,  # Quantidade atual de vidas do jogador - ele pode perder vidas ao colidir com espinhos ou ganhar vidas ao pegar corações
        'max_vidas': 5,  # Quantidade máxima de vidas que o jogador pode ter - o valor da chave 'vidas' nunca pode ser maior que o valor da chave 'max_vidas'
        'objetos': objetos,
        'mapa': mapa,
        'paredes': gera_paredes(),
        "paredessecreta": gera_paredessecreta(),
        'mensagem': '',  # Use esta mensagem para mostrar mensagens ao jogador, como "Você perdeu uma vida" ou "Você ganhou uma vida"
        "monstros": monstros,
        "jabateu": False,
        "xp": 0,
        "nivel": 1,
        "xp_proximo_nivel": 5
    }
