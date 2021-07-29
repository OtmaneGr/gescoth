# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class GescothAttributClasse(models.TransientModel):
    _name = 'gescoth.attriubtion.classe'
    _description = 'Réattribution des classe'

    eleve_ids = fields.Many2many(
        'gescoth.eleve',
        string='Elèves',
    )
    classe_id = fields.Many2one(
        'gescoth.classe',
        string='Nouvelle classe',
    )

    def change_classe(self):
        for el in self.eleve_ids:
            el.classe = self.classe_id.id