import disp
import dados
import time
global selecao

def tela_leitura(sel_elemento, telas, linear_map, analise, simbolo, elemento, vetor_escalar_descontado, off_set, media_R, media_G, media_B, contador, sel_arquivo, sel_amost, flags, regs):
    disp.leitura(linear_map, analise, simbolo, elemento, flags, regs)    
    return 
def tela_servico(sel_elemento, telas, linear_map, analise, simbolo, elemento, vetor_escalar_descontado, off_set, media_R, media_G, media_B, contador, sel_arquivo, sel_amost, flags, regs):
    disp.leitura_report(linear_map,vetor_escalar_descontado, off_set, media_R, media_G, media_B, contador)
    return 
def tela_elemento(sel_elemento, telas, linear_map, analise, simbolo, elemento, vetor_escalar_descontado, off_set, media_R, media_G, media_B, contador, sel_arquivo, sel_amost, flags, regs):
    disp.selecao_elementos(sel_elemento)
    return
def tela_config(sel_elemento, telas, linear_map, analise, simbolo, elemento, vetor_escalar_descontado, off_set, media_R, media_G, media_B, contador, sel_arquivo, sel_amost, flags, regs):
    disp.setup(sel_arquivo, sel_amost)
    return
def null(sel_elemento, telas, linear_map, analise, simbolo, elemento, vetor_escalar_descontado, off_set, media_R, media_G, media_B, contador, sel_arquivo, sel_amost, flags, regs):
    global null
    #tela em branco. para tratamento de telas secundarias de gravação (EEPROM) em arquivo externo para main
    #

def selecao(sel_elemento,telas, linear_map, analise, simbolo, elemento, vetor_escalar_descontado, off_set, media_R, media_G, media_B, contador, sel_arquivo, sel_amost, flags, regs):
    switcher={
            0:tela_leitura,
            1:tela_servico,
            2:tela_elemento,
            3:tela_config,
            4:null
            }
    func=switcher.get(telas)
    return func(sel_elemento, telas, linear_map, analise, simbolo, elemento, vetor_escalar_descontado, off_set, media_R, media_G, media_B, contador, sel_arquivo, sel_amost, flags, regs)
 

