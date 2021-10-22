# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import *
from odoo.exceptions import ValidationError
import base64

class GescothCarte(models.TransientModel):
    _name = 'gescoth.carte'
    _description = 'Carte'

    classe_id = fields.Many2one(
        'gescoth.classe',
        string='Classe',
        required=True,
    )
    annee_scolaire_id = fields.Many2one(
        'gescoth.anneescolaire',
        string='Année scolaire',
        required=True,
        default=lambda self: int(self.env['ir.config_parameter'].sudo().get_param('gescoth.annee_scolaire_id')),
    )
    imprimer_le_cachet = fields.Boolean(string="Imprimer le cachet")
    imprimer_la_signature = fields.Boolean(string="Imprimer la signaure")

    def imprimer_cate_scolaire(self):
        data = {}
        eleves = self.env['gescoth.eleve'].search([('classe','=',self.classe_id.id)])
        if len(eleves) < 1:
            raise ValidationError(_('Pas d\'élève inscrits dans cette classe'))
        chef_id = self.env['ir.config_parameter'].sudo().get_param('gescoth.chef_etablissement')
        if int(chef_id) <= 0 or chef_id == None:
            raise ValidationError(_('Veuillez vérifier les parmatres du chef détablissement'))
        chef = self.env['gescoth.personnel'].search([('id','=', chef_id)])[0]
        liste_eleves = []
        for el in eleves:
            date =''
            if el.date_naissance:
                date = el.date_naissance.strftime('%d/%m/%Y')
            else:
                ''
            vals = {
                'nom_eleve' : el.nom_eleve,
                'photo' : el.photo,
                'date_naissance' : date,
                'lieu_naissance' : el.lieu_naissance,
                'sexe' : 'Masculin' if el.sexe == 'masculin' else 'Féminin',
                'nationalite' : el.nationalite,
                'classe' : el.classe.name,
                'statut' : el.statut,
                'Apt_sport' : el.Apt_sport,
                'anneescolaire':self.annee_scolaire_id.name,
                'chef_etablissement':chef.name,
                'titre_chef_etablissement':chef.post_id.name,
            }
            liste_eleves.append(vals)
        data['Liste_eleve'] = liste_eleves
        data['entete'] = self.env['ir.config_parameter'].sudo().get_param('gescoth.entete')
        data['image_cache'] = self.env['ir.config_parameter'].sudo(
        ).get_param('gescoth.image_cache')
        data['image_signature'] = self.env['ir.config_parameter'].sudo(
        ).get_param('gescoth.image_signature')
        data['imprimer_le_cachet'] = self.imprimer_le_cachet
        data['imprimer_la_signature'] = self.imprimer_la_signature
        return self.env.ref('gescoth.carte_report_view').report_action(self, data=data)
