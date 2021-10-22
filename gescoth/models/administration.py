# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class GescothPersonnel(models.Model):
    _name = 'gescoth.personnel'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Personnel'

    name = fields.Char(
    	string='Nom et prénom(s)',
        required=True,
    )
    telephone = fields.Char(
    	string='Téléphone',
    )
    email = fields.Char(
    	string='E-mail',
    )
    Adresse = fields.Text(
    	string='Adresse',
    )

    post_id = fields.Many2one(
        'gescoth.poste',
        string='Poste occupé',
    )
    


class GescothPost(models.Model):
    _name = 'gescoth.poste'
    _description = 'Description'

    name = fields.Char(
    	string='',
    )
