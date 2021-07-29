# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class GescothEmploiWizard(models.TransientModel):
    _name = 'gescoth.emploi.wizard'
    _description = 'Emploi du temps'

    type_emploi_du_temp = fields.Selection([
        ('0', 'Professeur'),
        ('1', 'Classe'),
        ])
    professeur_id = fields.Many2one(
        'gescoth.professeur',
        string='Professeur',
    )
    classe_id = fields.Many2one(
        'gescoth.classe',
        string='Classe',
        
        )

    def imprimer_emploi_du_temps(self):
        pass
        # return self.env.ref('gescoth.fiche_note_report_view').report_action(self, data=data)
