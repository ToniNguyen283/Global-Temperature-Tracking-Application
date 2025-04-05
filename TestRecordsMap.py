import unittest
from RecordsMap import *
# Include unittests here. Focus on readability, including comments and docstrings.

class TestLocalRecord(unittest.TestCase):
    def test_init(self):
        #Test if Local Record has all the required attributes
        a = LocalRecord((41.8067, -72.2522))
        self.assertIs(a.max,None)
        self.assertIs(a.min,None)
        self.assertEqual(a.pos,(42,-72))
        self.assertEqual(a.precision,0)
        
    def test_hash(self):
        #Test the hash method to make sure that the position of the record and its hash value are equal
        a = LocalRecord((41.8067, -72.2522))
        self.assertEqual(hash(a),hash((42,-72)))

    def test_eq(self):
        #Test the equal method
        a = LocalRecord((41.8067, -72.2522))
        b = LocalRecord((41.8097, -72.1473))
        self.assertTrue(a==b)

    def test_add_report(self):
        #test the add_report method for a single record
        a = LocalRecord((41.8097, -72.1473))
        a.add_report(25)
        self.assertEqual(a.max,25)
        self.assertEqual(a.min,25)
        a.add_report(19)
        self.assertEqual(a.max,25)
        self.assertEqual(a.min,19)

class TestRecordsMap(unittest.TestCase):
    def test_add_one_report(self):
        #test the add_report method for adding a single record
        rm = RecordsMap()
        p1 = (41.8097, -72.1473)
        p2 = (41.8097, -72.1473)
        rm.add_report(p1, 25)
        self.assertTrue((42,-72) in rm)
        self.assertTrue(p2 in rm)
        self.assertEqual(rm._len,1)
        self.assertEqual(rm[p2],(25,25))

    def test_add_many_reports(self):
        #test the add_report for adding multiple records
        #in this case, we also check if hour rehashing triggers correctly when needed
        rm = RecordsMap()
        initial_capacity = rm._location
        num_entries = (2 * initial_capacity) + 1  # Force a rehash to trigger
        
        for i in range(num_entries):
            pos = (i + 0.1, i + 0.2)
            temp = 20 + i
            rm.add_report(pos, temp)

    # After rehashing, make sure all items are still correct
        for i in range(num_entries):
            pos = (i + 0.1, i + 0.2)
            self.assertTrue(pos in rm)
            self.assertEqual(rm[pos], (20 + i, 20 + i))

    # Check that rehash updated internal size
        self.assertGreater(rm._location, initial_capacity)
        
unittest.main()