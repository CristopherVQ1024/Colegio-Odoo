# -*- coding: utf-8 -*-
from odoo import models, fields, api


class TomboPolicia(models.Model):
    _name = 'tombo.policia'
    _description = 'Personal Policial'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Nombre completo', required=True, tracking=True)
    dni = fields.Char(string='DNI / Documento', required=True)
    codigo_placa = fields.Char(string='Código / Placa')
    telefono = fields.Char(string='Teléfono')
    email = fields.Char(string='Correo electrónico')
    foto = fields.Binary(string='Foto', attachment=True)

    cargo = fields.Selection([
        ('comisario', 'Comisario'),
        ('supervisor', 'Supervisor'),
        ('suboficial', 'Suboficial'),
        ('oficial', 'Oficial de Policía'),
        ('agente', 'Agente'),
        ('administrativo', 'Personal Administrativo'),
    ], string='Cargo', required=True, tracking=True)

    area = fields.Selection([
        ('recepcion', 'Recepción / Atención al Ciudadano'),
        ('investigacion', 'Investigación'),
        ('patrullaje', 'Patrullaje'),
        ('logistica', 'Logística'),
        ('administracion', 'Administración'),
    ], string='Área', required=True)

    comisaria_id = fields.Many2one('tombo.comisaria', string='Comisaría', required=True, tracking=True)
    user_id = fields.Many2one('res.users', string='Usuario del sistema vinculado')

    estado = fields.Selection([
        ('activo', 'Activo'),
        ('vacaciones', 'De vacaciones/licencia'),
        ('inactivo', 'Inactivo'),
    ], string='Estado', default='activo', required=True, tracking=True)

    recurso_ids = fields.One2many('tombo.recurso', 'policia_id', string='Recursos Asignados')
    denuncia_ids = fields.One2many('tombo.denuncia', 'responsable_id', string='Denuncias a cargo')
    recurso_count = fields.Integer(compute='_compute_counts')
    denuncia_count = fields.Integer(compute='_compute_counts')

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    _sql_constraints = [
        ('dni_unique', 'unique(dni)', 'Ya existe un policía registrado con ese DNI.'),
    ]

    @api.depends('recurso_ids', 'denuncia_ids')
    def _compute_counts(self):
        for rec in self:
            rec.recurso_count = len(rec.recurso_ids)
            rec.denuncia_count = len(rec.denuncia_ids)

    def action_view_denuncias(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Denuncias a cargo',
            'res_model': 'tombo.denuncia',
            'view_mode': 'list,form',
            'domain': [('responsable_id', '=', self.id)],
        }

    def action_view_recursos(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Recursos Asignados',
            'res_model': 'tombo.recurso',
            'view_mode': 'list,form',
            'domain': [('policia_id', '=', self.id)],
        }

