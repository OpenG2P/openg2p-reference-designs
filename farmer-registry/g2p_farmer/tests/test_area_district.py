from psycopg2.errors import NotNullViolation

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestDistrict(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Ensure Region records exist since district depends on them
        existing_region = cls.env["g2p.region"].search([("code", "=", "NA")], limit=1)
        if not existing_region:
            cls.region = cls.env["g2p.region"].create(
                {"name": "Test Region", "code": "NA", "iso_code": "001"}
            )
        else:
            cls.region = existing_region

    def test_01_create_district(self):
        """Test creating a new District record."""
        district_data = {
            "name": "Test District",
            "code": "TW",
            "region": self.region.id,
        }
        district = self.env["g2p.district"].create(district_data)
        self.assertEqual(district.name, "Test District", "District name is incorrect")
        self.assertEqual(district.code, "TW", "District code is incorrect")
        self.assertEqual(district.region, self.region, "Incorrect Region assigned")

    def test_02_check_required_fields(self):
        with self.assertRaises(NotNullViolation):
            self.env["g2p.district"].create(
                {
                    "name": "A",
                }
            )

    def test_03_create_district_without_region(self):
        with self.assertRaises(NotNullViolation):
            self.env["g2p.district"].create({"name": "Test District", "code": "TW", "Region": ""})

    def test_04_create_district_with_empty_name(self):
        with self.assertRaises(ValidationError):
            self.env["g2p.district"].create({"name": "", "code": "TW", "region": self.region.id})

    def test_05_create_district_with_empty_code(self):
        with self.assertRaises(ValidationError):
            self.env["g2p.district"].create({"name": "Test District", "code": "", "region": self.region.id})

    def test_06_create_district_duplicate_code(self):
        self.env["g2p.district"].create({"name": "Test", "code": "TCU", "region": self.region.id})
        with self.assertRaises(ValidationError):
            self.env["g2p.district"].create({"name": "Test", "code": "TCU", "region": self.region.id})
