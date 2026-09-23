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

def gera_monstros(quantidade, tipo, cor, vida, probatk, largura_mapa, altura_mapa, posicoes_ocupadas):
    monstros = []

    for i in range(quantidade):
        posicao = gera_posicao_desocupada(posicoes_ocupadas, largura_mapa, altura_mapa)
        monstros.append({
            'tipo': tipo,
            'posicao': posicao,
            'cor': cor,
            "vida": vida,
            "probatk": probatk
        })

    return monstros

def gera_paredes():
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

def gera_paredessecreta():
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
    objetos += gera_objetos(8, CORACAO, VERMELHO, largura_mapa, altura_mapa, posicoes_ocupadas)
    objetos += gera_objetos(6, ESPINHO, MARROM_ESCURO, largura_mapa, altura_mapa, posicoes_ocupadas)

    monstros = []
    monstros += gera_monstros(6, GOSMA, VERDE_CLARO, 2, 0.2, largura_mapa, altura_mapa, posicoes_ocupadas)
    
    return {
        'tela_atual': TELA_SALA_SECRETA,
        'pos_jogador': pos_jogador,
        'vidas': 5,  # Quantidade atual de vidas do jogador - ele pode perder vidas ao colidir com espinhos ou ganhar vidas ao pegar corações
        'max_vidas': 5,  # Quantidade máxima de vidas que o jogador pode ter - o valor da chave 'vidas' nunca pode ser maior que o valor da chave 'max_vidas'
        'objetos': objetos,
        'mapa': mapa,
        'paredes': gera_paredes(),
        "paredessecreta": gera_paredessecreta(),
        'mensagem': '',  # Use esta mensagem para mostrar mensagens ao jogador, como "Você perdeu uma vida" ou "Você ganhou uma vida"
        "monstros": monstros,
    }
