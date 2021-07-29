# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from .. functions.myFunctions import *
from datetime import datetime

# classe pour gérer les les coeficients
class GescothCoeficient(models.Model):
	_name = 'gescoth.coeficient'
	_description = 'Gestion des coeficient'
	_rec_name = 'matiere'

	name = fields.Many2one('gescoth.classe', string="Classe")
	matiere = fields.Many2one('gescoth.matiere', string="Matière", required=True)
	est_facultative = fields.Boolean(string="La matière est facultative")
	coef = fields.Float(string="Coeficient", default=1)
	professeur_id = fields.Many2one('gescoth.professeur','Professeur')


class GesocthNote(models.Model):
	_name = 'gescoth.note'
	_description = 'Gestion des notes'
	_rec_name = 'eleve_id'
	_sql_constraints = [
		('saison_unique_note', 'UNIQUE (eleve_id, classe_id, coeficient_id, saison)', 'Cette note existe déjà !')
	]

	eleve_id = fields.Many2one('gescoth.eleve', string="Elève", required=True)
	classe_id = fields.Many2one('gescoth.classe', string="Classe", required=True)
	coeficient_id = fields.Many2one('gescoth.coeficient', string="Matière", required=True)
	saison = fields.Selection([('s1','Semestre 1'),('s2','Semestre 2'),('s3','Semestre 3')], required=True)
	note_compo = fields.Float(string="Note de composition", store=True,)
	moy_classe = fields.Float(string="Moyenne de classe", store=True,)
	moyenne = fields.Float(string="Moyenne", default=0, store=True, )
	rang = fields.Char(string="Rang", compute="CalculerRang",)
	annee_scolaire = fields.Many2one('gescoth.anneescolaire', required=True, string="Année scolaire",)
	professeur_id = fields.Many2one('gescoth.professeur', "Professeur")
	appreciation = fields.Char(string='Appréciation', compute='Appreciation')
    
	# @api.onchange('note_compo','moy_classe')
	def CalculerRang(self):
		for rec in self:
			data = list()
			notes = self.env['gescoth.note'].search([
				('classe_id','=', rec.classe_id.id),
				('saison','=', rec.saison),
				('coeficient_id','=', rec.coeficient_id.id),
			])
			for note in notes:
				data.append(note.moyenne)
			
			rec.rang = Rang(rec.moyenne, rec.eleve_id.sexe, data)

	    

	@api.onchange('moy_classe','note_compo')	    
	def Appreciation(self):
		appr = self.env['gescoth.appreciation'].search([])
		for rec in self:
			for ap in appr:
				if rec.moyenne >= ap.inf and rec.moyenne < ap.sup:
					rec.appreciation = ap.name
				if rec.moyenne >= 20:
					rec.appreciation = 'Excellent'

	@api.constrains('moy_classe','note_compo')
	def check_notes(self):
		for rec in self:
			if rec.moy_classe < 0 or rec.moy_classe > 20:
				raise ValidationError(_('La moyenne de classe doit être entre 0 et 20. Vous avez taper : ' + str(rec.moy_classe)))
			if rec.note_compo < 0 or rec.note_compo> 20:
				raise ValidationError(_('La moyenne de classe doit être entre 0 et 20. Vous avez taper : ' + str(rec.note_compo)))

	@api.onchange('note_compo','moy_classe')
	def _onchange_note_compo(self):
		for rec in self:
			if rec.coeficient_id.est_facultative:
				res = (rec.note_compo + rec.moy_classe)/2
				if res > 10:
					rec.moyenne = res-10
				else:
					rec.moyenne = 0
			else:
				rec.moyenne = (rec.note_compo + rec.moy_classe)/2




class GescothAppreciation(models.Model):
	_name = 'gescoth.appreciation'
	_description = 'Gestion des appications'

	name= fields.Char(string="Appréciation")
	inf = fields.Float(string='Inférieur')
	sup = fields.Float(string='Supérieur')

class GescothDecision(models.Model):
	_name = 'gescoth.decision'
	_description = 'Décision'

	name= fields.Char(string="Décision")
	inf = fields.Float(string='Inférieur')
	sup = fields.Float(string='Supérieur')

class GescothResultatExamen(models.Model):
    _name = 'gescoth.examen.resultat'
    _description = "Resultat de l'exament"
    _rec_name = 'eleve_id'

    eleve_id = fields.Many2one(
        'gescoth.eleve',
        string='Eleve',
        required=True,
    )
    classe_id = fields.Many2one(
        'gescoth.classe',
        string='Classe',
        required=True,
    )

    saison = fields.Selection([
    	('s1','Semestre 1'),
    	('s2','Semestre 2'),
    	('s3','Semestre 3')
    ], 
    	required=True
    )

    annee_scolaire = fields.Many2one(
    	'gescoth.anneescolaire', 
    	required=True, 
    	string="Année scolaire",
    )
    moyenne = fields.Float(
        string='Moyenne',
    )
    rang = fields.Char(
        string='Rang',
    )



class GescothProgramExamen(models.Model):
    _name = 'gescoth.examen.program'
    _description = "Programme d'examen"

    name = fields.Char(
    	string='Description',
    )
    date_debut = fields.Date(
        string='Date de début'
    )

    date_fin = fields.Date(
        string='Date de fin'
    )
    annee_scolaire = fields.Many2one(
    	'gescoth.anneescolaire', 
    	required=True, 
    	string="Année scolaire",
    )

    organisateur = fields.Many2one(
    	'gescoth.personnel', 
    	required=True, 
    	string="Organisateur",
    )
    line_ids = fields.One2many(
        'gescoth.program.line',
        'program_id',
        string='Programmes',
    )

class GescothProgramLine(models.Model):
    _name = 'gescoth.program.line'
    _rec_name="classe_id"

    date_examen = fields.Date(
        string='Date',
    )
    heure_debut = fields.Float(
        string='Heure de début',
    )
    heure_fin = fields.Float(
        string='Heure de fin',
    )

    professeur_id = fields.Many2one(
        'gescoth.professeur',
        string='Prof Surveillant',
    )
    classe_id = fields.Many2one(
        'gescoth.classe',
        string='Classe',
    )
    matiere_id = fields.Many2one(
        'gescoth.matiere',
        string='Matière',
    )
    program_id = fields.Many2one(
        'gescoth.examen.program',
        string='Programme',
    )
