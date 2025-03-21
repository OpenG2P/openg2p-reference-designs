from datetime import date

from psycopg2.errors import InvalidDatetimeFormat

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestG2PCropInformation(TransactionCase):
    def setUp(self):
        super().setUp()
        self.farmer = self.env["res.partner"].create({"name": "Test Farmer"})
        self.crop_category = self.env["g2p.crop.category"].create(
            {"name": "Test Crop Category", "code": "TCC"}
        )
        self.crop = self.env["g2p.crop"].create(
            {"category": self.crop_category.id, "name": "Test Crop", "code": "TC"}
        )
        self.disease = self.env["g2p.illness.type"].create(
            {"name": "Test Disease", "code": "TD", "illness_type": "crop"}
        )
        self.season = self.env["g2p.season"].create(
            {"name": "Test Season", "start_gc": "2020-01-01", "end_gc": "2020-12-31"}
        )

    def test_01_create_crop_information(self):
        """Test creating a new Crop Information record."""
        crop_info_data = {
            "partner_id": self.farmer.id,
            "crop": self.crop.id,
            "is_diseased": "no",
            "collected_gc": "2020-01-15",
            "season": self.season.id,
        }
        crop_info = self.env["g2p.crop.information"].create(crop_info_data)
        self.assertEqual(crop_info.partner_id, self.farmer, "Incorrect farmer assigned")
        self.assertEqual(crop_info.crop, self.crop, "Incorrect crop assigned")
        self.assertEqual(crop_info.is_diseased, "no", "Crop information incorrectly marked as diseased")
        self.assertEqual(crop_info.season, self.season, "Incorrect season assigned")

    def test_02_onchange_collected_gc_sets_season_correctly(self):
        """Test onchange method for collected_gc sets the correct season."""
        crop_info = self.env["g2p.crop.information"].create(
            {
                "partner_id": self.farmer.id,
                "crop": self.crop.id,
                "is_diseased": "no",
                "collected_gc": "2020-01-15",
            }
        )
        crop_info._onchange_collected_gc()
        self.assertEqual(crop_info.season, self.season, "Season not set correctly based on collected_gc")

    def test_03_create_crop_information_with_invalid_collected_gc_dates(self):
        """Test creating a Crop Information record with invalid dates raises ValidationError."""
        with self.assertRaises(InvalidDatetimeFormat):
            self.env["g2p.crop.information"].create(
                {
                    "partner_id": self.farmer.id,
                    "crop": self.crop.id,
                    "is_diseased": "no",
                    "collected_gc": "invalid-date",
                }
            )

    def test_04_create_record_without_required_fields(self):
        """Test creating a record without required fields."""
        with self.assertRaises(ValidationError):
            self.env["g2p.crop.information"].create(
                {
                    "partner_id": self.farmer.id,
                    "crop": self.crop.id,
                    "is_diseased": "yes",
                    "collected_gc": "2020-01-01",
                    "season": self.season.id,
                }
            )

    def test_05_check_illness_type_required(self):
        """Test checking if illness_type is required when is_diseased is 'yes'."""
        with self.assertRaises(ValidationError):
            self.env["g2p.crop.information"].create(
                {
                    "partner_id": self.farmer.id,
                    "crop": self.crop.id,
                    "is_diseased": "yes",
                    "collected_gc": "2020-01-01",
                    "season": self.season.id,
                }
            )

    def test_06_check_collected_dates_empty(self):
        """Test error when collected_gc is empty."""
        with self.assertRaises(ValidationError):
            self.env["g2p.crop.information"].create(
                {
                    "partner_id": self.farmer.id,
                    "crop": self.crop.id,
                    "collected_gc": False,
                }
            )
