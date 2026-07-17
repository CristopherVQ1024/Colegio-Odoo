# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class TomboObjetoPerdido(models.Model):
    _name = 'tombo.objeto.perdido'
    _description = 'Objeto Perdido / Encontrado'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha_hallazgo desc'

    name = fields.Char(string='Código', required=True, copy=False, readonly=True, default=lambda self: _('Nuevo'))
    descripcion = fields.Text(string='Descripción del objeto', required=True)
    imagen = fields.Binary(string='Foto del objeto', attachment=True)

    lugar_hallazgo = fields.Char(string='Lugar del hallazgo', required=True)
    fecha_hallazgo = fields.Date(string='Fecha del hallazgo', default=fields.Date.today, required=True)
    encontrado_por = fields.Char(string='Encontrado por (ciudadano/policía)')

    estado = fields.Selection([
        ('custodia', 'En Custodia'),
        ('devuelto', 'Devuelto'),
        ('no_reclamado', 'No Reclamado'),
    ], string='Estado', default='custodia', required=True, tracking=True)

    comisaria_id = fields.Many2one('tombo.comisaria', string='Comisaría', required=True)

    # Entrega al propietario
    propietario_id = fields.Many2one('res.partner', string='Propietario (si se reclama)')
    propietario_nombre = fields.Char(string='Nombre de quien reclama')
    propietario_dni = fields.Char(string='DNI de quien reclama')
    fecha_entrega = fields.Date(string='Fecha de entrega')
    entregado_por_id = fields.Many2one('tombo.policia', string='Entregado por (responsable)')
    observaciones_entrega = fields.Text(string='Observaciones de la entrega')

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('Nuevo')) == _('Nuevo'):
                vals['name'] = self.env['ir.sequence'].next_by_code('tombo.objeto.perdido') or _('Nuevo')
        return super().create(vals_list)

    def action_marcar_devuelto(self):
        self.write({'estado': 'devuelto', 'fecha_entrega': fields.Date.today()})

    def action_marcar_no_reclamado(self):
        self.write({'estado': 'no_reclamado'})

    def action_reabrir_custodia(self):
        self.write({'estado': 'custodia'})
