import math
import re

from django.db.models import Q


def is_correct_brackets(value):
    """
    Check correct brackets in phrase
    """
    count = 0
    for symbol in value:
        if symbol == "(":
            count += 1
        elif symbol == ")":
            count -= 1
        if count < 0:
            return False
    return count == 0


def get_first_operator(phrase):
    """
    Get first 'AND' or 'OR' substring
    """
    try:
        and_index = phrase.upper().index('AND')
    except ValueError:
        and_index = math.inf
    try:
        or_index = phrase.upper().index('OR')
    except ValueError:
        or_index = math.inf
    if and_index < or_index:
        return 'AND'
    else:
        return 'OR'


def check_valid_compare_operator(operator: str):
    """
    Check compare operator
    """
    compare_operators = ['eq', 'ne', 'gt', 'lt']
    if not operator in compare_operators:
        raise ValueError('Invalid operator {}'.format(operator))


def split_phrase(phrase, query=None):
    """
    Divided phrase into two expressions and make Django Q expressions
    """

    first_operator = get_first_operator(phrase)
    # divided phrase into two string using first operator
    divided_by_operator = re.split("and|AND|or|OR", phrase, maxsplit=1)
    phrase_divided_by_operator = [i.strip() for i in divided_by_operator]

    # if only one expression without 'and' or 'or'
    if len(phrase_divided_by_operator) != 2:
        expression = phrase_divided_by_operator[0].strip("(").strip(")")
        field, operator, value = expression.split(" ")
        check_valid_compare_operator(operator)
        expression_kwargs = {field + "__" + operator: value}
        query = Q(**expression_kwargs)
        return query

    # if we have two expressions
    expressions = []
    for expression in phrase_divided_by_operator:
        result = split_phrase(expression, query)
        expressions.append(result)

    # concatenate two expression using operator
    if first_operator == "AND":
        query = expressions[0] & expressions[1]
    elif first_operator == "OR":
        query = expressions[0] | expressions[1]
    return query


def parse_search_phrase(phrase):
    if is_correct_brackets(phrase):
        query = split_phrase(phrase)
    else:
        raise ValueError("Invalid search phrase. You should use correct brackets")
    return query
