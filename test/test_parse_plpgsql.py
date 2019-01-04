from psqlparse.nodes import PLpgSQLvar
from psqlparse.tesitng import PLpgSQLTestCase
from psqlparse import parse_plpgsql


class ReturnTestCase(PLpgSQLTestCase):

    def test_return_next(self):
        query = """
            CREATE OR REPLACE FUNCTION get_all_foo() RETURNS SETOF foo AS
            $BODY$
            DECLARE
                r foo%rowtype;
            BEGIN
                FOR r IN
                    SELECT * FROM foo WHERE fooid > 0
                LOOP
                    -- can do some processing here
                    RETURN NEXT r; -- return current row of SELECT
                END LOOP;
                RETURN;
            END
            $BODY$
            LANGUAGE plpgsql;
        """

        stmt = parse_plpgsql(query).pop()

        self.assertFunction(stmt)
        self.assertHasVariable(stmt, PLpgSQLvar({
            "refname": "found",
            "datatype": {
                "PLpgSQL_type": {
                    "typname": "UNKNOWN"
                }
            }
        }))
        self.assertHasVariable(stmt, PLpgSQLvar({
            "refname": "r",
            "datatype": {
                "PLpgSQL_type": {
                    "typname": "foo%rowtype"
                }
            }
        }))
