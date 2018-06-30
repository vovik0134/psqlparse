import unittest

from psqlparse import nodes


class PLpgSQLTestCase(unittest.TestCase):
    def assertFunction(self, stmt):
        self.assertIsInstance(stmt, nodes.PLpgSQLfunction)

    def assertHasVariable(self, stmt, variable):
        if not variable in stmt.datums:
            self.fail("Variable %s not found" % variable.refname)
