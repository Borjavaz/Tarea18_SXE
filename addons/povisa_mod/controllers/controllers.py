# -*- coding: utf-8 -*-
# from odoo import http


# class PovisaMod(http.Controller):
#     @http.route('/povisa_mod/povisa_mod', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/povisa_mod/povisa_mod/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('povisa_mod.listing', {
#             'root': '/povisa_mod/povisa_mod',
#             'objects': http.request.env['povisa_mod.povisa_mod'].search([]),
#         })

#     @http.route('/povisa_mod/povisa_mod/objects/<model("povisa_mod.povisa_mod"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('povisa_mod.object', {
#             'object': obj
#         })

