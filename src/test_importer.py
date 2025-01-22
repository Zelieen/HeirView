import unittest

from importer import *

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

class TestNode(unittest.TestCase):
    def test_file_load(self):
        read = read_in_file("./HeirView_test_export.ged")
        self.assertEqual("0 HEAD\n", read[0])

    def test_file_version(self):
        read = read_in_file("./HeirView_test_export.ged")
        self.assertEqual("5.5.1", get_version(read))
    
    def test_line_finder(self):
        read = read_in_file("./HeirView_test_export.ged")
        self.assertEqual([(8, "2 VERS 5.5.1\n")], find_lines_by_tags(read, ["HEAD", "GEDC", "VERS"]))

    def test_collect_person_info(self):
        self.assertEqual(1, collect_person_info(test_person_lines, 0)[0])        

if __name__ == "__main__":
    unittest.main()