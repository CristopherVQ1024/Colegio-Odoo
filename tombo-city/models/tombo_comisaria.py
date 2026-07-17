# -*- coding: utf-8 -*-
from odoo import models, fields, api


class TomboComisaria(models.Model):
    _name = 'tombo.comisaria'
    _description = 'Comisaría'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Nombre de la Comisaría', required=True, tracking=True)
    direccion = fields.Char(string='Dirección', required=True)
    distrito = fields.Char(string='Distrito', required=True)
    provincia = fields.Char(string='Provincia', required=True)
    telefono = fields.Char(string='Teléfono')
    email = fields.Char(string='Correo electrónico')
    responsable_id = fields.Many2one(
        'tombo.policia', string='Responsable / Comisario a cargo',
        domain="[('comisaria_id', '=', id)]",
    )
    estado = fields.Selection([
        ('activa', 'Activa'),
        ('inactiva', 'Inactiva'),
    ], string='Estado', default='activa', required=True, tracking=True)

    policia_ids = fields.One2many('tombo.policia', 'comisaria_id', string='Personal Policial')
    recurso_ids = fields.One2many('tombo.recurso', 'comisaria_id', string='Recursos Asignados')
    denuncia_ids = fields.One2many('tombo.denuncia', 'comisaria_id', string='Denuncias')

    policia_count = fields.Integer(compute='_compute_counts', string='N° Policías')
    recurso_count = fields.Integer(compute='_compute_counts', string='N° Recursos')
    denuncia_count = fields.Integer(compute='_compute_counts', string='N° Denuncias')

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    @api.depends('policia_ids', 'recurso_ids', 'denuncia_ids')
    def _compute_counts(self):
        for rec in self:
            rec.policia_count = len(rec.policia_ids)
            rec.recurso_count = len(rec.recurso_ids)
            rec.denuncia_count = len(rec.denuncia_ids)

    def action_view_policias(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Personal Policial',
            'res_model': 'tombo.policia',
            'view_mode': 'list,form',
            'domain': [('comisaria_id', '=', self.id)],
            'context': {'default_comisaria_id': self.id},
        }

    def action_view_recursos(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Recursos Policiales',
            'res_model': 'tombo.recurso',
            'view_mode': 'list,form',
            'domain': [('comisaria_id', '=', self.id)],
            'context': {'default_comisaria_id': self.id},
        }

    def action_view_denuncias(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Denuncias',
            'res_model': 'tombo.denuncia',
            'view_mode': 'list,form',
            'domain': [('comisaria_id', '=', self.id)],
            'context': {'default_comisaria_id': self.id},
        }
