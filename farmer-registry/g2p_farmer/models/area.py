from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Region(models.Model):
    _inherit = "g2p.region"

    name = fields.Char("Region")

    @api.constrains("name")
    def _check_name(self):
        for record in self:
            if not record.name:
                error_message = _("Region name should not empty.")
                raise ValidationError(error_message)

    @api.constrains("code")
    def _check_code(self):
        regions = self.search([])
        for record in self:
            if not record.code:
                error_message = _("Region Code should not empty.")
                raise ValidationError(error_message)
        for region in regions:
            if str(self.code.lower()) == str(region.code.lower()) and self.id != region.id:
                raise ValidationError(_("The code must be unique!"))

    @api.constrains("iso_code")
    def _check_iso_code(self):
        regions = self.search([])
        for record in self:
            if not record.iso_code:
                error_message = _("Region International Code should not empty.")
                raise ValidationError(error_message)
        for region in regions:
            if record.iso_code:
                if self.iso_code.lower() == region.iso_code.lower() and self.id != region.id:
                    raise ValidationError(_("The International code must be unique!"))

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        args = args or []
        domain = ["|", ("code", operator, name), ("name", operator, name)] + args
        return self.search(domain, limit=limit).name_get()

class District(models.Model):
    _name = "g2p.district"

    region = fields.Many2one("g2p.region", required=True)
    code = fields.Char(required=True, index=True)
    name = fields.Char(required=True, string="District")

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        args = args or []
        domain = ["|", ("code", operator, name), ("name", operator, name)] + args
        return self.search(domain, limit=limit).name_get()

    @api.constrains("region")
    def _check_district(self):
        for record in self:
            if not record.region:
                error_message = _("Region should not empty.")
                raise ValidationError(error_message)

    @api.constrains("name")
    def _check_name(self):
        for record in self:
            if not record.name:
                error_message = _("District name should not empty.")
                raise ValidationError(error_message)

    @api.constrains("code")
    def _check_code(self):
        districts = self.search([])
        for record in self:
            if not record.code:
                error_message = _("District Code should not empty.")
                raise ValidationError(error_message)

        for district in districts:
            if self.code.lower() == district.code.lower() and self.id != district.id:
                raise ValidationError(_("The code must be unique!"))


class Block(models.Model):
    _name = "g2p.block"

    district = fields.Many2one("g2p.district", required=True)
    code = fields.Char(required=True, index=True)
    name = fields.Char(required=True, string="Block")

    @api.constrains("district")
    def _check_district(self):
        for record in self:
            if not record.district:
                error_message = _("District should not empty.")
                raise ValidationError(error_message)

    @api.constrains("name")
    def _check_name(self):
        for record in self:
            if not record.name:
                error_message = _("block name should not empty.")
                raise ValidationError(error_message)

    @api.constrains("code")
    def _check_code(self):
        blocks = self.search([])
        for record in self:
            if not record.code:
                error_message = _("block Code should not empty.")
                raise ValidationError(error_message)

        for block in blocks:
            if self.code.lower() == block.code.lower() and self.id != block.id:
                raise ValidationError(_("The code must be unique!"))
