from odoo import models, fields, api
from datetime import date

class Cuota(models.Model):
    _name = 'colegio.cuota'
    _description = 'Cuota'

    periodo = fields.Char(string='Periodo', required=True)
    monto = fields.Float(string='Monto', required=True)
    fecha_vencimiento = fields.Date(string='Fecha de vencimiento')
    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('vencido', 'Vencido'),
    ], string='Estado', default='pendiente')
    colegiado_id = fields.Many2one('colegio.colegiado', string='Colegiado', required=True, ondelete='cascade')
    pago_ids = fields.One2many('colegio.pago', 'cuota_id', string='Pagos')

    @api.model
    def _cron_actualizar_vencidas(self):
        cuotas = self.search([('estado', '=', 'pendiente'), ('fecha_vencimiento', '<', date.today())])
        cuotas.write({'estado': 'vencido'})