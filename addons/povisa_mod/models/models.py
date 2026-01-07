# -*- coding: utf-8 -*-
from odoo import models, fields, api

# tabla para registrar pacientes
class Paciente(models.Model):
    _name = 'paciente'
    _description = 'registro de pacientes'
    _rec_name = 'nombre_completo'

    nombre = fields.Char(string='nombre', required=True)
    apellidos = fields.Char(string='apellidos', required=True)
    nombre_completo = fields.Char(string='nombre completo', compute='_compute_nombre_total', store=True)
    sintomas = fields.Text(string='sintomas del paciente')

    citas_ids = fields.One2many('cita', 'paciente_id', string='historial de citas')
    contador_visitas = fields.Integer(string='total de visitas', compute='_compute_total_citas', store=True)

    @api.depends('nombre', 'apellidos')
    def _compute_nombre_total(self):
        for p in self:
            p.nombre_completo = f"{p.nombre} {p.apellidos}".strip().lower()

    @api.depends('citas_ids')
    def _compute_total_citas(self):
        for p in self:
            p.contador_visitas = len(p.citas_ids)

# tabla para registrar médicos
class Medico(models.Model):
    _name = 'medico'
    _description = 'registro de medicos'
    _rec_name = 'nombre_completo'

    nombre = fields.Char(string='nombre', required=True)
    apellidos = fields.Char(string='apellidos', required=True)
    nombre_completo = fields.Char(string='nombre completo', compute='_compute_nombre_total', store=True)
    num_colegiado = fields.Char(string='numero de colegiado', required=True)

    consultas_ids = fields.One2many('cita', 'medico_id', string='consultas realizadas')
    pacientes_atendidos = fields.Integer(string='pacientes distintos vistos', compute='_compute_pacientes_unicos',
                                         store=True)

    @api.depends('nombre', 'apellidos')
    def _compute_nombre_total(self):
        for m in self:
            m.nombre_completo = f"{m.nombre} {m.apellidos}".strip().lower()

    @api.depends('consultas_ids.paciente_id')
    def _compute_pacientes_unicos(self):
        for m in self:
            lista_pacientes = m.consultas_ids.mapped('paciente_id.id')
            m.pacientes_atendidos = len(set(lista_pacientes))

# tabla para unir pacientes con médicos
class Cita(models.Model):
    _name = 'cita'
    _description = 'registro de citas'
    _rec_name = 'texto_resumen'

    paciente_id = fields.Many2one('paciente', string='paciente', required=True, ondelete='cascade')
    medico_id = fields.Many2one('medico', string='medico', required=True)
    diagnostico = fields.Text(string='diagnostico medico', required=True)
    fecha_cita = fields.Date(string='fecha de la cita', default=fields.Date.context_today)
    texto_resumen = fields.Char(string='resumen', compute='_compute_resumen', store=True)

    @api.depends('paciente_id', 'medico_id', 'fecha_cita')
    def _compute_resumen(self):
        for c in self:
            if c.paciente_id and c.medico_id:
                c.texto_resumen = f"cita: {c.paciente_id.nombre} con {c.medico_id.nombre} ({c.fecha_cita})".lower()
            else:
                c.texto_resumen = "nueva cita"