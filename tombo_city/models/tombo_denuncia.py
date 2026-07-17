# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class TomboDenuncia(models.Model):
    _name = 'tombo.denuncia'
    _description = 'Denuncia Ciudadana'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'fecha_registro desc'

    name = fields.Char(string='Código', required=True, copy=False, readonly=True, default=lambda self: _('Nuevo'))
    fecha_registro = fields.Datetime(string='Fecha de Registro', default=fields.Datetime.now, required=True)

    # Datos del denunciante
    partner_id = fields.Many2one('res.partner', string='Denunciante (contacto)')
    denunciante_nombre = fields.Char(string='Nombre del Denunciante', required=True, tracking=True)
    denunciante_dni = fields.Char(string='DNI / Documento')
    denunciante_telefono = fields.Char(string='Teléfono')
    denunciante_email = fields.Char(string='Correo electrónico')
    denunciante_direccion = fields.Char(string='Dirección')

    tipo_denuncia = fields.Selection([
        ('robo', 'Robo'),
        ('hurto', 'Hurto'),
        ('violencia_familiar', 'Violencia Familiar'),
        ('agresion', 'Agresión / Lesiones'),
        ('estafa', 'Estafa'),
        ('vandalismo', 'Vandalismo'),
        ('amenaza', 'Amenazas'),
        ('otro', 'Otro'),
    ], string='Tipo de Denuncia', required=True, tracking=True)

    descripcion = fields.Text(string='Descripción de los hechos', required=True)
    lugar_hechos = fields.Char(string='Lugar de los hechos')
    fecha_hechos = fields.Datetime(string='Fecha y hora de los hechos')

    evidencia_ids = fields.Many2many('ir.attachment', string='Evidencias (opcional)')

    estado = fields.Selection([
        ('registrada', 'Registrada'),
        ('investigacion', 'En Investigación'),
        ('resuelta', 'Resuelta'),
        ('archivada', 'Archivada'),
    ], string='Estado', default='registrada', required=True, tracking=True, copy=False)

    responsable_id = fields.Many2one('tombo.policia', string='Responsable Asignado', tracking=True)
    comisaria_id = fields.Many2one('tombo.comisaria', string='Comisaría', tracking=True)

    observaciones = fields.Text(string='Observaciones / Notas de investigación')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('Nuevo')) == _('Nuevo'):
                vals['name'] = self.env['ir.sequence'].next_by_code('tombo.denuncia') or _('Nuevo')
        return super().create(vals_list)

    def _compute_access_url(self):
        super()._compute_access_url()
        for rec in self:
            rec.access_url = '/my/denuncias/%s' % rec.id

    def action_iniciar_investigacion(self):
        self.write({'estado': 'investigacion'})

    def action_resolver(self):
        self.write({'estado': 'resuelta'})

    def action_archivar(self):
        self.write({'estado': 'archivada'})

    def action_reabrir(self):
        self.write({'estado': 'registrada'})
