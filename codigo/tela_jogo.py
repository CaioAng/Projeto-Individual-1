from constantes import *  # Você pode usar as constantes definidas em constantes.py, se achar útil
                          # Por exemplo, usar a constante CORACAO é o mesmo que colocar a string '❤'
                          # diretamente no código
import motor_grafico as motor  # Utilize as funções do arquivo motor_grafico.py para desenhar na tela
                               # Por exemplo: motor.preenche_fundo(janela, [0, 0, 0]) preenche o fundo de preto


def desenha_tela(janela, estado, altura_tela, largura_tela):
    motor.preenche_fundo(janela, PRETO)
    mapa = estado["mapa"]
    deltax = (largura_tela - len(mapa[0]))//2
    deltay = (altura_tela - len(mapa))//2    
    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            if (i + j) % 2 == 0:
                motor.desenha_string(janela, j + deltax, i + deltay, '▯', CINZA_MEDIO_AZULADO, CINZA_ESCURO_AZULADO)
            else:
                motor.desenha_string(janela, j + deltax, i + deltay, '▯', CINZA_CLARO_AZULADO, CINZA_ESCURO_AZULADO)
    motor.desenha_string(janela, estado["pos_jogador"][0] + deltax, estado["pos_jogador"][1]+ deltay, '𓁆', CINZA_ESCURO_AZULADO, BRANCO)
    for objeto in estado["objetos"]:
        motor.desenha_string(janela, objeto["posicao"][0] + deltax, objeto["posicao"][1]+ deltay, objeto["tipo"], CINZA_ESCURO_AZULADO, objeto["cor"])  
    motor.desenha_string(janela, 0+ deltax, deltay-1, estado["vidas"]*'❤︎ ', PRETO, VERMELHO)
    motor.desenha_string(janela, 0+ deltax, len(mapa) + deltay + 1, estado["mensagem"], PRETO, BRANCO)


def atualiza_estado(estado, tecla):
    if tecla == "CIMA":
        estado["pos_jogador"][1] -= 1
    if tecla == "BAIXO":
        estado["pos_jogador"][1] += 1
    if tecla == "ESQUERDA":
        estado["pos_jogador"][1] -= 1
    if tecla == "DIREITA":
        estado["pos_jogador"][1] += 1
    
    # Mude o valor da chave 'tela_atual' para mudar de tela
    
    # Começamos apagando a mensagem anterior, pois ela já foi mostrada no frame anterior
    estado['mensagem'] = ''

    # Escreva seu código para atualizar o dicionário "estado" com base na tecla apertada pelo jogador aqui
    # APAGUE ESTA LINHA E ESCREVA SEU CÓDIGO AQUI

    # Ao apertar a tecla 'i', o jogador deve ver o inventário
    if tecla == 'i':
        estado['tela_atual'] = TELA_INVENTARIO
    # Termina o jogo se o jogador apertar ESC ou 'q'
    elif tecla == motor.ESCAPE or tecla =='q':
        estado['tela_atual'] = SAIR