INSERT INTO g2p_block (code, name, district) VALUES ('29050101007', 'Block 06', (SELECT id FROM g2p_district WHERE code = 'IN290501'));
INSERT INTO g2p_block (code, name, district) VALUES ('29060101001', 'Mysuru Block 1', (SELECT id FROM g2p_district WHERE code = 'IN290601'));
INSERT INTO g2p_block (code, name, district) VALUES ('29070101001', 'Belagavi Block 1', (SELECT id FROM g2p_district WHERE code = 'IN290701'));
INSERT INTO g2p_block (code, name, district) VALUES ('29070201001', 'Hubballi Block 1', (SELECT id FROM g2p_district WHERE code = 'IN290702'));
INSERT INTO g2p_block (code, name, district) VALUES ('29070301001', 'Dharwad Block 1', (SELECT id FROM g2p_district WHERE code = 'IN290703'));
INSERT INTO g2p_block (code, name, district) VALUES ('29080101001', 'Bengaluru Rural', (SELECT id FROM g2p_district WHERE code = 'IN290801'));
INSERT INTO g2p_block (code, name, district) VALUES ('29080201001', 'Bengaluru Urban', (SELECT id FROM g2p_district WHERE code = 'IN290802'));
