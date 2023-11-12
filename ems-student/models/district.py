from odoo import fields, models, api
from odoo.exceptions import ValidationError



class District(models.Model):
    _name = 'ems.district'
    _description = 'HMS District'

    name = fields.Char(required=True)
    province_id = fields.Many2one('res.country.state', domain="[('country_id.name', '=', 'Afghanistan'), ('country_id.code', '=', 'AF')]", string="Province/State", required=True)


    @api.constrains('name')
    def _check_unique_field(self):
        for district in self:
            if district.search_count([('name', '=', district.name), ('province_id', '=', district.province_id.id)]) > 1:
                raise ValidationError("This district has already been created!")