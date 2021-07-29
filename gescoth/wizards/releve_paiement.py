# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class GescothAbsence(models.TransientModel):
	_name = 'gescoth.releve.paiement'
	_description = "Impression le releve de paiement"

	eleve_id = fields.Many2one('gescoth.eleve', string='Elève', required=True,)
	classe_id = fields.Many2one('gescoth.classe', string='classe', required=True,)
	annee_scolaire_id = fields.Many2one(
        'gescoth.anneescolaire',
        string='Année scolaire',
        required=True,
        default=lambda self: int(self.env['ir.config_parameter'].sudo().get_param('gescoth.annee_scolaire_id')),
    )

	def imprimer_releve_paiement(self):
		data = {}
		paiement_ids = self.env['gescoth.paiement.eleve'].search([
			('eleve_id','=', self.eleve_id.id),
			('annee_scolaire_id','=', self.annee_scolaire_id.id),
		])
		paiements = []
		for p in paiement_ids:
			vals = {
			'numer_recu':p.numer_recu,
			'eleve_id':p.eleve_id,
			'date_paiement':p.date_paiement.strftime('%d/%m/%Y'),
			'montant':p.montant,
			'recu_manuel':p.recu_manuel,
			}
			paiements.append(vals)

		data['anneescolaire'] = self.annee_scolaire_id.name
		data['paiements'] = paiements
		data['nom'] = self.eleve_id.nom_eleve
		return self.env.ref('gescoth.releve_paiement_report_view').report_action(self, data=data)