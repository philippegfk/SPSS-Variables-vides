# coding: utf-8
from __future__ import unicode_literals
from PhS import *

import savReaderWriter

######################################################################################################################################################

###SPSSFile1 = 'France EPN W1.sav'
###SPSSFile2 = 'France EPN W2.sav'
###SPSSFile3 = 'France EPN W3.sav'
###SPSSFile4 = 'France EPN W4.sav'
###SPSSFiles = [ SPSSFile1, SPSSFile2, SPSSFile3, SPSSFile4 ]

SPSSFile1 = '150176 - Brand Vivo Coty - Bourjois - UAE.sav'
SPSSFiles = [ SPSSFile1 ]

######################################################################################################################################################

Debut_Exec_Total = Temps()
print ''
for SPSSFile in SPSSFiles :
	Debut_Exec = Temps()
	print ' Fichier « ' + SPSSFile + ' » en cours de traitement...'

	# Création d'un dictionnaire comprenant toutes les données : [incrément] -> ligne du fichier SPSS
	# L'incrément '0' représente les libellés des variables : ainsi, 'dico[0]' est une liste contenant tous les libellés !
	dico = dict()
	i = 0
	donnees = savReaderWriter.SavReader(SPSSFile, returnHeader=True, ioUtf8=True, ioLocale='french')
	with donnees as reader :
		for c in donnees :
			dico[i] = c
			i += 1
###			if i > 10 : break

	print '   - Variables :', Separe_Milliers(len(dico[1]), '.')
	print '   - Individus :', Separe_Milliers(len(dico) - 1, '.')

	# Création d'une liste de repérage des variables vides
	liste = list()
	ind_incr = 0
	for individu, variable in sorted(dico.items()) :
		if individu != 0 :
			var_incr = 0
			for v in variable :
				# Si les 10 premiers caractères sont blancs
				try :
					if v[:10] == ' ' * 10 : v = None
				except : pass
				# Premier individu : incrémentation de la liste avec les valeurs des variables du premier individu
				if ind_incr == 0 :	liste.append(v)
				# Individus suivants : si 'None' est trouvé, alors remplacement de l'élément figurant dans la liste par la nouvelle valeur trouvée
				else :
					if liste[var_incr] == None : liste[var_incr] = v
				var_incr += 1
			ind_incr += 1
	# La liste contient donc le nombre exact des variables du fichier SPSS (chaque élément de la liste représente donc une variable)
	# Si un élément de la liste est 'None', c'est que cet élément/cette variable est vide pour tous les individus du fichier SPSS

	Fichier_Vides = open(SPSSFile[:len(SPSSFile) - 4] + '.Vides', 'w')
	Fichier_Syntaxe = open(SPSSFile[:len(SPSSFile) - 4] + '.SPS', 'w')
	Fichier_Syntaxe.write('SAVE OUTFILE="' + os.getcwd() + '\\CLEAN ' + SPSSFile + '"  /DROP=\n')
	i = 0
	var_vides = 0
	for l in liste :
		if l == None :
			# Création du fichier-texte contenant toutes les variables vides du fichier (avec leur position dans le fichier SPSS)
			Fichier_Vides.write( 'Var.' + str(i + 1) + ' ' * ( len(str(len(dico[0]))) - len(str(i + 1)) ) + ' : ' + dico[0][i] + '\n' )
			# Création du fichier de syntaxe SPSS s'il on veut créer un nouveau fichier SPSS en supprimant les variables vides
			Fichier_Syntaxe.write( ' ' * 4 + dico[0][i] + '\n' )
			var_vides += 1
		i += 1
	Fichier_Syntaxe.write('.')

	Fichier_Vides.close()
	Fichier_Syntaxe.close()
	Fin_Exec = Temps()
	if var_vides == 0 :
		os.remove(SPSSFile[:len(SPSSFile) - 4] + '.Vides')
		os.remove(SPSSFile[:len(SPSSFile) - 4] + '.SPS')
	if var_vides > 1 : s = 's'
	else : s = ''
	print ( ' ' + Separe_Milliers(var_vides, '.') + ' variable' + s + ' vide' + s + ' trouvée' + s + '.' ).encode('latin1')
	Chrono(Debut_Exec, Fin_Exec)

Fin_Exec_Total = Temps()
if len(SPSSFiles) > 1 : s = 's'
else : s = ''
print ( ' ' + str(len(SPSSFiles)) + ' fichier' + s + ' traité' + s + '.' ).encode('latin1')
Chrono(Debut_Exec_Total, Fin_Exec_Total)