import re
from datetime import date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class G2PCropInformation(models.Model):
    _name = "g2p.crop.information"
    _rec_name = "partner_id"

    partner_id = fields.Many2one("res.partner", string="Farmer", required=True, index=True)
    farmer_id = fields.Char(related="partner_id.farmer_id", string="Farmer ID", readonly=True)
    crop = fields.Many2one("g2p.crop", required=True, index=True)

    collected_gc = fields.Date(string="Planted date in GC")
    season = fields.Many2one("g2p.season", store=True)
    is_diseased = fields.Selection(
        string="Has this crop been affected by illness?", selection=[("yes", "Yes"), ("no", "No")]
    )
    illness_type = fields.Many2many("g2p.illness.type", string="Disease")

    @api.constrains("is_diseased", "illness_type")
    def _check_illness_type_required(self):
        """Ensure illness_type is required if is_diseased is 'yes'."""
        for record in self:
            if record.is_diseased == "yes" and not record.illness_type:
                error_message = _("Illness type is required when the crop is diseased.")
                raise ValidationError(error_message)
