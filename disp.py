import time
import subprocess
import digitalio
import board
import dados
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import adafruit_rgb_display.st7735 as st7735 

import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI



# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

WIDTH = 128
HEIGHT = 160
a=0
 
spi = board.SPI()

disp = st7735.ST7735R(spi, rotation=90,                           # 1.8" ST7735R

    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height

image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)


 
status_font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
font1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
unidade = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
lcd = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
font_init = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 19)

def intro():
    draw.rectangle((0, 0, width, height), outline=(60,0,0), fill=(60,0,0)) # LIMPA TELA (IMPRIME PRETO)
    draw.text((0,1), ("Firmware     ver 1.0.16"), font=font, fill="#FFAC00")
    draw.text((20,30), ("FOTOMETRO"), font=font_init, fill="#00CF00")
    draw.text((70,50), ("DE"), font=font_init, fill="#00CF00")
    draw.text((45,70), ("CHAMA"), font=font_init, fill="#00CF00")
    for y in range(0, 159, 10):
        draw.text((y,100), ("_"), font=font_init, fill="#00ACAA")
        time.sleep(.1)
        disp.image(image)
intro()        


def selecao_elementos(setagem):
    global simbolo
    global elemento
    
    draw.rectangle((0, 0, width, height), outline=(60,0,0), fill=(60,0,0)) # LIMPA TELA (IMPRIME PRETO)
    draw.rectangle((0,0,159,127), outline=(255,255,255), fill=(60, 0, 0))
    draw.rectangle((0,0,159,20), outline=(255,255,255), fill=(60, 0, 0))
    draw.rectangle((0,107,159,107), outline=(255,255,255), fill=(60, 0, 0))
    draw.text((2,1),   ("SELEÇÃO DE ELEMENTO"), font=font1, fill="#00FFFF")
    draw.text((2,108), ("Escolha opções acima"), font=font1, fill="#00FFFF")
    draw.text((45,25), ("    [Na] Sódio"), font=font1, fill="#707070")
    draw.text((45,45), ("    [Ca] Cálcio"), font=font1, fill="#707070")
    draw.text((45,65), ("    [K]  Potássio"), font=font1, fill="#707070")
    draw.text((45,85), ("    [Li] Lítio"), font=font1, fill="#707070")
  #  ciclo_menu = ciclo_menu + 1
    if (setagem == 0):
        draw.text((45,25), ("->[Na] Sódio"), font=font1, fill="#0000FF")
        elemento = "Sódio"
        simbolo = "Na"
    if (setagem == 1):
        draw.text((45,45), ("->[Ca] Cálcio"), font=font1, fill="#0000FF")
        elemento = "Cálcio"
        simbolo = "Ca"
    if (setagem == 2):
        draw.text((45,65), ("->[K]  Potássio"), font=font1, fill="#0000FF")
        elemento = "Potássio"
        simbolo = "K"
    if (setagem == 3):
        draw.text((45,85), ("->[Li] Lítio"), font=font1, fill="#0000FF")
        elemento = "Lítio"
        simbolo = "Li"
        
    disp.image(image)
    return elemento, simbolo


def about():
    draw.rectangle((0, 0, 159, 127), outline=(255,255,255), fill=(255,255,255)) # LIMPA TELA (IMPRIME PRETO)
    draw.text((2,1), ("V1.0.16"), font=font1, fill="#f00000")
    draw.text((2,30), ("Sobre!"), font=unidade, fill="#f00000")
    draw.text((2,55), ("Fotometro de Emissão"), font=font1, fill="#f00000")
    draw.text((2,68), ("por imagem é um"), font=font1, fill="#f00000")
    draw.text((2,81), ("projeto desenvolvido"), font=font1, fill="#f00000")
    draw.text((2,94), ("para pós graduação"), font=font1, fill="#f00000")
    draw.text((2,107), ("SENAI Sist. Embarcados."), font=font1, fill="#f00000")
    disp.image(image)
    eletron = Image.open("eletron.jpg")
    disp.image(eletron)
    time.sleep(10)
    return 

 
def leitura(valor, status, elemento, desc_elemento, flags, regs):

    #O esquema de cor é invertido tipo BGR e não RGB 
    draw.rectangle((0, 0, width, height), outline=0, fill=0) # LIMPA TELA (IMPRIME PRETO)
    # desenha uma caixa para o texto corpo de leitura
    draw.rectangle((0,26,159,100), outline=(0,255,255), fill=(50, 0, 0))
    # desenha uma caixa para o texto rodape
    draw.rectangle((0,107,159,127), outline=(0,255,255), fill=(80, 0, 0)) 
    #imprime os valores no LCD
    draw.text((0,50), ("%.1f"% valor), font=lcd, fill="#FFFF00")
    #imprime a unidade 
    draw.text((130,30), (elemento), font=unidade, fill="#FFFF00")
    #tratamento de deslocamento da unidade com as casas decimais
    if (valor < 0):
        draw.text((90,70), ("ppm"), font=unidade, fill="#FFFF00")
    if (valor >= 0 and valor < 10):
        draw.text((65,70), ("ppm"), font=unidade, fill="#FFFF00")
    if (valor >= 10 and valor < 100):
        draw.text((90,70), ("ppm"), font=unidade, fill="#FFFF00")
    if (valor >= 100):
        draw.text((112,70), ("ppm"), font=unidade, fill="#FFFF00")
    #imprime o status (RODAPE)
    draw.text((3,110), (status), font=status_font, fill="#FFFFFF")
    #imprime o info (CABECARIO)
    draw.text((3,28), (desc_elemento), font=status_font, fill="#00FF00")
    if (flags == 0):
        draw.text((3,3), ("Normal Analise [SR]"), font=status_font, fill="#EE5000")
    if (flags == 1):
        draw.text((3,3), ("Reg:       [AUTO=1s]"), font=status_font, fill="#EE5000")
    if (flags == 2):
        draw.text((3,3), ("Reg:            [ESTAB]"), font=status_font, fill="#EE5000")
    if (regs >= 1):
        draw.text((40,3), ("%.0f"% regs), font=status_font, fill="#00CCCC")
   
    disp.image(image)



    
def leitura_report(valor, vetor, valor_off_set , pixel_R, pixel_G, pixel_B, varredura):
    #convertendo o RGB em inteiros para usar na caixa de cor (FILL (x,x,x))
    R = int (pixel_R)
    G = int (pixel_G)
    B = int (pixel_B)
    
    #O esquema de cor é invertido tipo BGR e não RGB 
    draw.rectangle((0, 0, width, height), outline=0, fill=0) # LIMPA TELA (IMPRIME PRETO)
    # desenha uma caixa para o texto corpo de leitura
    draw.rectangle((0,0,159,127), outline=(255,255,255), fill=(0, 0, 0))
    draw.rectangle((5,25,154,122), outline=(255,255,255), fill=(80, 0, 0))
    draw.rectangle((0,0,159,20), outline=(255,255,255), fill=(0, 0, 0))
    draw.rectangle((120,80,150,100), outline=(255,255,255), fill=(B, G, R))
    #imprime 2x (efeito BOLD (negrito)) no CABECARIO
    draw.text((7,2), ("TELA DE SERVIÇOS"), font=status_font, fill="#FFFF00")
    draw.text((7,2), ("TELA DE SERVIÇOS"), font=status_font, fill="#FFFF00")
    #imprime 2x (efeito BOLD (negrito)) nos textos 
    draw.text((8,28), ("Leitura ppm:"), font=font, fill="#00FFFF")
    draw.text((8,43), ("Vetor Escalar:"), font=font, fill="#00FFFF")
    draw.text((8,58), ("Off-Set:"), font=font, fill="#00FFFF")
    draw.text((8,73), ("Pixel R:"), font=font, fill="#00FFFF")
    draw.text((8,88), ("Pixel G:"), font=font, fill="#00FFFF")
    draw.text((8,103),("Pixel B:"), font=font, fill="#00FFFF")
    draw.text((8,28), ("Leitura ppm:"), font=font, fill="#00FFFF")
    draw.text((8,43), ("Vetor Escalar:"), font=font, fill="#00FFFF")
    draw.text((8,58), ("Off-Set:"), font=font, fill="#00FFFF")
    draw.text((8,73), ("Pixel R:"), font=font, fill="#00FFFF")
    draw.text((8,88), ("Pixel G:"), font=font, fill="#00FFFF")
    draw.text((8,103), ("Pixel B:"), font=font, fill="#00FFFF")
    draw.text((93,102), ("var:"), font=font, fill="#00FFFF")
    draw.text((93,102), ("var:"), font=font, fill="#00FFFF")
    draw.text((120,64), ("Cor"), font=font, fill="#00FFFF")
    #imprime os  valores no LCD8
    draw.text((110,28), ("%.1f"% valor), font=font, fill="#FFFFFF")
    draw.text((110,43), ("%.1f"% vetor), font=font, fill="#FFFFFF")
    draw.text((60,58), ("%.1f"% valor_off_set), font=font, fill="#FFFFFF")
    draw.text((60,73), ("%.0f"% pixel_R), font=font, fill="#0000FF")
    draw.text((60,88), ("%.0f"% pixel_G), font=font, fill="#00FF00")
    draw.text((60,103), ("%.0f"% pixel_B), font=font, fill="#FF6600")
    draw.text((120,102), ("%.0f"% varredura), font=font, fill="#00FFFF")
 
    disp.image(image)

def setup (sel_arquivo, sel_amost):
    #O esquema de cor é invertido tipo BGR e não RGB 
    draw.rectangle((0, 0, width, height), outline=0, fill=0) # LIMPA TELA (IMPRIME PRETO)
    # desenha uma caixa para o texto corpo de leitura
    draw.rectangle((0,0,159,127), outline=(255,255,255), fill=(0, 0, 0))
#    draw.rectangle((5,25,154,122), outline=(255,255,255), fill=(80, 0, 0))
    draw.rectangle((0,0,159,20), outline=(255,255,255), fill=(0, 0, 0))
    #imprime 2x (efeito BOLD (negrito)) no CABECARIO
    draw.text((20,2), ("CONFIGURAÇÃO"), font=status_font, fill="#FFFF00")
    draw.text((8,28), ("Exportar dados:"), font=font, fill="#00FFFF")
    draw.text((25,43), (" Habilitar escrita"), font=font, fill="#707070")
    draw.text((25,58), (" Desativar"), font=font, fill="#707070")
    draw.text((8,73), ("Modo de escrita:"), font=font, fill="#00FFFF")
    draw.text((25,88), (" ao comando (KEY)"), font=font, fill="#707070")
    draw.text((25,103), (" por estabilização"), font=font, fill="#707070")
        
    if (sel_arquivo == 1):
        draw.text((8,43), ("-> Habilitar escrita"), font=font, fill="#0000FF")
    if (sel_arquivo == 0):
        draw.text((8,58), ("-> Desativar"), font=font, fill="#0000FF")
    if (sel_amost == 1):
        draw.text((8,88), ("-> ao comando (KEY)"), font=font, fill="#0000FF")
    if (sel_amost == 0):
        draw.text((8,103), ("-> por estabilização"), font=font, fill="#0000FF")
       
    disp.image(image)
    return

def salvar ():
    #O esquema de cor é invertido tipo BGR e não RGB 
    draw.rectangle((0, 0, width, height), outline=0, fill=0) # LIMPA TELA (IMPRIME PRETO)
    # desenha uma caixa para o texto corpo de leitura
    draw.rectangle((0,0,159,127), outline=(120,120,120), fill=(0, 0, 0))
#    draw.rectangle((5,25,154,122), outline=(255,255,255), fill=(80, 0, 0))
    draw.rectangle((0,0,159,20), outline=(120,120,120), fill=(0, 0, 0))
    #imprime 2x (efeito BOLD (negrito)) no CABECARIO
    draw.text((20,2), ("CONFIGURAÇÃO"), font=status_font, fill="#707070")
    draw.text((8,28), ("Exportar dados:"), font=font, fill="#707070")
    draw.text((25,43), (" Habilitar escrita"), font=font, fill="#707070")
    draw.text((25,58), (" Desativar"), font=font, fill="#707070")
    draw.text((8,73), ("Modo de escrita:"), font=font, fill="#707070")
    draw.text((25,88), (" ao comando (KEY)"), font=font, fill="#707070")
    draw.text((25,103), (" por estabilização"), font=font, fill="#707070")
    draw.rectangle((25,45,135,100), outline=(255,255,255), fill=(100, 0, 0))
    draw.text((31,52), ("ENT="), font=status_font, fill="#00FFFF")
    draw.text((73,52), ("SALVAR"), font=status_font, fill="#0000FF")
    draw.text((31,72), ("SEL= SAIR"), font=status_font, fill="#00FFFF")
         
    disp.image(image)

    return
def dados_salvado ():
    #O esquema de cor é invertido tipo BGR e não RGB 
    draw.rectangle((0, 0, width, height), outline=0, fill=0) # LIMPA TELA (IMPRIME PRETO)
    # desenha uma caixa para o texto corpo de leitura
    draw.rectangle((0,0,159,127), outline=(120,120,120), fill=(0, 0, 0))
#    draw.rectangle((5,25,154,122), outline=(255,255,255), fill=(80, 0, 0))
    draw.rectangle((0,0,159,20), outline=(120,120,120), fill=(0, 0, 0))
    #imprime 2x (efeito BOLD (negrito)) no CABECARIO
    draw.text((20,2), ("CONFIGURAÇÃO"), font=status_font, fill="#707070")
    draw.text((8,28), ("Exportar dados:"), font=font, fill="#707070")
    draw.text((25,43), (" Habilitar escrita"), font=font, fill="#707070")
    draw.text((25,58), (" Desativar"), font=font, fill="#707070")
    draw.text((8,73), ("Modo de escrita:"), font=font, fill="#707070")
    draw.text((25,88), (" ao comando (KEY)"), font=font, fill="#707070")
    draw.text((25,103), (" por estabilização"), font=font, fill="#707070")
    draw.rectangle((25,45,135,100), outline=(255,255,255), fill=(100, 0, 0))
    draw.text((31,52), ("Salvando..."), font=status_font, fill="#00FFFF")
    disp.image(image)
    time.sleep(2)
    draw.rectangle((25,45,135,100), outline=(255,255,255), fill=(100, 0, 0))
    draw.text((31,52), ("Dados Salvo!"), font=status_font, fill="#00FFFF")
    draw.text((31,72), ("Tecle ENTRA"), font=status_font, fill="#00FFFF")
    disp.image(image)

    return

def cancel_dados ():
    #O esquema de cor é invertido tipo BGR e não RGB 
    draw.rectangle((0, 0, width, height), outline=0, fill=0) # LIMPA TELA (IMPRIME PRETO)
    # desenha uma caixa para o texto corpo de leitura
    draw.rectangle((0,0,159,127), outline=(120,120,120), fill=(0, 0, 0))
#    draw.rectangle((5,25,154,122), outline=(255,255,255), fill=(80, 0, 0))
    draw.rectangle((0,0,159,20), outline=(120,120,120), fill=(0, 0, 0))
    #imprime 2x (efeito BOLD (negrito)) no CABECARIO
    draw.text((20,2), ("CONFIGURAÇÃO"), font=status_font, fill="#707070")
    draw.text((8,28), ("Exportar dados:"), font=font, fill="#707070")
    draw.text((25,43), (" Habilitar escrita"), font=font, fill="#707070")
    draw.text((25,58), (" Desativar"), font=font, fill="#707070")
    draw.text((8,73), ("Modo de escrita:"), font=font, fill="#707070")
    draw.text((25,88), (" ao comando (KEY)"), font=font, fill="#707070")
    draw.text((25,103), (" por estabilização"), font=font, fill="#707070")
    draw.rectangle((25,45,135,100), outline=(255,255,255), fill=(100, 0, 0))
    draw.text((31,52), ("Aguarde..."), font=status_font, fill="#00FFFF")
    disp.image(image)
    time.sleep(2)
    draw.rectangle((25,45,135,100), outline=(255,255,255), fill=(100, 0, 0))
    draw.text((31,52), ("CANCELADO!"), font=status_font, fill="#00FFFF")
    draw.text((31,72), ("Tecle ENTRA"), font=status_font, fill="#00FFFF")
    disp.image(image)

    return
