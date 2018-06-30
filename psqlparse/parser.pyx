import json

import six

from .nodes.utils import build_from_obj
from .exceptions import PSqlParseError
from .pg_query cimport (pg_query_parse, pg_query_free_parse_result,
                        PgQueryParseResult, pg_query_parse_plpgsql,
                        pg_query_free_plpgsql_parse_result, PgQueryPlpgsqlParseResult)


def encode_query(query):
    if isinstance(query, six.text_type):
        encoded_query = query.encode('utf8')
    elif isinstance(query, six.binary_type):
        encoded_query = query
    else:
        encoded_query = six.text_type(query).encode('utf8')

    return encoded_query


def parse(query):
    result = pg_query_parse(encode_query(query))
    if result.error:
        error = PSqlParseError(result.error.message.decode('utf8'),
                               result.error.lineno, result.error.cursorpos)
        pg_query_free_parse_result(result)
        raise error

    statement_dicts = json.loads(result.parse_tree.decode('utf8'),
                                 strict=False)
    pg_query_free_parse_result(result)

    return [build_from_obj(obj) for obj in statement_dicts]


def parse_plpgsql(query):
    result = pg_query_parse_plpgsql(encode_query(query))
    if result.error:
        error = PSqlParseError(result.error.message.decode('utf8'),
                               result.error.lineno, result.error.cursorpos)
        pg_query_free_plpgsql_parse_result(result)
        raise error

    statement_dicts = json.loads(result.plpgsql_funcs.decode('utf8'),
                                 strict=False)
    pg_query_free_plpgsql_parse_result(result)

    return [build_from_obj(obj) for obj in statement_dicts]
