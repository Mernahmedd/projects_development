from odoo import models, fields, api, _

class Project(models.Model):
    _inherit = 'project.project'

    odoo_version = fields.Integer(string='Odoo Version')
    odoo_type = fields.Selection([
        ('community', 'Community'),
        ('enterprise', 'Enterprise'),
    ], string='Odoo Type', default='enterprise')
    github_repo = fields.Char(string='Github Repository')
    github_url = fields.Char(string='Github URL')
    hosting = fields.Selection([
        ('on_prem', 'On Prem'),
        ('cloud_hosting', 'Cloud Hosting'),
        ('odoo_sh', 'Odoo SH'),
        ('odoo_online', 'Odoo Online')
    ], string="Hosting")
    hosting_description = fields.Text(string='Hosting Description')

    collaborators_ids = fields.One2many('project.collaborators', 'project_id', string='Collaborators')
