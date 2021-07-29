# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class GescothAbsence(models.TransientModel):
	_name = 'gescot.generer.note'
	_description = "Générer les note note à saisir"

	classe_id = fields.Many2one(
		'gescoth.classe', 
		string='classe', 
		required=True,)
	annee_scolaire = fields.Many2one(
		'gescoth.anneescolaire', 
		required=True, 
		string="Année scolaire",
		default=lambda self: int(self.env['ir.config_parameter'].sudo().get_param('gescoth.annee_scolaire_id')),
	)
	saison = fields.Selection([
		('s1','Semestre 1'),
		('s2','Semestre 2'),
		('s3','Semestre 3')
		], 
		required=True,
	)

	def generer_note_a_saisir(self):
		eleve_ids = self.env['gescoth.eleve'].search([('classe','=',self.classe_id.id)])
		if len(eleve_ids) == 0:
			raise ValidationError(_("Pas encore d'élève dans cette classe : " + self.classe_id.name))
		for eleve in eleve_ids:
			for coef in eleve.classe.coeficient_ids:
				vals = {
				'eleve_id':eleve.id,
				'classe_id':eleve.classe.id,
				'coeficient_id':coef.id,
				'saison':self.saison,
				'annee_scolaire':self.annee_scolaire.id,
				}
				note = self.env['gescoth.note'].search([
					('eleve_id','=', vals['eleve_id']),
					('classe_id','=', vals['classe_id']),
					('coeficient_id','=', vals['coeficient_id']),
					('saison','=', vals['saison']),
					('annee_scolaire','=', vals['annee_scolaire']),
				])
				if len(note) <= 0:
					self.env['gescoth.note'].create(vals)
			