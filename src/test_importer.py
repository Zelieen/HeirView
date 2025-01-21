import unittest

from importer import *

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

if __name__ == "__main__":
    unittest.main()