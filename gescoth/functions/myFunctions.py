# -*- coding: utf-8 -*-

def Rang(note, sexe, data):
	"""Fonction permettant de calculer le rang
	d'une note en en se bansant le sexe
	"""
	rang = ""
	data.sort()
	data.reverse()
	index = data.index(note) + 1
	if index == 1 and sexe == 'feminin':
		rang = '1ère'
	elif index == 1 and sexe == 'masculin':
		rang= '1er'
	else:
		rang = str(index) + 'ème'
	if data.count(note) > 1:
		rang += ' ex'
	return rang


def Rangb(note, sexe, data):
	"""Fonction permettant de calculer le rang
	d'une note en en se bansant le sexe
	"""
	rang = ""
	data.sort()
	data.reverse()
	index = data.index(note) + 1
	if index == 1 and sexe == 'Féminin':
		rang = '1ère'
	elif index == 1 and sexe == 'Masculin':
		rang= '1er'
	else:
		rang = str(index) + 'ème'
	if data.count(note) > 1:
		rang += ' ex'
	return rang

