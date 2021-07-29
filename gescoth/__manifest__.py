# -*- coding: utf-8 -*-
{
    'name' : 'GescoTh',
    'version' : '1.2.0',
    'summary' : """
       Module de gestion complète des écoles secondaires officielles et privées
    """,
    'category' : 'Gestion des écoles',
    'author' : 'Thomas ATCHA',
    'maintainer' : 'Thomas ATCHA',
    'company': 'Thomas ATCHA',
    'website' : 'https://gescoth.edu',
    'depends' : ['base','mail','website'],
    'data' : [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/eleve_view.xml',
        'wizards/liste_eleve_view.xml',
        'wizards/carte.xml',
        'views/cours_view.xml',
        'views/ecole_view.xml',
        'views/settings.xml',
        'views/examen_view.xml',
        'views/administration.xml',
        'wizards/fiche_note.xml',
        'wizards/bulletin_premiere_trimestre.xml',
        'wizards/bulletin_second_trimestre.xml',
        'wizards/bulletin_troisieme_trimestre.xml',
        'wizards/bulletin_premiere_semestre.xml',
        'wizards/bulletin_second_semestre.xml',
        'wizards/generer_note.xml',
        'wizards/attribution_classe.xml',
        'views/finance_view.xml',
        'wizards/releve_paiement.xml',
        'wizards/emploi_du_temps.xml',
        'views/template.xml',
        'data/sequence.xml',
        'data/data.xml',
        'reports/eleve_report_view.xml',
        'reports/paiement_recu.xml',
        'reports/carte_report.xml',
        'reports/liste_eleve_report.xml',
        'reports/fiche_note_report.xml',
        'reports/bulletin_premiere_trimestre_report.xml',
        'reports/bulletin_second_trimestre_report.xml',
        'reports/bulletin_troisieme_trimestre_report.xml',
        'reports/bulletin_premiere_semestre_report.xml',
        'reports/bulletin_second_semestre_report.xml',
        'reports/releve_paiement_report.xml',
        'reports/fiche_paie_report.xml',
        'views/web/website_form.xml',
        'views/web/cours_webiste_view.xml',
        'views/web/examen_view.xml',
        'views/actualite_view.xml',
        'reports/program_report_view.xml',
        'reports/tranche_paiement_report.xml',
        'reports/prof_reports.xml',
        'data/mail_template.xml',
        'data/bulletin_mail_template.xml',
    ],

    'images': ['static/description/thumbnail.jpg'],
    'installable' : True,
    'application' : True,
    'auto_install' : False,
    'license' : 'AGPL-3',
}
