from odoo import models, fields, api, _

class ProjectTask(models.Model):
    _inherit = 'project.task'

    developer_id = fields.Many2one('hr.employee', string='Developer')
    functional_id = fields.Many2one('hr.employee', string='Functional Consultant')
    development_status = fields.Selection([
        ('pending', 'Pending'),
        ('ongoing', 'Ongoing'),
        ('delivered', 'Delivered'),
        ('onhold', 'Onhold'),
        ('cancelled', 'Cancelled'),
    ], string='Development Status', default='pending', tracking=True)
    module = fields.Char(string='Module')
    branch = fields.Char(string='Branch')
    release_notes = fields.Text(string='Release Notes')
    dev_priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
    ], string='Priority')
    internal_deadline = fields.Date(string='Internal Deadline')
    allocated_time = fields.Float(string='Allocated Tome', compute='_compute_allocated_time', store=True)
    res_time = fields.Float(string='Research and Solution design allocated time')
    dev_time = fields.Float(string='Development allocated time')
    test_time = fields.Float(string='Testing allocated time')
    task_no = fields.Char(string='Task Number')

    @api.depends('res_time', 'dev_time', 'test_time')
    def _compute_allocated_time(self):
        for record in self:
            record.allocated_time = record.res_time + record.dev_time + record.test_time

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['task_no'] = self.env['ir.sequence'].get('project.task')
        return super(ProjectTask, self).create(vals_list)
    