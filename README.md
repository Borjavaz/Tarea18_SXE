# Tarea18_SXE

### Primero creo un nuevo proyecto con la siguiente estructura:

<img width="300" height="451" alt="image" src="https://github.com/user-attachments/assets/5eb550b7-012b-4928-ab7b-8dc32d1d681f" />



### A continuacion en el ```manifest.py```
 
```bash

# -*- coding: utf-8 -*-
{
    'name': "gestion povisa",
    'summary': "Modulo sencillo para el control de enfermos y especialistas",
    'description': """
        Este modulo permite gestionar:
        - Pacientes (datos y sintomas)
        - Medicos (datos y numero de colegiado)
        - Citas (union de ambos con el diagnostico)
    """,
    'author': "Borja",
    'website': "https://www.povisa.es",
    'category': 'hospital',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}

```

---

### A continuacion en el ```models.py```:

#### 1º La tabla que sirve para registrar los pacientes
 
```bash

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

```

#### 2º La tabla que sirve para registrar los medicos

```bash
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
```
#### 3º La tabla que sirve para unir pacientes con medicos

```bash
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
```

---

### Lo siguiente que hago es modificar el ```views.py``` 

```bash

<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_paciente_form" model="ir.ui.view">
        <field name="name">paciente.form</field>
        <field name="model">paciente</field>
        <field name="arch" type="xml">
            <form string="ficha del paciente">
                <sheet>
                    <group>
                        <group>
                            <field name="nombre"/>
                            <field name="apellidos"/>
                            <field name="nombre_completo" readonly="1"/>
                        </group>
                        <group>
                            <field name="contador_visitas" readonly="1"/>
                            <field name="sintomas" placeholder="describa los sintomas..."/>
                        </group>
                    </group>
                    <notebook>
                        <page string="historial de visitas">
                            <field name="citas_ids">
                                <list editable="bottom">
                                    <field name="fecha_cita"/>
                                    <field name="medico_id"/>
                                    <field name="diagnostico"/>
                                </list>
                            </field>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>

    <record id="view_paciente_list" model="ir.ui.view">
        <field name="name">paciente.list</field>
        <field name="model">paciente</field>
        <field name="arch" type="xml">
            <list string="lista de pacientes">
                <field name="nombre_completo"/>
                <field name="contador_visitas" string="visitas"/>
                <field name="sintomas" optional="show"/>
            </list>
        </field>
    </record>

    <record id="action_pacientes" model="ir.actions.act_window">
        <field name="name">pacientes</field>
        <field name="res_model">paciente</field>
        <field name="view_mode">list,form</field>
    </record>

    <record id="action_medicos" model="ir.actions.act_window">
        <field name="name">medicos</field>
        <field name="res_model">medico</field>
        <field name="view_mode">list,form</field>
    </record>

    <record id="action_citas" model="ir.actions.act_window">
        <field name="name">citas</field>
        <field name="res_model">cita</field>
        <field name="view_mode">list,form</field>
    </record>

    <menuitem id="menu_hospital_root" name="hospital povisa" sequence="10"/>
    <menuitem id="menu_paciente" name="pacientes" parent="menu_hospital_root" action="action_pacientes"/>
    <menuitem id="menu_medico" name="medicos" parent="menu_hospital_root" action="action_medicos"/>
    <menuitem id="menu_cita" name="citas" parent="menu_hospital_root" action="action_citas"/>
</odoo>

```
---

### A continuacion lo que hago es resetear el contenedor e instalar el modulo.

#### Para comprobar los cambios:

- Reiniciar el contenedor
- Activo el modo desarrollador
- Actualizo las aplicaciones 

<img width="1302" height="302" alt="image" src="https://github.com/user-attachments/assets/99d5cc31-c465-4e84-8372-1b8a57193271" />

---

## Comprobaciones:

<img width="1295" height="477" alt="image" src="https://github.com/user-attachments/assets/f6678e19-be8d-4560-8540-26f1e893b513" />

<img width="1295" height="540" alt="image" src="https://github.com/user-attachments/assets/5b420ba5-42ae-4e16-a541-e785de91baf8" />

<img width="1294" height="326" alt="image" src="https://github.com/user-attachments/assets/6ea1e08d-f62c-401a-b9d7-d71cd43dd28a" />



