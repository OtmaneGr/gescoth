# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
# from twilio.rest import Client
# classe élève pour inscrire les élèves de l'établissement
class GescothEleve(models.Model):
	_name = 'gescoth.eleve'
	_inherit = ['mail.thread','mail.activity.mixin']
	_description = 'Elève'
	_rec_name = 'nom_eleve'
	_order = 'name'

	name = fields.Char(string="N° Matricule", readonly=True, required=True, copy=False, default='Nouveau')
	nom_eleve = fields.Char(string="Nom et prénom(s)", compute="onchange_nom_famille")
	nom_famille = fields.Char(string="Nom de famille", required=True,)
	prenom = fields.Char(string="Prénom(s)", required=True,)
	photo = fields.Binary(string="Photo de l'élève")
	date_naissance = fields.Date(string="Date de naissance",track_visibility='always', default='')
	lieu_naissance = fields.Char(string="Lieu de naissance", default='')
	sexe = fields.Selection([('masculin','Masculin'),('feminin','Féminin')], string="Sexe", default='')
	nationalite = fields.Many2one('res.country', string="Nationalité", default=216)
	telephone = fields.Char(string="Téléphone", track_visibility='onchange', default='')
	email =  fields.Char(string="E-mail", track_visibility='always')
	adresse= fields.Text(string="Adresse complète", default='')
	classe = fields.Many2one('gescoth.classe', string="Classe", default='')
	date_inscription = fields.Date(string="Date d'inscription",default=fields.Date.today())
	niveau_id = fields.Many2one(
	    'gescoth.niveau',
	    string="Niveau d'étude",
	)
	numero_cni = fields.Char(string="N° de carte d'indentité nationale")
	statut = fields.Selection([('N','Nouveau'),('D','Doublant'),('T','Triplant'),('Q','Quatriplant')], string='Statut', default='N')
	Apt_sport = fields.Boolean(string="Apte pour le sport", default=True)
	info_medicaux_ids = fields.One2many('gescoth.info.medicaux', 'eleve_id', string="Information médicales")
	active = fields.Boolean(string="Active", default=True)
	scolaire_anterieur_ids = fields.One2many(
        'gescoth.scolarite.anterieur', 'eleve_id', string="Scolarité antérieur")

	liste_des_absences_total = fields.Integer(
	    string='Total',
	    compute="_liste_des_absences_total",
	)
	liste_des_retards_total = fields.Integer(
	    string='Total',
	    compute="_liste_des_retards_total",
	)
	liste_des_punitions_total = fields.Integer(
	    string='Total',
	    compute="_liste_des_punitions_total",
	)
	liste_des_parents_total = fields.Integer(
	    string='Total',
	    compute="_liste_des_parents_total",
	)
	paiement_total = fields.Float(
	    string='Total',
	    compute="_paiement_total",
	)

	total_reste_a_payer = fields.Float(string="Reste à payer", compute="_calcule_rest_a_payer")

	conduite_ids = fields.One2many(
	    'gescoth.conduite',
	    'eleve_id',
	    string='Conduite',
	)
	date_arrive = fields.Date(string="Date d'arrivée dans l'établissement")
	derinier_etablissement = fields.Char(string="Dernier établissement férquenté")
	taille = fields.Float(string='Taille de l\'élève')
	groupe_sangin = fields.Selection(string='Group sangin', selection=[
		('1', 'A+'),
		('2', 'A-'),
		('3', 'B+'),
		('4', 'B-'),
		('5', 'O+'),
		('6', 'O-'),
		('7', 'AB+'),
		('8', 'AB-'),
		])
	absences =  fields.Float(string="Absence", compute="_calcul_absence")
	retard =  fields.Float(string="Absence", compute="_calcul_absence")
	punition =  fields.Float(string="Absence", compute="_calcul_absence")
	parent_ids = fields.One2many(
	    'gescoth.parent.eleve',
	    'eleve_id',
	    string='Parents/Tuteurs',
	)
	responsable_id = fields.Many2one(
	    'res.users',
	    string='Responsable',
	    default=lambda self: self.env.user.id,
	    readonly=True,
	)

	def _calcule_rest_a_payer(self):
		paiements = self.env['gescoth.paiement.eleve'].search([('eleve_id','=',self.id),('annee_scolaire_id','=', int(self.env['ir.config_parameter'].sudo().get_param('gescoth.annee_scolaire_id')))])
		total_paye = 0
		for p in paiements:
			total_paye += p.montant
		self.total_reste_a_payer = self.niveau_id.frais_total - total_paye

	@api.onchange('classe')
	def onchange_classe(self):
		for rec in self:
			rec.niveau_id = rec.classe.niveau_id.id
	
	def onchange_nom_famille(self):
		for rec in self:
			rec.nom_eleve = rec.nom_famille + " " + rec.prenom
	

	def envoyer_carte_eleve(self):
		template_id= self.env.ref('gescoth.eleve_email_template').id
		template = self.env['mail.template'].browse(template_id)
		return template.send_mail(self.id, force_send=True)


	def liste_des_absences(self):
		return{
			'name':('Conduites'),
			'domain':[('eleve_id','=', self.id),('type_conduite','=','absence'),('annee_scolaire_id','=', int(self.env['ir.config_parameter'].sudo().get_param('gescoth.annee_scolaire_id')))],
			'res_model':'gescoth.conduite',
			'view_id':False,
			'view_mode':'tree,form',
			'type':'ir.actions.act_window',
		}
	def _liste_des_absences_total(self):
		conduite = self.env['gescoth.conduite'].search([('eleve_id','=', self.id),('type_conduite','=','absence'),('annee_scolaire_id','=', int(self.env['ir.config_parameter'].sudo().get_param('gescoth.annee_scolaire_id')))])
		total = 0
		for c in conduite:
			total += c.nombre_heure
		self.liste_des_absences_total = total


	def liste_des_retards(self):
		return{
			'name':('Retards'),
			'domain':[('eleve_id','=', self.id),('type_conduite','=','retard'),('annee_scolaire_id','=', int(self.env['ir.config_parameter'].sudo().get_param('gescoth.annee_scolaire_id')))],
			'res_model':'gescoth.conduite',
			'view_id':False,
			'view_mode':'tree,form',
			'type':'ir.actions.act_window',
		}
	def _liste_des_retards_total(self):
		conduite = self.env['gescoth.conduite'].search([('eleve_id','=', self.id),('type_conduite','=','retard'),('annee_scolaire_id','=', int(self.env['ir.config_parameter'].sudo().get_param('gescoth.annee_scolaire_id')))])
		total = 0
		for c in conduite:
			total += c.nombre_heure
		self.liste_des_retards_total = total

	def liste_des_punitions(self):
		return{
			'name':('Punition'),
			'domain':[('eleve_id','=', self.id),('type_conduite','=','punition'),('annee_scolaire_id','=', int(self.env['ir.config_parameter'].sudo().get_param('gescoth.annee_scolaire_id')))],
			'res_model':'gescoth.conduite',
			'view_id':False,
			'view_mode':'tree,form',
			'type':'ir.actions.act_window',
		}
	def _liste_des_punitions_total(self):
		conduite = self.env['gescoth.conduite'].search([('eleve_id','=', self.id),('type_conduite','=','punition'),('annee_scolaire_id','=', int(self.env['ir.config_parameter'].sudo().get_param('gescoth.annee_scolaire_id')))])
		total = 0
		for c in conduite:
			total += c.nombre_heure
		self.liste_des_punitions_total = total

	def liste_des_parents(self):
		return{
			'name':('Parents'),
			'domain':[('eleve_id','=', self.id),('annee_scolaire_id','=', int(self.env['ir.config_parameter'].sudo().get_param('gescoth.annee_scolaire_id')))],
			'res_model':'gescoth.parent.eleve',
			'view_id':False,
			'view_mode':'tree,form',
			'type':'ir.actions.act_window',
		}

	def _paiement_total(self):
		list_paiement_total = self.env['gescoth.paiement.eleve'].search([('eleve_id','=', self.id),('annee_scolaire_id','=', int(self.env['ir.config_parameter'].sudo().get_param('gescoth.annee_scolaire_id')))])
		montant = 0
		for p in list_paiement_total:
			montant += p.montant
		self.paiement_total = montant


	def liste_des_paiements(self):
		return{
			'name':('Paiements'),
			'domain':[('eleve_id','=', self.id),('annee_scolaire_id','=', int(self.env['ir.config_parameter'].sudo().get_param('gescoth.annee_scolaire_id')))],
			'res_model':'gescoth.paiement.eleve',
			'view_id':False,
			'view_mode':'tree,form',
			'type':'ir.actions.act_window',
		}
	def _liste_des_parents_total(self):
		self.liste_des_parents_total = len(self.env['gescoth.parent.eleve'].search([('eleve_id','=', self.id)]))

	def _calcul_absence(self):
		for rec in self:
			conduite = self.env['gescoth.conduite'].search([('eleve_id', '=', rec.id), ('annee_scolaire_id', '=', int(
				self.env['ir.config_parameter'].sudo().get_param('gescoth.annee_scolaire_id')))])
			n=0
			n2=0
			n3=0
			for ab in conduite:
				if ab.type_conduite == 'absence':
					n += ab.nombre_heure
				if ab.type_conduite == 'retard':
					n2 += ab.nombre_heure
				if ab.type_conduite == 'punition':
					n3 += ab.nombre_heure

			rec.absences = n
			rec.retard = n2
			rec.punition = n3

	def afficher_conduite(self, anneescolaire, saison):
		conduite = self.env['gescoth.conduite'].search([
			('eleve_id','=',self.id),
			('annee_scolaire_id','=', anneescolaire),
			('saison','=', saison),
		])
		absences=0
		retard=0
		punition=0
		for ab in conduite:
			if ab.type_conduite == 'absence':
				absences += ab.nombre_heure
			if ab.type_conduite == 'retard':
				retard += ab.nombre_heure
			if ab.type_conduite == 'punition':
				punition += ab.nombre_heure

		return {
			'absences':absences,
			'retard':retard,
			'punition':punition,
		}


	@api.model
	def create(self, vals):
		n = self.env['gescoth.eleve'].search([])
		# if len(n)>=20:
		# 	raise ValidationError(_('Vous ne vous pouvez pas enregistrer plus de ' + n + ' élèves pour cette version'))
		if vals.get('name', 'Nouveau') == 'Nouveau':
			vals['name'] = self.env['ir.sequence'].next_by_code(
				'gescoth.eleve') or 'Nouveau'
			result = super(GescothEleve, self).create(vals)
		return result



class GescothParentEleve(models.Model):
	_name = 'gescoth.parent.eleve'
	_description = "Parent d'élève"

	name = fields.Char(
		string='Nom et prénom(s)',
		required=True
		)
	email = fields.Char(
		string='E-mail',
		)
	telephone = fields.Char(
		string='Téléphone',
		required=True,
		)
	Adresse = fields.Text(
		string='Adresse',
		)
	eleve_id = fields.Many2many(
		'gescoth.eleve',
		string='Elève',
		required=True,
		)


class GescothConduite(models.Model):
    _name = 'gescoth.conduite'
    _description = 'Conduite'
    _rec_name="eleve_id"

    eleve_id = fields.Many2one(
        'gescoth.eleve',
        string='Elève',
        required=True,
    )
    date_conduite = fields.Date(
        string='Date',
        required=True,
        default =fields.Date.today(),
    )
    type_conduite = fields.Selection([
    	('absence','Absence'),
    	('retard','Retard'),
    	('punition','Punition')
    ], string="Type",
    required=True,)

    saison = fields.Selection([
    	('s1','Semestre 1'),
    	('s2','Semestre 2'),
    	('s3','Semestre 3'),
    ], required=True)

    nombre_heure = fields.Float(
        string="Nombre d'heure",
        required=True,
    )
    motif = fields.Text(
        string='Motif',
    )
    annee_scolaire_id = fields.Many2one(
        'gescoth.anneescolaire',
        string='Année scolaire',
        required=True,
        default=lambda self: int(self.env['ir.config_parameter'].sudo().get_param('gescoth.annee_scolaire_id')),
    )

class gescothScolariteAnterieur(models.Model):
    
    _name = 'gescoth.scolarite.anterieur'
    _description = 'Scolarité antérieur'

    classe_id = fields.Many2one(
        'gescoth.classe',
        string='Classe',
    )
    annescolaire_id = fields.Many2one(
        'gescoth.anneescolaire',
        string='Année scolaire',
		
		required=True
		
    )
    etablisement = fields.Char(string="Etablissement",required=True)
    country_id = fields.Many2one(
		'res.country',
		string='Pays',required=True
		)
    villde = fields.Char(string="Ville",required=True)
    eleve_id = fields.Many2one(
        'gescoth.eleve',
        string='Elève',
    )

class GescothInfoMedicaux(models.Model):
    
	_name = 'gescoth.info.medicaux'
	_description = 'Informations médicales'

	nom_medecin = fields.Char(string="Nom du médécin", 
	required=True
	)
	telephone_medecin = fields.Char(string="Téléphone")
	date_visite = fields.Date(string="Dernière visite médicale",required=True)
	oberserations = fields.Text(string="Obervations médicales")
	email = fields.Char("Email")
	eleve_id = fields.Many2one(
		'gescoth.eleve',
		string='Elève',
		)