from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    github_account = fields.Char(string='Github Account')
    collaborators_ids = fields.One2many('project.collaborators', 'employee_id', string='Collaborators', compute='_compute_collaborators_ids')

    @api.depends('user_id')
    def _compute_collaborators_ids(self):
        for record in self:
            record.collaborators_ids = self.env['project.collaborators'].search([('employee_id', '=', record.id)])

    @api.model
    def get_employees_api(self):
        emp_data = {
            'employees': []
        }
        employees = self.env['hr.employee'].search([])
        for emp in employees:
            data = {
                'name': emp.name,
                'projects': []
            }
            lines = []
            if len(emp.collaborators_ids) > 0:
                for line in emp.collaborators_ids.filtered(lambda x: x.state == 'active'):
                    lines.append({
                        'project': line.project_id.name
                    })

            data['projects'] = lines
            emp_data['employees'].append(data)
        return emp_data
    
    def toggle_active(self):
        res = super().toggle_active()
        for record in self:
            if not record.active:
                if len(record.collaborators_ids) > 0:
                    for line in record.collaborators_ids.filtered(lambda x: x.state == 'active'):
                        return {
                            'type': 'ir.actions.client',
                            'tag': 'display_notification',
                            'params': {
                                'title': 'Warning',
                                'message': 'An employee has some project active in it.',
                                'sticky': True,
                                'type': 'warning'
                            }
                        }

        return res

    # def write(self, vals):
    #     if 'active' in vals:
    #         if vals['active'] == False:
    #             for record in self:
    #                 if len(record.collaborators_ids) > 0:
    #                     for line in record.collaborators_ids.filtered(lambda x: x.state == 'active'):
    #                         raise UserError(_('You cannot deactivate an employee who is a collaborator in a project.'))

    #     return super(HrEmployee, self).write(vals)

class HrDepartureWizard(models.TransientModel):
    _inherit = 'hr.departure.wizard'

    def action_register_departure(self):
        res = super(HrDepartureWizard, self).action_register_departure()
        if self.employee_id:
            if len(self.employee_id.collaborators_ids) > 0:
                for line in self.employee_id.collaborators_ids.filtered(lambda x: x.state == 'active'):
                    self.env['bus.bus']._sendone(
                        self.env.user.partner_id,
                        'simple_notification',
                        {'title': 'Warning', 'message': 'An employee has some project active in it.', 'type': 'warning', 'sticky': True}
                    )
        return res

    