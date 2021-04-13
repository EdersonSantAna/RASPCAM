import cv2
import math
import cpu_status
import disp
import dados
import funcoes
import _thread as thread
import RPi.GPIO as gpio
import time

#frame = np.ones((300, 400, 3)) * 255 #imagem 400x300, com fundo branco e 3 canais para as cores
######################################################################################################
#
#                          CONFIGURAÇOES DO FOTOMETRO POR CAM
#
cap = cv2.VideoCapture(0) #Inicializa a camera
cor = (255, 255, 0) # marca a cor da mira (BGR)
font                   = cv2.FONT_HERSHEY_SIMPLEX
font2                  = cv2.FONT_HERSHEY_COMPLEX_SMALL
coord                  = (311,246) #(x,y) x = horiz , y = vert
coord2                 = (250,300) #(x,y) x = horiz , y = vert
fontScale2             = 1
fontScale              = 1
fontColor              = (255,255,0) #azul (BGR)
lineType2              = 0
lineType               = 1
resultado              = 0
resultado_vetor        = 0
flags                  = 0       # flags de parametros default em Normal Analise
regs                   = 0       # Registro default desligado
janela                 = 5       # janela limite de coleta padrão fator = 5,
contador               = 0
controle_tela          = 0
tempo_salva_imagens    = 0.2     # tempo em segundos para salva e processamento da imagem capturada
amostragem_resultado   = 64      # limite maximo de amostragens de resultados padrão = 64 (mesmo valor para amostragem dos pixel)
amostragem             = 64      # limite maximo de amostragens de pixel  padrão = 64 (valor de amostragem decorrente do passo = 5)
passo                  = 5       # passo para analise da matrix padrão = 5 ( para amostragem = 64)
#off_set                = 1.732   # analise da luz espuria / escuro
entrada_max            = 255     # map valor de entrada (pixel)
entrada_min            = 0       # map valor minimo de entrada 0 à xxx (pixel)
saida_max              = 100     # map valor de saida (escala linear)
saida_min              = 0       # map valor minimo de saida 0 à xxx
start                  = 1       # inicia o processo de THREADS CPU Status no disp. OLED (1 = on / 0 = off)
filtro_debouncing      = 0.05   # tempo (segundos) de debouncing para o filtro de teclas
start_tecla            = 1       # inicia o processo de THREADS teclado.(1 = on / 0 = off)
span_calib             = 100     # ponto de calibração em ppm
tecla_off_set          = 21      # pino BOARD para a tecla zera a leitura no branco
tecla_cal              = 20      # pino BOARD para a tecla calibra um ponto na curva
tecla_selecao          = 18      # pino BOARD para a tecla seleção nos modos pages
tecla_entra            = 16      # pino BOARD para a tecla entra
led_status             = 12      # pino BOARD para o led status
indice_sel             = 0
indice_entra           = 0
controle_gravacao      = 1
analise                = " "
selecao_elemento       = 0  #inicio de uma variavel
cal                    = 0
result_cal             =1
sel_arquivo            = 0
sel_amost              = 0
sel_elemento           = 0
controle               = 0
num                    = 1


##########################################################################################################################

#le parametros gravados em arquivo
sel_arquivo, sel_amost, elemento, simbolo = dados.eprom_le() 

def cpu_processo(start): #executa uma Thread
    while (start):
        cpu_status.processo()
 
def interrupt_tecla_zero(filtro_debouncing):
    global cal
    if gpio.event_detected(tecla_off_set):
        time.sleep(filtro_debouncing) # filtro de boucing
        if (not gpio.event_detected(tecla_off_set)):
            time.sleep(filtro_debouncing) # filtro de boucing
            print("Calibrando o ZERO, aguarde estabilizando...")
            gpio.output(led_status, gpio.HIGH)
            cal = vetor_escalar_descontado
            time.sleep (2) # tempo para calibração aprox. 2 segundos
    return cal

def interrupt_tecla_calib(filtro_debouncing, span_calib, linear_map ):
    global result_cal

    if gpio.event_detected(tecla_cal):
        time.sleep(filtro_debouncing) # filtro de boucing
        if (not gpio.event_detected(tecla_cal)):
            print("Calibrando o SPAN, aguarde estabilizando...")
            gpio.output(led_status, gpio.HIGH)
            result_cal = (span_calib / linear_map)
            time.sleep (2) # tempo para calibração aprox. 2 segundos
    return result_cal

def interrupt_tecla_selecao(filtro_debouncing):
    global indice_sel
    if gpio.event_detected(tecla_selecao):
        time.sleep(filtro_debouncing) # filtro de boucing
        if (not gpio.event_detected(tecla_selecao)):
            time.sleep(filtro_debouncing) # filtro de boucing
            indice_sel = indice_sel + 1
            if (indice_sel == 4): indice_sel = 0
            gpio.output(led_status, gpio.HIGH)
    return indice_sel

def interrupt_tecla_entra(filtro_debouncing):
    global indice_entra, controle
    if gpio.event_detected(tecla_entra):
        time.sleep(filtro_debouncing) # filtro de boucing
        if (not gpio.event_detected(tecla_entra)):
            time.sleep(filtro_debouncing) # filtro de boucing
            indice_entra = indice_entra + 1
            controle = 1
            if (indice_entra > 4): indice_entra = 0
            gpio.output(led_status, gpio.HIGH)
    return indice_entra, controle

def selecao_opcoes(controle_tela, selecao_elemento):
    global sel_arquivo, sel_amost, elemento, simbolo, sel_elemento
    
    if((controle_tela == 2) and (selecao_elemento == 0)):
        sel_elemento = 0
        elemento, simbolo  = disp.selecao_elementos(0)

    if((controle_tela == 2) and (selecao_elemento == 1)):
        sel_elemento = 1
        elemento, simbolo  = disp.selecao_elementos(1)

    if((controle_tela == 2) and (selecao_elemento == 2)):
        sel_elemento = 2
        elemento, simbolo  = disp.selecao_elementos(2)
        
    if((controle_tela == 2) and (selecao_elemento == 3)):
        sel_elemento = 3
        elemento, simbolo  = disp.selecao_elementos(3)
        
    if((controle_tela == 3) and (selecao_elemento == 0)):
        sel_arquivo = 0
                
    if((controle_tela == 3) and (selecao_elemento == 1)):
        sel_arquivo = 1
        sel_amost = 0
        
    if((controle_tela == 3) and (selecao_elemento == 2)):
        sel_arquivo = 1
        sel_amost = 1
        
    if((controle_tela == 3) and (selecao_elemento == 3)):
        sel_arquivo = 1
        sel_amost = 0
   
    return sel_arquivo, sel_amost, elemento, simbolo, sel_elemento     
  
def leitura():

    scan_x                 = 301 # coord para varredura (scan) da imagem
    scan_y                 = 220 # coord para varredura (scan) da imagem
    limite_x               = 339 # coord para varredura (scan) da imagem
    limite_y               = 258 # coord para varredura (scan) da imagem
    medida_R               = 0
    medida_G               = 0
    medida_B               = 0
    debbug_passo = 0
    for y in range(scan_y, limite_y, passo): #varredura em Y (vertical) 38 passos

        for x in range (scan_x, limite_x, passo): #varredura em X (horizontal) 38 passos
            b,g,r = (captura[y, x]) #leitura nas coord. Y,X de uma matrix da imagem
            medida_R = (medida_R + r) #somatorias da varredura de R
            medida_G = (medida_G + g) #somatorias da varredura de G
            medida_B = (medida_B + b) #somatorias da varredura de B
    #calcula as medias dos pontos da areas arredondando 2 casas decimais
    media_R = round (medida_R / amostragem , 2)
    media_G = round (medida_G / amostragem , 2)
    media_B = round (medida_B / amostragem , 2)
    # monta um vetor escalar para RGB
    vetor_escalar = round (math.sqrt ((media_R ** 2) + (media_G ** 2) + (media_B ** 2)), 3)
    # desconta o zero (Off-Set)
    vetor_escalar_descontado = round ((vetor_escalar - off_set) , 1)
    if (vetor_escalar_descontado < 0):
        vetor_escalar_descontado = round (0 , 1)
    #retorna os resultados da analises
    return vetor_escalar_descontado, media_R, media_G, media_B

# Configurando PIN como INPUT e modo pull-donw interno
gpio.setmode(gpio.BCM)

# Adicionando um evento as teclas de off-set na mudança RISING 0V[LOW] - > 3.3V[HIGH]
gpio.setup(tecla_off_set, gpio.IN, pull_up_down = gpio.PUD_UP)
gpio.setup(tecla_cal, gpio.IN, pull_up_down = gpio.PUD_UP)
gpio.setup(tecla_selecao, gpio.IN, pull_up_down = gpio.PUD_UP)
gpio.setup(tecla_entra, gpio.IN, pull_up_down = gpio.PUD_UP)
gpio.setup(led_status, gpio.OUT) # led externo

# interrupção para teclas
gpio.add_event_detect(tecla_off_set, gpio.FALLING)
gpio.add_event_detect(tecla_cal, gpio.FALLING)
gpio.add_event_detect(tecla_selecao, gpio.FALLING)
gpio.add_event_detect(tecla_entra, gpio.FALLING)

#multiprocessamento. chamada de uma Thread
thread.start_new_thread(cpu_processo, (start,)) # servico processamento para status CPU

#porta conf. como saida para led estabilização
gpio.output(led_status, gpio.LOW) #high para alto e low para baixo

while(1):

    gpio.output(led_status, gpio.LOW)
    off_set =  interrupt_tecla_zero(filtro_debouncing) #interrupção para a tecla calibra zero. retorna um int e passa um parametro para deboucing em segundos
    controle_tela, controle = interrupt_tecla_entra(filtro_debouncing)
    selecao_elemento = interrupt_tecla_selecao (filtro_debouncing)

    _, frame = cap.read() # faz captura de imagens (video) em tempo real
    cv2.imwrite("foton_process.jpg",frame) # salva a imagem do objeto da analise
    cv2.putText(frame,'x', coord, font, fontScale, fontColor, lineType) #desenha a mira de analise
    cv2.rectangle(frame, (301, 220), (339, 258), cor) #moldura limitadora de analises
    cv2.putText(frame,analise, coord2, font2, fontScale2, fontColor, lineType2)
    #cv2.putText(frame,'ANALISES FOTOMETRICA POR CAM CCD', (0,30), font, 1, fontColor, 1)
    cv2.imshow('resultado',frame) #abre uma janela com a imagem para analise da foto
    time.sleep(tempo_salva_imagens) # delay para salva a foto para analise
    captura = cv2.imread('foton_process.jpg', 1) # abre a fotografia capturada para analises. 1 para cor RGB
    vetor_escalar_descontado, media_R, media_G, media_B = leitura() #retorno da função com dados numericos
    resultado = resultado + vetor_escalar_descontado # somatoria dos valores lidos
    contador += 1 # contador de ciclo
    #calcula a media e reseta as variaveis
    if (contador == amostragem_resultado):
        resultado_vetor = round ((resultado / amostragem_resultado),1)
        contador = 0
        resultado = 0
    #subtraindo os dois resultados para achar valores para janela de estabilização
    estab_janela = (round ((resultado_vetor - vetor_escalar_descontado), 1) )
    #aplicando o map() para linearização de escala
    linear_map = round ((((resultado_vetor - entrada_min) * (saida_max - saida_min)) / ((entrada_max - entrada_min) + saida_min)), 1)
    # calibra o 100ppm (SPAN )
    calib =  interrupt_tecla_calib(filtro_debouncing, span_calib, linear_map)
    #montando uma janela de estabilidade
    linear_map = round ((linear_map * calib), 1)
    if (estab_janela < 0): estab_janela = (estab_janela * -1)
    if (estab_janela <=  janela):
        analise = "Analisando"
  
          #escreve (exporta) arquivo .TXT e .CVS (excel)
        if(controle_tela == 0) or (controle_tela == 1): #so executa o registro quando estiver na tela de leituras
            if(sel_arquivo == 1) and (sel_amost == 0): #executa comando de escrita em arquivo por tempo
                if(num == 1):dados.cria_page_export_txt() #imprime uma vez o cabeçario
                time.sleep(1) #intervalo de escrita em 1 segundos
                dados.exporta_dados_txt(num, linear_map, "ppm", simbolo, elemento) #exporta arquivo no formato texto  (.TXT)
                dados.exporta_dados_cvs(num, linear_map, simbolo, elemento)# exporta arquivo no formato para excell (.CVS)
                num = num+1
                regs = regs+1
                flags = 1
                
            if(sel_arquivo == 1) and (sel_amost == 1):#executa comando de escrita em arquivo por estabilização
                flags = 2
                if(num == 1):dados.cria_page_export_txt() #imprime uma vez o cabeçario
                if(num == 1) or (gpio.event_detected(tecla_selecao)):
                    dados.exporta_dados_txt(num, linear_map, "ppm", simbolo, elemento) #exporta arquivo no formato texto  (.TXT)
                    dados.exporta_dados_cvs(num, linear_map, simbolo, elemento)# exporta arquivo no formato para excell (.CVS)
                    num = num+1
                    regs = regs+1
                            
    else:
        analise = "Estabilizando..."
    abs (linear_map) # não permite valor negativo de concentração
     
    # faz a seleção dos menus (pesquisar maquina de estado para python)
    sel_arquivo, sel_amost, elemento, simbolo, sel_elemento = selecao_opcoes(controle_tela, selecao_elemento)
    
    # executa as operacoes de telas para navegação semelhante a (maquina de estado)
    funcoes.selecao(sel_elemento,controle_tela, linear_map, analise, simbolo, elemento, vetor_escalar_descontado, off_set, media_R, media_G, media_B, contador, sel_arquivo, sel_amost, flags, regs) 
    
    #acessa a tela de apresentação pela tecla sel
    if(controle_tela == 1) and (gpio.event_detected(tecla_selecao)):disp.about()
    
    if (controle_tela == 0):
        controle_gravacao = 1 #controla o acesso a gravação.
        
        
    if (controle_gravacao == 1) and (controle_tela == 4): #entra na função de gravação de parametros
        disp.salvar()
    
        if (controle == 1) and (gpio.event_detected(tecla_selecao)): #escapa sem salvar
            disp.cancel_dados()
            print("Parametros NÂO salvo!")
            controle = 0
            controle_gravacao = 0
            num = 1
            regs = 0
            flags = 0
            sel_arquivo, sel_amost, elemento, simbolo = dados.eprom_le() #le parametros gravados em arquivo

            
        if (controle == 1) and (gpio.event_detected(tecla_entra)): #salva na EEPROM
            dados.eprom_grava(sel_arquivo, sel_amost, elemento, simbolo)
            print("Parametros de configuração SALVOS com sucesso!")
            disp.dados_salvado()
            controle = 0
            controle_gravacao = 0
            num = 1
            regs = 0
            flags = 0
            sel_arquivo, sel_amost, elemento, simbolo = dados.eprom_le() #le parametros gravados em arquivo
        
    print ("Leitura:",linear_map,"ppm",simbolo)
        
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

gpio.cleanup()
cap.release()
cv2.destroyAllWindows()