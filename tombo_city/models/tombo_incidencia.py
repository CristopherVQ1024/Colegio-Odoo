# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class TomboIncidencia(models.Model):
    _name = 'tombo.incidencia'
    _description = 'Incidencia Ciudadana'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'prioridad desc, fecha_registro desc'

    name = fields.Char(string='Código', required=True, copy=False, readonly=True, default=lambda self: _('Nuevo'))
    fecha_registro = fields.Datetime(string='Fecha de Registro', default=fields.Datetime.now, required=True)

    partner_id = fields.Many2one('res.partner', string='Reportado por (contacto)')
    reportante_nombre = fields.Char(string='Nombre de quien reporta')
    reportante_telefono = fields.Char(string='Teléfono de contacto')

    tipo_incidencia = fields.Selection([
        ('ruido', 'Ruido Excesivo'),
        ('vehiculo_abandonado', 'Vehículo Abandonado'),
        ('alumbrado', 'Alumbrado Público Dañado'),
        ('sospechoso', 'Persona Sospechosa'),
        ('disturbios', 'Disturbios'),
        ('emergencia_menor', 'Emergencia Menor'),
        ('otro', 'Otro'),
    ], string='Tipo de Incidencia', required=True, tracking=True)

    descripcion = fields.Text(string='Descripción')
    ubicacion = fields.Char(string='Ubicación', required=True, tracking=True)

    prioridad = fields.Selection([
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ], string='Prioridad', default='media', required=True, tracking=True)

    estado = fields.Selection([
        ('registrada', 'Registrada'),
        ('en_proceso', 'En Proceso / Atención'),
        ('resuelta', 'Resuelta'),
        ('cerrada', 'Cerrada'),
    ], string='Estado', default='registrada', required=True, tracking=True, copy=False)

    responsable_id = fields.Many2one('tombo.policia', string='Responsable / Unidad Asignada', tracking=True)
    comisaria_id = fields.Many2one('tombo.comisaria', string='Comisaría')
    denuncia_id = fields.Many2one('tombo.denuncia', string='Denuncia derivada (si aplica)')

    seguimiento = fields.Text(string='Seguimiento / Novedades')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('Nuevo')) == _('Nuevo'):
                vals['name'] = self.env['ir.sequence'].next_by_code('tombo.incidencia') or _('Nuevo')
        return super().create(vals_list)

    def _compute_access_url(self):
        super()._compute_access_url()
        for rec in self:
            rec.access_url = '/my/incidencias/%s' % rec.id

    def action_atender(self):
        self.write({'estado': 'en_proceso'})

    def action_resolver(self):
        self.write({'estado': 'resuelta'})

    def action_cerrar(self):
        self.write({'estado': 'cerrada'})

    def action_reabrir(self):
        self.write({'estado': 'registrada'})
