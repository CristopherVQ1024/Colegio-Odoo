# -*- coding: utf-8 -*-
from odoo import http, fields, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class TomboCustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id
        values['denuncia_count'] = request.env['tombo.denuncia'].search_count(
            [('partner_id', '=', partner.id)])
        values['incidencia_count'] = request.env['tombo.incidencia'].search_count(
            [('partner_id', '=', partner.id)])
        values['permiso_count'] = request.env['tombo.permiso.evento'].search_count(
            [('partner_id', '=', partner.id)])
        return values

    # ------------------------------------------------------------------
    # DENUNCIAS
    # ------------------------------------------------------------------
    @http.route(['/my/denuncias', '/my/denuncias/page/<int:page>'], type='http', auth='user', website=True)
    def portal_my_denuncias(self, page=1, **kw):
        partner = request.env.user.partner_id
        Denuncia = request.env['tombo.denuncia']
        domain = [('partner_id', '=', partner.id)]
        total = Denuncia.search_count(domain)
        pager = portal_pager(url='/my/denuncias', total=total, page=page, step=20)
        denuncias = Denuncia.search(domain, limit=20, offset=pager['offset'], order='fecha_registro desc')
        return request.render('tombo_city.portal_my_denuncias', {
            'denuncias': denuncias,
            'pager': pager,
            'page_name': 'denuncia',
            'default_url': '/my/denuncias',
        })

    @http.route(['/my/denuncias/nueva'], type='http', auth='user', website=True, methods=['GET', 'POST'])
    def portal_denuncia_nueva(self, **post):
        partner = request.env.user.partner_id
        if request.httprequest.method == 'POST':
            vals = {
                'partner_id': partner.id,
                'denunciante_nombre': post.get('denunciante_nombre') or partner.name,
                'denunciante_dni': post.get('denunciante_dni'),
                'denunciante_telefono': post.get('denunciante_telefono') or partner.phone,
                'denunciante_email': post.get('denunciante_email') or partner.email,
                'denunciante_direccion': post.get('denunciante_direccion'),
                'tipo_denuncia': post.get('tipo_denuncia'),
                'lugar_hechos': post.get('lugar_hechos'),
                'descripcion': post.get('descripcion'),
                'comisaria_id': int(post.get('comisaria_id')) if post.get('comisaria_id') else False,
            }
            denuncia = request.env['tombo.denuncia'].sudo().create(vals)
            return request.redirect('/my/denuncias/%s' % denuncia.id)
        comisarias = request.env['tombo.comisaria'].sudo().search([('estado', '=', 'activa')])
        return request.render('tombo_city.portal_denuncia_form', {'comisarias': comisarias})

    @http.route(['/my/denuncias/<int:denuncia_id>'], type='http', auth='user', website=True)
    def portal_denuncia_detail(self, denuncia_id, **kw):
        denuncia = request.env['tombo.denuncia'].search([
            ('id', '=', denuncia_id), ('partner_id', '=', request.env.user.partner_id.id)
        ], limit=1)
        if not denuncia:
            return request.redirect('/my/denuncias')
        return request.render('tombo_city.portal_denuncia_detail', {'denuncia': denuncia})

    # ------------------------------------------------------------------
    # INCIDENCIAS
    # ------------------------------------------------------------------
    @http.route(['/my/incidencias', '/my/incidencias/page/<int:page>'], type='http', auth='user', website=True)
    def portal_my_incidencias(self, page=1, **kw):
        partner = request.env.user.partner_id
        Incidencia = request.env['tombo.incidencia']
        domain = [('partner_id', '=', partner.id)]
        total = Incidencia.search_count(domain)
        pager = portal_pager(url='/my/incidencias', total=total, page=page, step=20)
        incidencias = Incidencia.search(domain, limit=20, offset=pager['offset'], order='fecha_registro desc')
        return request.render('tombo_city.portal_my_incidencias', {
            'incidencias': incidencias,
            'pager': pager,
            'page_name': 'incidencia',
            'default_url': '/my/incidencias',
        })

    @http.route(['/my/incidencias/nueva'], type='http', auth='user', website=True, methods=['GET', 'POST'])
    def portal_incidencia_nueva(self, **post):
        partner = request.env.user.partner_id
        if request.httprequest.method == 'POST':
            vals = {
                'partner_id': partner.id,
                'reportante_nombre': post.get('reportante_nombre') or partner.name,
                'reportante_telefono': post.get('reportante_telefono') or partner.phone,
                'tipo_incidencia': post.get('tipo_incidencia'),
                'ubicacion': post.get('ubicacion'),
                'descripcion': post.get('descripcion'),
                'comisaria_id': int(post.get('comisaria_id')) if post.get('comisaria_id') else False,
            }
            incidencia = request.env['tombo.incidencia'].sudo().create(vals)
            return request.redirect('/my/incidencias/%s' % incidencia.id)
        comisarias = request.env['tombo.comisaria'].sudo().search([('estado', '=', 'activa')])
        return request.render('tombo_city.portal_incidencia_form', {'comisarias': comisarias})

    @http.route(['/my/incidencias/<int:incidencia_id>'], type='http', auth='user', website=True)
    def portal_incidencia_detail(self, incidencia_id, **kw):
        incidencia = request.env['tombo.incidencia'].search([
            ('id', '=', incidencia_id), ('partner_id', '=', request.env.user.partner_id.id)
        ], limit=1)
        if not incidencia:
            return request.redirect('/my/incidencias')
        return request.render('tombo_city.portal_incidencia_detail', {'incidencia': incidencia})

    # ------------------------------------------------------------------
    # PERMISOS DE EVENTOS
    # ------------------------------------------------------------------
    @http.route(['/my/permisos', '/my/permisos/page/<int:page>'], type='http', auth='user', website=True)
    def portal_my_permisos(self, page=1, **kw):
        partner = request.env.user.partner_id
        Permiso = request.env['tombo.permiso.evento']
        domain = [('partner_id', '=', partner.id)]
        total = Permiso.search_count(domain)
        pager = portal_pager(url='/my/permisos', total=total, page=page, step=20)
        permisos = Permiso.search(domain, limit=20, offset=pager['offset'], order='fecha_evento desc')
        return request.render('tombo_city.portal_my_permisos', {
            'permisos': permisos,
            'pager': pager,
            'page_name': 'permiso',
            'default_url': '/my/permisos',
        })

    @http.route(['/my/permisos/nuevo'], type='http', auth='user', website=True, methods=['GET', 'POST'])
    def portal_permiso_nuevo(self, **post):
        partner = request.env.user.partner_id
        if request.httprequest.method == 'POST':
            vals = {
                'partner_id': partner.id,
                'organizador_nombre': post.get('organizador_nombre') or partner.name,
                'organizador_dni': post.get('organizador_dni'),
                'organizador_telefono': post.get('organizador_telefono') or partner.phone,
                'organizador_email': post.get('organizador_email') or partner.email,
                'tipo_evento': post.get('tipo_evento'),
                'fecha_evento': post.get('fecha_evento'),
                'lugar_evento': post.get('lugar_evento'),
                'descripcion': post.get('descripcion'),
                'comisaria_id': int(post.get('comisaria_id')) if post.get('comisaria_id') else False,
            }
            permiso = request.env['tombo.permiso.evento'].sudo().create(vals)
            return request.redirect('/my/permisos/%s' % permiso.id)
        comisarias = request.env['tombo.comisaria'].sudo().search([('estado', '=', 'activa')])
        return request.render('tombo_city.portal_permiso_form', {'comisarias': comisarias})

    @http.route(['/my/permisos/<int:permiso_id>'], type='http', auth='user', website=True)
    def portal_permiso_detail(self, permiso_id, **kw):
        permiso = request.env['tombo.permiso.evento'].search([
            ('id', '=', permiso_id), ('partner_id', '=', request.env.user.partner_id.id)
        ], limit=1)
        if not permiso:
            return request.redirect('/my/permisos')
        return request.render('tombo_city.portal_permiso_detail', {'permiso': permiso})

    # ------------------------------------------------------------------
    # OBJETOS PERDIDOS (consulta pública para usuarios logueados)
    # ------------------------------------------------------------------
    @http.route(['/my/objetos-perdidos', '/my/objetos-perdidos/page/<int:page>'], type='http', auth='user', website=True)
    def portal_objetos_perdidos(self, page=1, search='', **kw):
        Objeto = request.env['tombo.objeto.perdido']
        domain = [('estado', '=', 'custodia')]
        if search:
            domain += [('descripcion', 'ilike', search)]
        total = Objeto.search_count(domain)
        pager = portal_pager(url='/my/objetos-perdidos', total=total, page=page, step=20)
        objetos = Objeto.search(domain, limit=20, offset=pager['offset'], order='fecha_hallazgo desc')
        return request.render('tombo_city.portal_objetos_perdidos', {
            'objetos': objetos,
            'pager': pager,
            'search': search,
        })
