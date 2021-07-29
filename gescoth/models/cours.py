# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.addons.website.tools import get_video_embed_code

class GesctothCours(models.Model):
    _name = 'gescoth.cours'
    _description = 'Cours'
    _rec_name="titre"

    titre = fields.Char(
        string='Titre du cours',
        required=True,
    )
    chapitre_ids = fields.One2many(
        'gescoth.cours.chapitre',
        'cours_id',
        string='Liste des chapitres',
    )
    niveau_ids = fields.Many2many(
        'gescoth.niveau',
        string='Niveaux d\'étude',
    )
    filiere_id = fields.Many2one(
        'gescoth.filiere',
        string='Filiere',
    )
    professeur_id = fields.Many2one(
        'gescoth.professeur',
        string='Professeur',
        required=True,
    )

class GesctothCoursChapitre(models.Model):
	_name = 'gescoth.cours.chapitre'
	_description = 'Chapitre'

	name = fields.Char(
		string='Nom du chapitre',
		required=True,
		)
	binary_file = fields.Binary(
		string='Aperçu',
		attachment=True,
		)
	contenu = fields.Html(
		string='Contenu du cours',
		)
	chapitre_id = fields.Many2one(
		'gescoth.cours.chapitre',
		string='Chapitre Mère',
		)
	cours_id = fields.Many2one(
		'gescoth.cours',
		string='Cours',
		)
	niveau_id = fields.Many2one(
		'gescoth.niveau',
		string='Niveau',
		)

	video_url = fields.Char(
		'Video URL',
		help="Coller l'url de la video ici"
	)
	
	embed_code = fields.Char(
		compute="_compute_embed_code"
	)

	@api.depends('video_url')
	def _compute_embed_code(self):
		for rec in self:
			rec.embed_code = get_video_embed_code(rec.video_url)
