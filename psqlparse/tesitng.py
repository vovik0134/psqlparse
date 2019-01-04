import unittest

from psqlparse import nodes


class PLpgSQLTestCase(unittest.TestCase):
    def assertFunction(self, stmt):
        self.assertIsInstance(stmt, nodes.PLpgSQLfunction)

    def assertHasVariable(self, stmt, variable):
        self.assertIn(variable, stmt.datums)
