# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class GescothMusique(models.Model):
    _name = 'gescoth.musique'
    _description = 'Description'

    name = fields.Char(
    	string='Musiqe',
    )