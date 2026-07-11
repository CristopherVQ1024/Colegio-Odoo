from odoo import models, fields

class Pago(models.Model):
    _name = 'colegio.pago'
    _description = 'Pago'

    fecha_pago = fields.Date(string='Fecha de pago', default=fields.Date.context_today)
    monto_pagado = fields.Float(string='Monto pagado', required=True)
    metodo_pago = fields.Selection([
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
        ('tarjeta', 'Tarjeta'),
    ], string='Método de pago')
    numero_comprobante = fields.Char(string='N° de comprobante')
    cuota_id = fields.Many2one('colegio.cuota', string='Cuota', required=True, ondelete='cascade')