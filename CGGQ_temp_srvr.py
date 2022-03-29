#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# LUPLtemperature.py
#
# Author: Cristian Gabriel Garcia Quezada
# Original by:  Mauricio Matamoros
# Licence: MIT
# Date:    2023.03.28
# 
# Reads temperature from a LM35 interfaced via an Arduino ADC
# connected as I2C slave.
#
# ## #############################################################

import smbus2
import struct
import time

# Initializes virtual board (comment out for hardware deploy)
from CGGQ_virtualboards import run_temperature_board

# Arduino's I2C device address
SLAVE_ADDR = 0x0A # I2C Address of Arduino

# Name of the file in which the log is kept
LOG_FILE = './temp_history.log'                 #nombre del archivo donde se guardaran los datos

# Initialize the I2C bus;
# RPI version 1 requires smbus.SMBus(0)
i2c = smbus2.SMBus(1)
    
    
def readTemperature():
	"""Reads a temperature bytes from the Arduino via I2C"""
	try:
		msg = smbus2.i2c_msg.read(SLAVE_ADDR, 2)
		i2c.i2c_rdwr(msg)
		data = list(msg)
		temp = struct.unpack('<H', msg.buf)[0]          #se quieren leer 16 bits(10 bits ADC)
		print('Received ADC temp value: {} = {:0.2f}'.format(data, temp))
		return temp
	except:
		return None
#end def


def log_temp(temperature):
	try:
		with open(LOG_FILE, 'a') as fp:
			fp.write('{} {:0.2f}C\n'.format(
				time.strftime("%Y.%m.%d %H:%M:%S"),
				temperature
			))
	except:
		return
#end def

def main():
    bits8 = 255          #convertidor de 8 bits
    bits10 = 1024        #convertidor de 10 bits
    rh=True             #variable para dar valor true o false dependiendo de la veracidad de los datos, en un inicio se define como True
    while rh:           #comienza una sentencia que validara los datos, en caso de ser erroneos los volvera a pedir
        r1= float(input("valor r1 "))   #valor resistencia 1
        r2= float(input("valor R2 "))   #valor resistencia 2
        frequencia = int(input("valor de la frecuencia,entre 1 y 100 HZ ")) #valor de la frecuencia a usar
        resolucion=int(input("resolucion 8 o 10 bits "))        #resolucion ya sea de 8 o 10 bits, dependiendo la elegida se dara un valor
        if frequencia >= 1 and frequencia <= 100 and r1 >=1 and r1 <=100000 and r2 >= 1 and r2<= 100000 and resolucion == 8 or resolucion == 10:  #validacion de parametros
            rh=False                   #cambiamos a False la variable, indicando que los datos son correctos y salir del bucle
            if(resolucion == 8):        #condicion para levantar
                res = True              #una bandera
            elif(resolucion == 10):     #dependiendo de la resolucion   que ocupemos
                res = False             # sera true si es de 8, y false si es de 10
            else:                       #si los valores de la resolucion no son correctos 
                input("la resolucion introducida es incorrecta")#manda un mensaje 
        else:                      #si la validacion de datos es incorrecta
            print("valor invalido")#mandara un mensaje y volvera al inicio del while


	# Runs virtual board (comment out for hardware deploy)
    run_temperature_board(r1, r2, p8bits= res, freq = frequencia)
    valorRef = (r2/(r1+r2))*5            #para calcular el valor referido
    time.sleep(1)
    while True:
         try:
             cTemp = readTemperature()
             if(res == True):                                       #condicionales para
                 temperaturacenti = (cTemp * (valorRef/bits8))*100  #convertir la temperatura 
             else:                                                  #a grados centigrados
                 temperaturacenti = (cTemp * (valorRef/bits10))*100 #dependiendo de el convertidor elegido
             log_temp(temperaturacenti)
             time.sleep(1)
         except KeyboardInterrupt:
             return
#end def

if __name__ == '__main__':
	main()
