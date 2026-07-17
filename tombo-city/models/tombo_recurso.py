# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class TomboRecurso(models.Model):
    _name = 'tombo.recurso'
    _description = 'Recurso Policial'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Código / Identificador', required=True, tracking=True)
    tipo_recurso = fields.Selection([
        ('patrullero', 'Patrullero'),
        ('motocicleta', 'Motocicleta'),
        ('arma', 'Arma'),
        ('radio', 'Radio'),
        ('chaleco', 'Chaleco Antibalas'),
        ('computadora', 'Computadora / Equipo Informático'),
        ('otro', 'Otro'),
    ], string='Tipo de Recurso', required=True, tracking=True)

    descripcion = fields.Text(string='Descripción / Características')
    marca = fields.Char(string='Marca / Modelo')
    numero_serie = fields.Char(string='N° de Serie / Placa')

    estado = fields.Selection([
        ('disponible', 'Disponible'),
        ('asignado', 'Asignado'),
        ('mantenimiento', 'En Mantenimiento'),
        ('baja', 'Dado de Baja'),
    ], string='Estado', default='disponible', required=True, tracking=True)

    comisaria_id = fields.Many2one('tombo.comisaria', string='Comisaría', required=True)
    policia_id = fields.Many2one('tombo.policia', string='Asignado a',
                                  domain="[('comisaria_id', '=', comisaria_id)]", tracking=True)

    fecha_adquisicion = fields.Date(string='Fecha de Adquisición')
    fecha_ultimo_mantenimiento = fields.Date(string='Último Mantenimiento')
    fecha_proximo_mantenimiento = fields.Date(string='Próximo Mantenimiento')
    observaciones = fields.Text(string='Observaciones')

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    @api.onchange('policia_id')
    def _onchange_policia_id(self):
        if self.policia_id and self.estado == 'disponible':
            self.estado = 'asignado'

    def action_asignar(self):
        for rec in self:
            if not rec.policia_id:
                raise ValidationError(_('Debe seleccionar un policía para asignar este recurso.'))
            rec.estado = 'asignado'

    def action_liberar(self):
        self.write({'estado': 'disponible', 'policia_id': False})

    def action_enviar_mantenimiento(self):
        self.write({'estado': 'mantenimiento'})

    def action_dar_de_baja(self):
        self.write({'estado': 'baja', 'policia_id': False})
