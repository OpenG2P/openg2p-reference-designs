from psycopg2.errors import NotNullViolation

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestBlock(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Ensure District record exists since Block depends on it
        existing_district = cls.env["g2p.district"].search([], limit=1)
        if not existing_district:
            cls.district = cls.env["g2p.district"].create(
                {
                    "name": "Test District",
                    "code": "TW",
                    "region": cls.env["g2p.region"]
                    .create(
                        {
                            "name": "Test Region",
                            "code": "TZ",
                        }
                    )
                    .id,
                }
            )
        else:
            cls.district = existing_district

    def test_01_create_block(self):
        """Test creating a new Block record."""
        block_data = {
            "name": "Test Block",
            "code": "TK",
            "district": self.district.id,
        }
        block = self.env["g2p.block"].create(block_data)
        self.assertEqual(block.name, "Test Block", "Block name is incorrect")
        self.assertEqual(block.code, "TK", "Block code is incorrect")
        self.assertEqual(block.district, self.district, "Incorrect district assigned")

    def test_02_check_required_fields(self):
        with self.assertRaises(NotNullViolation):
            self.env["g2p.block"].create(
                {
                    "name": "A",
                }
            )

    def test_03_create_block_without_district(self):
        with self.assertRaises(NotNullViolation):
            self.env["g2p.block"].create({"name": "Test Block", "code": "TK", "district": None})

    def test_04_create_block_with_empty_name(self):
        with self.assertRaises(ValidationError):
            self.env["g2p.block"].create({"name": "", "code": "TK", "district": self.district.id})

    def test_05_create_block_with_empty_code(self):
        with self.assertRaises(ValidationError):
            self.env["g2p.block"].create({"name": "Test Block", "code": "", "district": self.district.id})

    def test_06_create_block_duplicate_code(self):
        self.env["g2p.block"].create({"name": "Test", "code": "TCU", "district": self.district.id})

        with self.assertRaises(ValidationError):
            self.env["g2p.block"].create({"name": "Test", "code": "TCU", "district": self.district.id})
