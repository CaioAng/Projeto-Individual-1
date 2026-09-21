from constantes import *  # Você pode usar as constantes definidas em constantes.py, se achar útil
                          # Por exemplo, usar a constante CORACAO é o mesmo que colocar a string '❤'
                          # diretamente no código
import motor_grafico as motor  # Utilize as funções do arquivo motor_grafico.py para desenhar na tela
                               # Por exemplo: motor.preenche_fundo(janela, [0, 0, 0]) preenche o fundo de preto


def desenha_tela(janela, estado, altura_tela, largura_tela):
    motor.preenche_fundo(janela, PRETO)
    deltax = 15
    deltay = 15

    mapa = estado["mapa"]
    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            if (i + j) % 2 == 0:
                motor.desenha_string(janela, j, i, '▯', CINZA_MEDIO_AZULADO, CINZA_ESCURO_AZULADO)
            else:
                motor.desenha_string(janela, j, i, '▯', CINZA_CLARO_AZULADO, CINZA_ESCURO_AZULADO)
    motor.desenha_string(janela, estado["pos_jogador"][0], estado["pos_jogador"][1], '@', VERDE_CLARO, PRETO)
    for objeto in estado["objetos"]:
        motor.desenha_string(janela, objeto["posicao"][0], objeto["posicao"][1], objeto["tipo"], VERDE_CLARO, objeto["cor"])  
    
    motor.desenha_string(janela, 1, 1, estado["vidas"]*'❤︎ ', MARROM_ESCURO, VERMELHO)

def atualiza_estado(estado, tecla):
    # O seu código deve atualizar o dicionário "estado" com base na tecla apertada pelo jogador
    # Por exemplo, se o jogador apertar a seta para a esquerda (o valor da variável será "ESQUERDA"), 
    # o seu código deve atualizar o dicionário estado['pos_jogador'][0] -= 1

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