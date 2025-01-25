import unittest

from importer import *
from node import Event, Family

test_person_lines = [
    "0 @I1@ INDI",
    "1 NAME Leia/SKYWALKER/",
    "2 GIVN Leia",
    "2 SURN SKYWALKER",
    "1 SEX F",
    "1 _FIL LEGITIMATE_CHILD",
    "1 CHAN",
    "2 DATE 18 JAN 2025",
    "3 TIME 12:47",
    "1 BIRT",
    "2 DATE 4 OCT 1981",
    "2 PLAC Polis Massa,,,,,",
    "2 _FNA NO",
    "1 DEAT",
    "2 DATE 1 SEP 2035",
    "2 PLAC Ajan Kloss,,,,,",
    "2 _FNA NO",
    "1 FAMC @F2@",
    "0 @I2@ INDI"
    ]

test_family_lines = [
    "0 @F2@ FAM",
    "1 HUSB @I2@",
    "1 WIFE @I4@",
    "1 _UST MARRIED",
    "1 CHIL @I1@",
    "1 CHIL @I3@",
    "1 MARR",
    "2 DATE 16 AUG 1978",
    "2 PLAC Naboo,,,,,Seenland",
    "2 _FNA NO",
    "0 TRLR"
    ]

class TestNode(unittest.TestCase):
    def test_file_load(self):
        read = read_in_file("./HeirView_test_export.ged")
        self.assertEqual("0 HEAD", read[0])

    def test_file_version(self):
        read = read_in_file("./HeirView_test_export.ged")
        self.assertEqual("5.5.1", get_version(read))
    
    def test_line_finder(self):
        read = read_in_file("./HeirView_test_export.ged")
        self.assertEqual([(8, "2 VERS 5.5.1")], find_lines_by_tags(read, ["HEAD", "GEDC", "VERS"]))

    def test_file_blocks(self):
        read = read_in_file("./HeirView_test_export.ged")
        self.assertEqual([(0, 14), (14, 32), (32, 50), (50, 68), (68, 86), (86, 96), (96, 96)], find_blocks(read))
        self.assertEqual("0 @I2@ INDI", read[find_blocks(read)[2][0]])

    def test_collect_person_info(self):
        self.assertEqual(1, collect_person_info(test_person_lines)[0])

    def test_make_person_from_info(self):
        p = Person(1, "Leia", "SKYWALKER")
        self.assertEqual(str(p), str(make_person_from_info(*collect_person_info(test_person_lines))))

    def test_made_person_events(self):
        e = Event("birth", [1], "4 OCT 1981", "Polis Massa")
        self.assertEqual(str(e), str(make_person_from_info(*collect_person_info(test_person_lines)).birth))

    def test_collect_family_info(self):
        f_test = (4, 2, [1, 3], "16 AUG 1978", "Naboo")
        self.assertEqual(str(f_test), str(collect_family_info(test_family_lines)))

    def test_collect_all_info_persons(self):
        read = read_in_file("./HeirView_test_export.ged")
        blocks = find_blocks(read)
        self.assertEqual(4, len(extract_info(read, blocks)[0]))

    def test_collect_all_info_family(self):
        read = read_in_file("./HeirView_test_export.ged")
        blocks = find_blocks(read)
        self.assertEqual(1, len(extract_info(read, blocks)[1]))

    def test_event_missing(self):
        p = test_person_lines[:-7]
        self.assertEqual(str(None), str(make_person_from_info(*collect_person_info(p)).death))

if __name__ == "__main__":
    unittest.main()