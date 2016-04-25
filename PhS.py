# coding: utf-8
from __future__ import unicode_literals

# Syntaxe : from PhS import *

from datetime import date, time, datetime
import time
import os

# Chronometre
def Temps() : return datetime.now()
def Chrono(Debut, Fin) :
	Difference = Fin - Debut
	min = int(Difference.total_seconds() / 60)
	sec = int(Difference.total_seconds()) - min * 60
	txt_min = 'minute'
	txt_sec = 'seconde'
	if min > 1 : txt_min = 'minutes'
	if sec > 1 : txt_sec = 'secondes'
	txt_Difference = " Temps de compilation :"
	if min == 0 and sec == 0 : print txt_Difference, "moins d'une seconde !"
	elif min == 0 : print txt_Difference, sec, txt_sec + '.'
	else : print txt_Difference, min, txt_min, sec, txt_sec + '.'
	print ''
#var1 = Temps()
# ...
#var1 = Temps()
#Chrono(var1, var2)


def clr() : os.system('cls')


def pause() : raw_input(' Pause')


# Taille console
from ctypes import windll, create_string_buffer
# stdin handle is -10
# stdout handle is -11
# stderr handle is -12
h = windll.kernel32.GetStdHandle(-12)
csbi = create_string_buffer(22)
res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
if res:
	import struct
	(bufx, bufy, curx, cury, wattr, gauche, haut, droite, bas, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
	Taille_x = droite - gauche + 1
	Taille_y = bas - haut + 1
else:
	Taille_x, Taille_y = 80, 25 # Impossible de déterminer la taille : retour aux valeurs par defaut


# Séparation par un point ou une virgule les milliers... des nombres apparaissant à l'écran
def Separe_Milliers(nombre, separateur_de_milliers) :
	longueur = len( str(nombre) )
	separation = ( int(longueur) - 1 ) / 3
	terme = ''
	i = 0
	while i < separation :
		i = i + 1
		terme = separateur_de_milliers + str(nombre)[longueur - i * 3 : longueur] + terme
		nombre = str(nombre)[ : longueur - i * 3 ]
	return str(nombre) + str(terme)
