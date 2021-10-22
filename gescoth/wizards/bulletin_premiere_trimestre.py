# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from .. functions.myFunctions import *
from math import *


class GescothBulletinPremierSemestre(models.TransientModel):
	_name = 'gescoth.bulletin.premier.trimestre'
	_description = "Impression des bulltins du premier trimestre"

	classe_id = fields.Many2one('gescoth.classe', string='classe', required=True,)
	annee_scolaire_id = fields.Many2one(
		'gescoth.anneescolaire',
		required=True,
		string="Année scolaire",
		default=lambda self: int(self.env['ir.config_parameter'].sudo().get_param('gescoth.annee_scolaire_id')),
	)
	date_signature = fields.Date(
	    string='Date de signature',
	    required=True,
	    default=fields.date.today(),
	)
	eleve_id = fields.Many2one(
		'gescoth.eleve',
		string='Eleve',
		# domain=[('classe_id','=',self.classe_id.id), ],
		)

	def imprimer_bulletin_premier_trimestre(self):
		data = {}
		liste_note = []
		liste_note_total = []
		eleve_ids = self.env['gescoth.eleve'].search([('classe','=', self.classe_id.id)])
		if len(eleve_ids) <= 0:
			raise ValidationError(_("Pas encore d'élève dans cette classe !"))
		for el in eleve_ids:
			eleve = {
				'id':el.id,
				'nom_eleve': el.nom_eleve,
				'classe':el.classe.name,
				'sexe':'Masculin' if el.sexe == 'masculin' else 'Féminin',
				'Apt_sport':el.Apt_sport,
				'statut':el.statut,
				'saison':'Premiere trimestre',
				'conduite':el.afficher_conduite(self.annee_scolaire_id.id,'s1'),
			}
			el_note_ids = self.env['gescoth.note'].search([('eleve_id','=', el.id),('saison','=','s1'),('annee_scolaire','=', self.annee_scolaire_id.id)])
			if len(el_note_ids) <= 0:
				raise ValidationError(_("Veuillez générer toutes les notes d'abord !"))
			note_eleve = []
			coef= 0
			total = 0
			for note in el_note_ids:
				matiere = note.coeficient_id.matiere.nom_abrege if note.coeficient_id.matiere.user_abrege else note.coeficient_id.matiere.name
				vals_note = {
					'matiere' : matiere,
					'type_matiere': note.coeficient_id.matiere.type_matiere,
					'note_intero':note.note_intero,
					'note_devoir':note.note_devoir,
					'moy_classe':note.moy_classe,
					'note_compo': note.note_compo,
					'moyenne':note.moyenne,
					'coef':note.coeficient_id.coef,
					'total': note.moyenne * note.coeficient_id.coef,
					'rang':note.rang,
					'appreciation':note.appreciation,
					'prof':note.coeficient_id.professeur_id.name,
					'non_classe': note.non_classe,
				}
				if note.coeficient_id.matiere.type_matiere == 'sport' and not el.Apt_sport:
					pass
				else:
					if not note.coeficient_id.est_facultative:
						coef += note.coeficient_id.coef
					total += (note.moyenne * note.coeficient_id.coef)
				note_eleve.append(vals_note)

			eleve['total_coef'] = coef
			eleve['total_moyenne'] = total
			eleve['moyenne_sur_vingt'] = round((total/coef),2)
			eleve['notes'] = note_eleve


			liste_note.append(eleve)
			liste_note_total.append(round((total/coef),2))

		for el in liste_note:
			el['rang'] = Rang(el['moyenne_sur_vingt'],el['sexe'],liste_note_total)


		#appréciations générales
		decision = self.env['gescoth.decision'].search([])
		for el in liste_note:
			for dc in decision:
				if dc.name == "Tableau d'Excellence":
					if el['moyenne_sur_vingt'] >= dc.inf and el['moyenne_sur_vingt'] < dc.sup:
						el['tableau_excellence'] = "Oui"
					else:
						el['tableau_excellence'] = ""

		for el in liste_note:
			for dc in decision:
				if dc.name == "Tableau d'Honneur + Félicitations":
					if el['moyenne_sur_vingt'] >= dc.inf and el['moyenne_sur_vingt'] < dc.sup:
						el['tableau_honneur_felicitation'] = "Oui"
					else:
						el['tableau_honneur_felicitation'] = ""


		for el in liste_note:
			for dc in decision:
				if dc.name == "Tableau d'Honneur + Encouragements":
					if el['moyenne_sur_vingt'] >= dc.inf and el['moyenne_sur_vingt'] < dc.sup:
						el['tableau_honneur_encouragement'] = "Oui"
					else:
						el['tableau_honneur_encouragement'] = ""


		for el in liste_note:
			for dc in decision:
				if dc.name == "Tableau d'Honneur":
					if el['moyenne_sur_vingt'] >= dc.inf and el['moyenne_sur_vingt'] < dc.sup:
						el['tableau_honneur'] = "Oui"
					else:
						el['tableau_honneur'] = ""

		for el in liste_note:
			for dc in decision:
				if dc.name == "Avertissement":
					if el['moyenne_sur_vingt'] >= dc.inf and el['moyenne_sur_vingt'] < dc.sup:
						el['avertissement'] = "Oui"
					else:
						el['avertissement'] = ""

		for el in liste_note:
			for dc in decision:
				if dc.name == "Blâme":
					if el['moyenne_sur_vingt'] >= dc.inf and el['moyenne_sur_vingt'] < dc.sup:
						el['blame'] = "Oui"
					else:
						el['blame'] = ""


		ICPSudo = self.env['ir.config_parameter'].sudo()
		data['ville'] = ICPSudo.get_param('gescoth.ville')

		chef_id = self.env['ir.config_parameter'].sudo().get_param('gescoth.chef_etablissement')
		if int(chef_id) <= 0 or chef_id == None:
			raise ValidationError(_('Veuillez vérifier les parmatres du chef détablissement'))
		chef = self.env['gescoth.personnel'].search([('id','=', chef_id)])[0]

		liste_definitive = []
		list_unique = []

		for eleve in liste_note:
			if eleve['id'] == self.eleve_id.id:
				list_unique.append(eleve)
		if len(list_unique) == 1:
			liste_definitive = list_unique
		else :
			liste_definitive = liste_note

		data['moyMaxi'] = round(max(liste_note_total),2)
		data['moyMini'] = round(min(liste_note_total),2)
		data['moyGene'] = round(sum(liste_note_total)/len(eleve_ids),2)
		data['note_des_eleve'] = liste_definitive
		data['anneescolaire_id'] = self.annee_scolaire_id.name
		data['effectif'] = len(eleve_ids)
		data['date_signature'] = self.date_signature.strftime('%d/%m/%Y')
		data['chef_etablissement'] = chef.name
		data['titre_chef_etablissement'] = chef.post_id.name
		data['prof'] = self.classe_id.professeur.name
		data['entete'] = self.env['ir.config_parameter'].sudo().get_param('gescoth.entete')

		for el in liste_note:
			vals = {
				'eleve_id':el['id'],
				'classe_id':self.classe_id.id,
				'saison': 's1',
				'annee_scolaire': self.annee_scolaire_id.id,
				'moyenne' :el['moyenne_sur_vingt'],
				'rang': el['rang'],
			}
			exist = self.env['gescoth.examen.resultat'].search([
				('eleve_id','=',el['id']),
				('classe_id','=',self.classe_id.id),
				('saison','=', 's1'),
				('annee_scolaire','=', self.annee_scolaire_id.id,)
				])
			if exist != None:
				exist.unlink()
			self.env['gescoth.examen.resultat'].create(vals)
		return self.env.ref('gescoth.bulltin_premiere_trimestre_report_view').report_action(self, data=data)
