# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class GescothAbsence(models.TransientModel):
	_name = 'gescoth.liste.eleve'
	_description = "Impression des liste d'élève"

	classe_id = fields.Many2one('gescoth.classe', string='classe', required=True,)

	def imprimer_liste_eleve(self):
		data = {}
		liste_des_eleves = []
		eleves = self.env['gescoth.eleve'].search([('classe','=',self.classe_id.id)])
		for el in eleves:
			vals ={
			'matricule':el.name,
			'nom_eleve' : el.nom_eleve,
            'photo' : el.photo,
            'date_naissance' : el.date_naissance,
            'lieu_naissance' : el.lieu_naissance,
            'sexe' : el.sexe,
            'nationalite' : el.nationalite,
            'classe' : el.classe.name,
            'statut' : el.statut,
            'Apt_sport' : el.Apt_sport,
			}
			liste_des_eleves.append(vals)
		data['liste_des_eleves']= liste_des_eleves
		return self.env.ref('gescoth.liste_eleve_report_view').report_action(self, data=data)