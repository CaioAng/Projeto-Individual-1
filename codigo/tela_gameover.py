from constantes import *
import motor_grafico as motor

# esse arquivo é o que desenha e "atualiza o estado" da tela de gameover, quando o jogador perde o jogo

def desenha_tela(janela, estado, altura_tela, largura_tela):
    motor.preenche_fundo(janela, PRETO)
    mapa = estado["mapa"]
    deltax = (largura_tela - len(mapa[0]))//2
    deltay = (altura_tela - len(mapa))//2    
    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            motor.desenha_string(janela, j + deltax, i + deltay, '|', CINZA_ESCURO_AZULADO, CINZA_MEDIO_AZULADO)
    motor.desenha_string(janela,  len(mapa[0])//2 + deltax - 5, len(mapa)//2 + deltay - 4, 'VOCE PERDEU', CINZA_CLARO_AZULADO, BRANCO)
    motor.desenha_string(janela, len(mapa[0])//2 + deltax - 10, len(mapa)//2 + deltay, 'Aperte ↑ para renascer', CINZA_CLARO_AZULADO, BRANCO)
    motor.desenha_string(janela, len(mapa[0])//2 + deltax - 8, len(mapa)//2 + deltay + 2, 'Aperte q para sair', CINZA_MEDIO_AZULADO, BRANCO)

def atualiza_estado(estado, tecla_apertada):
    if tecla_apertada == 'CIMA':
        estado['tela_atual'] = TELA_JOGO
    elif tecla_apertada in (motor.ESCAPE, 'q'):
        estado['tela_atual'] = SAIR