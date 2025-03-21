import datetime

from psycopg2.errors import InvalidDatetimeFormat

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestG2PLiveStockInformation(TransactionCase):
    def setUp(self):
        super().setUp()
        self.farmer = self.env["res.partner"].create({"name": "Test Farmer"})
        self.livestock_type = self.env["g2p.livestock.type"].create(
            {"name": "Test Livestock Type", "code": "TLT"}
        )
        self.disease = self.env["g2p.illness.type"].create(
            {"name": "Test Disease", "code": "TD", "illness_type": "animal"}
        )
        self.season_gc = self.env["g2p.season"].create(
            {"name": "Test Season GC", "start_gc": "2020-01-01", "end_gc": "2020-12-31"}
        )


    def test_01_create_live_stock_information(self):
        """Test creating a new Live Stock Information record."""
        live_stock_info_data = {
            "partner_id": self.farmer.id,
            "livestock_type": self.livestock_type.id,
            "is_diseased": "no",
            "number_of_livestock": 5,
            "collected_gc": "2020-01-15",
            "season": self.season_gc.id,
        }
        live_stock_info = self.env["g2p.livestock.information"].create(live_stock_info_data)
        self.assertEqual(live_stock_info.partner_id, self.farmer, "Incorrect farmer assigned")
        self.assertEqual(
            live_stock_info.livestock_type, self.livestock_type, "Incorrect livestock type assigned"
        )
        self.assertEqual(
            live_stock_info.is_diseased, "no", "Livestock information incorrectly marked as diseased"
        )
        self.assertEqual(live_stock_info.number_of_livestock, 5, "Incorrect number of livestock")

    def test_02_onchange_collected_gc_sets_season_correctly(self):
        """Test onchange method for collected_gc sets the correct season."""
        live_stock_info = self.env["g2p.livestock.information"].create(
            {
                "partner_id": self.farmer.id,
                "livestock_type": self.livestock_type.id,
                "is_diseased": "no",
                "number_of_livestock": 5,
                "collected_gc": "2020-01-15",
            }
        )
        live_stock_info._onchange_collected_gc()
        self.assertEqual(
            live_stock_info.season, self.season_gc, "Season not set correctly based on collected_gc"
        )

    
    def test_03_create_live_stock_information_with_invalid_collected_gc_dates(self):
        """Test creating a Live Stock Information record with invalid dates raises ValidationError."""
        with self.assertRaises(InvalidDatetimeFormat):
            self.env["g2p.livestock.information"].create(
                {
                    "partner_id": self.farmer.id,
                    "livestock_type": self.livestock_type.id,
                    "is_diseased": "no",
                    "number_of_livestock": 5,
                    "collected_gc": "invalid-date",
                }
            )
