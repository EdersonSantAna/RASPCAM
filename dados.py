import datetime
from datetime import date
import csv

def exporta_dados_cvs(num,amostra,unid,elem):
    total = datetime.datetime.now()
    ano = '{:02d}'.format(total.year)
    mes = '{:02d}'.format(total.month)
    dia = '{:02d}'.format(total.day)
    hora = '{:02d}'.format(total.hour)
    minutos = '{:02d}'.format(total.minute)
    segundos = '{:02d}'.format(total.second)
    atual = '{}:{}:{}'.format(hora, minutos, segundos)
    
    with open('dados.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Registro ->"+atual,"#num:",num,"Amostra:",amostra,"ppm",unid,"Elemento",elem])

def cria_page_export_txt():
    data_atual = date.today()
    data = data_atual.strftime('%d/%m/%Y')
    arquivo = open('dados.txt', 'w')
    arquivo.write('Fotometro de Chama por Imagem                               Firmware rev1.0.16  set-20\n')
    arquivo.write('Projeto de conclusão de curso - Pos graduação em Sistemas Embarcados - SENAI 2018-2020\n')
    arquivo.write('\n')
    arquivo.write("Relatorio de leituras para exportação de dados     arquivo [\dados.txt] em: ")
    arquivo.write("%s"% data)
    arquivo.write('\n')
    arquivo.write('_______________________________________________________________________________________\n')
    arquivo.write("# Num.|    Amostra |   Unidade|   Símbolo|   Elemento|\n")
    arquivo.write('_______________________________________________________________________________________\n')
    arquivo.close()

def eprom_grava(data, data1, data2, data3):
    arquivo = open('parametros.eeprom', 'w')
    arquivo.write("%.0f"%data)
    arquivo.write('\n')
    arquivo.write("%.0f"%data1)
    arquivo.write('\n')
    arquivo.write("%s"%data2)
    arquivo.write('\n')
    arquivo.write("%s"%data3)
    arquivo.close()

def exporta_dados_txt(num, data, unid, simb, elem):
    arquivo = open('dados.txt', 'r')
    conteudo_data = arquivo.readlines()
    conteudo_data.append("%d"%num)
    conteudo_data.append("         ")
    conteudo_data.append("%.1f"%data)
    conteudo_data.append("         ")
    conteudo_data.append(unid)
    conteudo_data.append("         ")
    conteudo_data.append(simb)
    conteudo_data.append("         ")
    conteudo_data.append(elem)
    arquivo.close()
    arquivo = open('dados.txt', 'w')
    arquivo.writelines(conteudo_data)
    arquivo.writelines('\n')
    arquivo.close()
    
def eprom_le ():
    arquivo = open('parametros.eeprom', 'r+') #abre arquivo com parametros salvos
    nbytes=1 #numero de bytes
    data = arquivo.readlines(nbytes)
    data1 = arquivo.readlines(nbytes)
    data2 = arquivo.readlines(nbytes)
    data3 = arquivo.readlines(nbytes)
    arquivo.close() #fecha arquivo de parametros
    
    if (data == ['0\n']):data = 0
    if (data == ['1\n']):data = 1
    if (data1 == ['0\n']):data1 = 0
    if (data1 == ['1\n']):data1 = 1
    if (data2 == ['Sódio\n']):data2 = "Sódio"
    if (data2 == ['Potássio\n']):data2 = "Potássio"
    if (data2 == ['Cálcio\n']):data2 = "Cálcio"
    if (data2 == ['Lítio\n']):data2 = "Lítio"
    if (data3 == ['Na']):data3 = "Na"
    if (data3 == ['K']):data3 = "K"
    if (data3 == ['Ca']):data3 = "Ca"
    if (data3 == ['Li']):data3 = "Li"     
       
    return data, data1, data2, data3
