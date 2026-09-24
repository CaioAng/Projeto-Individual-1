from constantes import *
import motor_grafico as motor

# esse arquivo é o que desenha e "atualiza o estado" da tela de inicio, quando o jogador abre o jogo

def desenha_tela(janela, estado, altura_tela, largura_tela):
    motor.preenche_fundo(janela, PRETO)
    mapa = estado["mapa"]
    deltax = (largura_tela - len(mapa[0]))//2
    deltay = (altura_tela - len(mapa))//2    
    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            motor.desenha_string(janela, j + deltax, i + deltay, '=', CINZA_ESCURO_AZULADO, CINZA_MEDIO_AZULADO)
    motor.desenha_string(janela, len(mapa[0])//2 + deltax - 9, len(mapa)//2 + deltay+ 2, 'Aperte ↑ para jogar', CINZA_MUITO_ESCURO_AZULADO, BRANCO)
    motor.desenha_string(janela, len(mapa[0])//2 + deltax - 8, len(mapa)//2 + deltay - 6, 'PROJETO INDIVIDUAL', CINZA_CLARO_AZULADO, BRANCO)
    motor.desenha_string(janela, len(mapa[0])//2 + deltax - 9, len(mapa)//2 + deltay - 6, ' ', CINZA_CLARO_AZULADO, BRANCO)
    motor.desenha_string(janela, len(mapa[0])//2 + deltax + 10, len(mapa)//2 + deltay - 6, ' ', CINZA_CLARO_AZULADO, BRANCO)
    motor.desenha_string(janela, len(mapa[0])//2 + deltax + -9, len(mapa)//2 + deltay - 5, ' '*20, CINZA_CLARO_AZULADO, BRANCO)
    motor.desenha_string(janela, len(mapa[0])//2 + deltax + -9, len(mapa)//2 + deltay - 7, ' '*20, CINZA_CLARO_AZULADO, BRANCO)
    motor.desenha_string(janela, len(mapa[0])//2 + deltax - 10, len(mapa)//2 + deltay+ 5, 'Aperte ↓ para tutorial', CINZA_MUITO_ESCURO_AZULADO, BRANCO)

def atualiza_estado(estado, tecla_apertada):
    if tecla_apertada == 'CIMA':
        estado['tela_atual'] = TELA_JOGO
    if tecla_apertada == 'BAIXO':
        estado['tela_atual'] = TELA_INSTRUCOES
    elif tecla_apertada in (motor.ESCAPE, 'q'):
        estado['tela_atual'] = SAIR