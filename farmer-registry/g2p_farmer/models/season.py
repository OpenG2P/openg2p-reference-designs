import re
from datetime import date

from odoo import _, fields, models


class G2PSeason(models.Model):
    _name = "g2p.season"
    _description = "Season"

    name = fields.Char(required=True)
    start_gc = fields.Date(index=True)
    end_gc = fields.Date()
    year_gc = fields.Integer(index=True)