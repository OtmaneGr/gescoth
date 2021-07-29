# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class GescothFicheNote(models.TransientModel):
	_name = 'gescoth.note.eleve'
	_description = "Impression de la fiche de note"

	classe_id = fields.Many2one('gescoth.classe', string='classe', required=True,)
	matiere_id = fields.Many2one(
	    'gescoth.matiere',
	    string='Matière',
	)
	prof_id = fields.Many2one(
	    'gescoth.professeur',
	    string='Professeur',
	)

	def imprimer_fiche_note(self):
		data = {}
		liste_des_eleves = []
		eleves = self.env['gescoth.eleve'].search([('classe','=',self.classe_id.id)])
		for el in eleves:
			vals ={
			'matricule':el.name,
			'nom_eleve' : el.nom_eleve,
            'sexe' : el.sexe,
            'classe': self.classe_id.name,
            'matiere' : self.matiere_id.name,
            'prof': self.prof_id.name,
			}
			liste_des_eleves.append(vals)
		data['liste_des_eleves']= liste_des_eleves
		data['entete'] = self.env['ir.config_parameter'].sudo().get_param('gescoth.entete')
		return self.env.ref('gescoth.fiche_note_report_view').report_action(self, data=data)