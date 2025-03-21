import re
from datetime import date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class G2PLiveStockInformation(models.Model):
    _name = "g2p.livestock.information"
    _rec_name = "partner_id"

    partner_id = fields.Many2one("res.partner", string="Farmer", required=True, index=True)
    farmer_id = fields.Char(related="partner_id.farmer_id", string="Farmer ID", readonly=True)
    livestock_type = fields.Many2one("g2p.livestock.type", required=True, index=True)
    number_of_livestock = fields.Integer(string="Number", required=True)
    collected_gc = fields.Date(string="Collected GC")
    season = fields.Many2one("g2p.season")
    is_diseased = fields.Selection(
        string="Has this livestock been affected by illness?", selection=[("yes", "Yes"), ("no", "No")]
    )
    illness_type = fields.Many2many("g2p.illness.type", string="Disease")

    @api.constrains("number_of_livestock")
    def _check_number_of_livestock_positive(self):
        for record in self:
            if record.number_of_livestock < 0:
                raise ValidationError(_("Number of livestock must be greater than or equal to 0."))

    @api.constrains("is_diseased", "illness_type")
    def _check_illness_type_required(self):
        """Ensure illness_type is required if is_diseased is 'yes'."""
        for record in self:
            if record.is_diseased == "yes" and not record.illness_type:
                error_message = _("Illness type is required when the crop is diseased.")
                raise ValidationError(error_message)


class G2PIllnessType(models.Model):
    _name = "g2p.illness.type"

    name = fields.Char(required=True)
    code = fields.Char(required=True, index=True)
    illness_type = fields.Selection(
        string="Type", selection=[("crop", "Crop"), ("animal", "Livestock")], required=True, index=True
    )

    @api.constrains("illness_type")
    def _check_name(self):
        for record in self:
            if not record.illness_type:
                error_message = _("illness_type should not empty.")
                raise ValidationError(error_message)

    @api.constrains("name")
    def _check_name(self):
        for record in self:
            if not record.name:
                error_message = _("name should not empty.")
                raise ValidationError(error_message)

    @api.constrains("code")
    def _check_code(self):
        records = self.search([])
        for record in self:
            if not record.code:
                error_message = _("Code should not empty.")
                raise ValidationError(error_message)

        for rec in records:
            if self.code.lower() == rec.code.lower() and self.id != rec.id:
                raise ValidationError(_("The code must be unique!"))
