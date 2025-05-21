# -*- coding: utf-8 -*-

import logging
_logger = logging.getLogger(__name__)
import json
from odoo import http, SUPERUSER_ID
from odoo.http import request
import werkzeug
import base64

class IntegrationController(http.Controller):
    
    def _authenticate(self):
        """ Helper function to authenticate user via Basic Auth """
        auth_header = request.httprequest.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Basic '):
            return False
        
        # Decode credentials
        auth_decoded = base64.b64decode(auth_header[6:]).decode('utf-8')
        username, password = auth_decoded.split(':', 1)
        user = request.env['res.users'].sudo().search([('login', '=', username)], limit=1)
        if user or user.sudo()._check_credentials(password):
            return user
        return False


    @http.route('/employee', type='http', auth="none", methods=['GET'], csrf=False)
    def get_active_projects(self, **kwargs):
        self._authenticate()
        all_employees = request.env['hr.employee'].with_user(SUPERUSER_ID).get_employees_api()
        return json.dumps(all_employees, ensure_ascii=False).encode('utf8')
    
    
