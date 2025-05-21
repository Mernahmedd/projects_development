from odoo import models, fields, api, _

class ProjectCollaborator(models.Model):
    _name = 'project.collaborators'
    _description = 'Project Collaborator'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    project_id = fields.Many2one('project.project', string='Project', default=lambda self: self._default_project_id())
    state = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], string='Status', default='active')

    def action_active(self):
        self.state = 'active'

    def action_inactive(self):
        self.state = 'inactive'

    def _default_project_id(self):
        if self.env.context.get('active_model') == 'project.project':
            return self.env.context.get('active_id')
        return False