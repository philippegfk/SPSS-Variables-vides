# coding: utf-8
from __future__ import unicode_literals
from PhS import *

import savReaderWriter

######################################################################################################################################################

#SPSSFile01 = '150012 - PSA Image - Argentina'
#SPSSFile02 = '150012 - PSA Image - Belgium'
#SPSSFile03 = '150012 - PSA Image - Brazil'
#SPSSFile04 = '150012 - PSA Image - China'
#SPSSFile05 = '150012 - PSA Image - Denmark'
#SPSSFile06 = '150012 - PSA Image - France'
#SPSSFile07 = '150012 - PSA Image - Germany'
#SPSSFile08 = '150012 - PSA Image - Italy'
#SPSSFile09 = '150012 - PSA Image - Netherlands'
#SPSSFile10 = '150012 - PSA Image - Poland'
#SPSSFile11 = '150012 - PSA Image - Russia'
#SPSSFile12 = '150012 - PSA Image - Spain'
#SPSSFile13 = '150012 - PSA Image - Switzerland'
#SPSSFile14 = '150012 - PSA Image - Turkey'
#SPSSFile15 = '150012 - PSA Image - UK'
#SPSSFiles = [ SPSSFile01, SPSSFile02, SPSSFile03, SPSSFile04, SPSSFile05, SPSSFile06, SPSSFile07 ]
#SPSSFiles = [ SPSSFile08, SPSSFile09, SPSSFile10, SPSSFile11, SPSSFile12, SPSSFile13, SPSSFile14, SPSSFile15 ]

SPSSFile00 = 'UK'
SPSSFiles = [ SPSSFile00 ]

######################################################################################################################################################

Debut_Exec_Total = Temps()
print ''
for SPSSFile in SPSSFiles :
	Debut_Exec = Temps()
	txt = ' Fichier « ' + SPSSFile + ' » en cours de traitement...'
	if SPSSFile == SPSSFiles[0] : print txt
	else : print txt.encode('latin1')

	# Cas spécial du format SPSS 'TIME' : même si la variable n'est pas vide, elle apparaît en 'None'
	with savReaderWriter.SavHeaderReader(SPSSFile + '.sav', ioUtf8=True, ioLocale='french') as libelles :
		# Création d'une liste de ces variables pour les enlever plus tard (même si elles sont vides...) de la liste des variables vides
		exclusions = list()
		for variable, format in libelles.formats.items() :			# Rq. : beaucoup plus rapide que :	for variable in libelles.formats :
			if format[:4] == 'TIME' : exclusions.append(variable)	# Rq. : beaucoup plus rapide que :		if libelles.formats[variable][:4] == 'TIME' : exclusions.append(variable)

	# Création d'un dictionnaire comprenant toutes les données : [incrément] -> ligne du fichier SPSS
	# L'incrément '0' représente les libellés des variables : ainsi, 'toutes_les_donnees[0]' est une liste contenant tous les libellés !
	toutes_les_donnees = dict()
	ind = 0
	donnees = savReaderWriter.SavReader(SPSSFile + '.sav', returnHeader=True, ioUtf8=True, ioLocale='french')
	for ligne in donnees :
		# Création d'une nouvelle liste (chaque ligne/individu SPSS est une liste) pour cause de problèmes de mémoire
		# Sinon il suffirait de : 'toutes_les_donnees[ind] = ligne' (*)
		nouvelle_ligne = list()
		# Première ligne : libellés des variables
		if ind == 0 : nouvelle_ligne = ligne
		# Autres lignes : individus
		else :
			var = 0
			for l in ligne :
				# Si variable sans aucune réponse
				if l == None : nouvelle_ligne.append(l)
				# Sinon (c'est à dire si la variable n'est pas égale à 'None')
				else :
					# Variables non numériques : suppression des espaces non significatifs car une variable vide peut contenir n espaces
					try :
						nouvelle_ligne.append( l.strip() )
					# Variables numériques (et non vides)
					except :
						nouvelle_ligne.append( unicode(l).strip() )
				var += 1
		toutes_les_donnees[ind] = nouvelle_ligne	# (*)
		ind += 1
	print '   - Variables :', Separe_Milliers(len(toutes_les_donnees[1]), '.')
	print '   - Individus :', Separe_Milliers(len(toutes_les_donnees) - 1, '.')

	# Création d'une liste de repérage des variables vides
	variables_vides = list()
	ind_incr = 0
	for individu, variable in sorted(toutes_les_donnees.items()) :
		# Exclusion de la ligne de libellés
		if individu != 0 :
			var_incr = 0
			for v in variable :
				# Premier individu : incrémentation de la liste avec les valeurs des variables du premier individu
				if ind_incr == 0 :	variables_vides.append(v)
				# Individus suivants : si 'None' ou vide est trouvé, alors remplacement de l'élément figurant dans la liste par la nouvelle valeur trouvée
				else :
					if variables_vides[var_incr] == None or variables_vides[var_incr] == '' :
						variables_vides[var_incr] = v
				var_incr += 1
			ind_incr += 1
	# La liste contient donc le nombre exact des variables du fichier SPSS (chaque élément de la liste représente donc une variable)
	# Si un élément de la liste est 'None' ou vide, c'est que cet élément/cette variable est vide pour tous les individus du fichier SPSS

	# Création des fichiers de stockage des variables vides trouvées
	Fichier_Vides = open(SPSSFile[:len(SPSSFile)] + '.Vides', 'w')
	Fichier_Syntaxe = open(SPSSFile[:len(SPSSFile)] + '.SPS', 'w')
	Fichier_Syntaxe.write('SAVE OUTFILE="' + os.getcwd() + '\\CLEAN ' + SPSSFile + '"  /DROP=\n')
	inc = 0
	var_vides = 0
	for var in variables_vides :
		if ( var == None or var == '' ) and not toutes_les_donnees[0][inc] in exclusions :
			# Création du fichier-texte contenant toutes les variables vides du fichier (avec leur position dans le fichier SPSS)
			Fichier_Vides.write( 'Var.' + str(inc + 1) + ' ' * ( len(str(len(toutes_les_donnees[0]))) - len(str(inc + 1)) ) + ' : ' + toutes_les_donnees[0][inc] + '\n' )
			# Création du fichier de syntaxe SPSS s'il on veut créer un nouveau fichier SPSS en supprimant les variables vides
			Fichier_Syntaxe.write( ' ' * 4 + toutes_les_donnees[0][inc] + '\n' )
			var_vides += 1
		inc += 1
	Fichier_Syntaxe.write('.')

	Fichier_Vides.close()
	Fichier_Syntaxe.close()
	# Nettoyage du répertoire si aucune variable vide trouvée
	if var_vides == 0 :
		os.remove(SPSSFile[:len(SPSSFile)] + '.Vides')
		os.remove(SPSSFile[:len(SPSSFile)] + '.SPS')
	if var_vides > 1 : s = 's'
	else : s = ''
	txt = ' ' + Separe_Milliers(var_vides, '.') + ' variable' + s + ' vide' + s + ' trouvée' + s
	if len(exclusions) > 1 : s = 's'
	else : s = ''
	txt = txt + ' (' + str( len(exclusions) ) + ' variable' + s + " de type 'TIME' exclue" + s + ').'
	print txt.encode('latin1')
	Fin_Exec = Temps()
	Chrono(Debut_Exec, Fin_Exec)

if len(SPSSFiles) > 1 : s = 's'
else : s = ''
print ( ' ' + str(len(SPSSFiles)) + ' fichier' + s + ' traité' + s + '.' ).encode('latin1')
Fin_Exec_Total = Temps()
Chrono(Debut_Exec_Total, Fin_Exec_Total)
