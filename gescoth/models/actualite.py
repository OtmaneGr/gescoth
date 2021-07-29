# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class gescothActualite(models.Model):
    _name = 'gescoth.actualite'
    _description = 'Actualité'

    name = fields.Char(
    	string="Nom de l'actuité",
    )
    description = fields.Text(
        string='Description',
    )
    image_illustre = fields.Binary(
        string='Image ullustration',
        attachment=True,
    )