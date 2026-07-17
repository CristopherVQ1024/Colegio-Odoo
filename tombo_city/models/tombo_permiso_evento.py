# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class TomboPermisoEvento(models.Model):
    _name = 'tombo.permiso.evento'
    _description = 'Permiso para Evento'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'fecha_evento desc'

    name = fields.Char(string='Código', required=True, copy=False, readonly=True, default=lambda self: _('Nuevo'))

    # Datos del organizador
    partner_id = fields.Many2one('res.partner', string='Organizador (contacto)')
    organizador_nombre = fields.Char(string='Nombre del organizador', required=True, tracking=True)
    organizador_dni = fields.Char(string='DNI / RUC')
    organizador_telefono = fields.Char(string='Teléfono')
    organizador_email = fields.Char(string='Correo electrónico')

    tipo_evento = fields.Selection([
        ('cultural', 'Cultural'),
        ('deportivo', 'Deportivo'),
        ('religioso', 'Religioso'),
        ('comercial', 'Comercial / Feria'),
        ('social', 'Social / Fiesta'),
        ('manifestacion', 'Manifestación / Marcha'),
        ('otro', 'Otro'),
    ], string='Tipo de Evento', required=True, tracking=True)

    fecha_evento = fields.Datetime(string='Fecha y hora del evento', required=True)
    fecha_fin_evento = fields.Datetime(string='Fecha y hora de finalización')
    lugar_evento = fields.Char(string='Lugar del evento', required=True)
    aforo_estimado = fields.Integer(string='Aforo estimado')
    descripcion = fields.Text(string='Descripción del evento')

    estado = fields.Selection([
        ('solicitado', 'Solicitado'),
        ('en_revision', 'En Revisión'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ], string='Estado', default='solicitado', required=True, tracking=True, copy=False)

    revisado_por_id = fields.Many2one('tombo.policia', string='Revisado por')
    fecha_revision = fields.Datetime(string='Fecha de revisión')
    observaciones = fields.Text(string='Observaciones')
    motivo_rechazo = fields.Text(string='Motivo de rechazo')

    comisaria_id = fields.Many2one('tombo.comisaria', string='Comisaría jurisdicción')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('Nuevo')) == _('Nuevo'):
                vals['name'] = self.env['ir.sequence'].next_by_code('tombo.permiso.evento') or _('Nuevo')
        return super().create(vals_list)

    def _compute_access_url(self):
        super()._compute_access_url()
        for rec in self:
            rec.access_url = '/my/permisos/%s' % rec.id

    def action_enviar_revision(self):
        self.write({'estado': 'en_revision'})

    def action_aprobar(self):
        self.write({
            'estado': 'aprobado',
            'fecha_revision': fields.Datetime.now(),
            'revisado_por_id': self._get_current_policia(),
        })

    def action_rechazar(self):
        self.write({
            'estado': 'rechazado',
            'fecha_revision': fields.Datetime.now(),
            'revisado_por_id': self._get_current_policia(),
        })

    def _get_current_policia(self):
        policia = self.env['tombo.policia'].search([('user_id', '=', self.env.uid)], limit=1)
        return policia.id if policia else False
