'''
Requirement:
Input: 
  search string
Output:
  mongodb aggregation pipeline
Test Case:
1. A & B => {'$and': [{'dir_name': {'$regex': re.compile("A")}}, {'dir_name': {'$regex': re.compile("B")}}]}
2. A | B => {'$or': [{'dir_name': {'$regex': re.compile("A")}}, {'dir_name': {'$regex': re.compile("B")}}]}
3. A, B => {'$and': [{'dir_name': {'$regex': re.compile("A")}}, {'dir_name': {'$regex': re.compile("B")}}]}
4. A & (B | C) => {'$and': [{'dir_name': {'$regex': re.compile("A")}},{'$or': [{'dir_name': {'$regex': re.compile("B")}}, {'dir_name': {'$regex': re.compile("C")}}]}]}
5. (A & B) | C => {'$or': [{'$and': [{'dir_name': {'$regex': re.compile("A")}}, {'dir_name': {'$regex': re.compile("B")}}]}, {'dir_name': {'$regex': re.compile("C")}}]}
6. A & B | C => {'$or': [{'$and': [{'dir_name': {'$regex': re.compile("A")}}, {'dir_name': {'$regex': re.compile("B")}}]}, {'dir_name': {'$regex': re.compile("C")}}]}
7. Abc & Bc => {'$and': [{'dir_name': {'$regex': re.compile("Abc")}}, {'dir_name': {'$regex': re.compile("Bc")}}]}
'''
import re

def parse_search_string(search_string):
    def parse_expression(tokens, start=0):
        result = []
        current_term = ''
        i = start
        while i < len(tokens):
            if tokens[i] == '(':
                sub_expr, next_i = parse_expression(tokens, i + 1)
                result.append(sub_expr)
                i = next_i
            elif tokens[i] == ')':
                if current_term:
                    result.append(current_term)
                return result, i + 1
            elif tokens[i] in ['&', '|']:
                if current_term:
                    result.append(current_term)
                    current_term = ''
                result.append(tokens[i])
            else:
                current_term += tokens[i]
            i += 1
        if current_term:
            result.append(current_term)
        return result, i

    tokens = re.findall(r'\(|\)|&|\||[^()&|\s]+', search_string)
    parsed_expr, _ = parse_expression(tokens)
    return parsed_expr

def build_mongodb_query(expr):
    if isinstance(expr, list):
        if '|' in expr:
            or_exprs = []
            current_and = []
            for item in expr:
                if item == '|':
                    if current_and:
                        or_exprs.append(build_mongodb_query(current_and))
                        current_and = []
                else:
                    current_and.append(item)
            if current_and:
                or_exprs.append(build_mongodb_query(current_and))
            return {'$or': or_exprs}
        else:
            return {'$and': [build_mongodb_query(item) for item in expr if item != '&']}
    else:
        return {'dir_name': {'$regex': re.compile(expr, re.IGNORECASE)}}

def search_string_to_mongodb_pipeline(search_string):
    parsed_expr = parse_search_string(search_string)
    return build_mongodb_query(parsed_expr)

def test_search2mongodb_pipeline():
    test_cases = [
        ("A & B", {'$and': [{'dir_name': {'$regex': re.compile('A', re.IGNORECASE)}}, {
        'dir_name': {'$regex': re.compile('B', re.IGNORECASE)}}]}),
        ("A | B", {'$or': [{'dir_name': {'$regex': re.compile('A', re.IGNORECASE)}}, {
        'dir_name': {'$regex': re.compile('B', re.IGNORECASE)}}]}),
        ("A, B", {'$and': [{'dir_name': {'$regex': re.compile('A', re.IGNORECASE)}}, {
        'dir_name': {'$regex': re.compile('B', re.IGNORECASE)}}]}),
        ("A & (B | C)", {'$and': [{'dir_name': {'$regex': re.compile('A', re.IGNORECASE)}}, {'$or': [{'dir_name': {
        '$regex': re.compile('B', re.IGNORECASE)}}, {'dir_name': {'$regex': re.compile('C', re.IGNORECASE)}}]}]}),
        ("(A & B) | C", {'$or': [{'$and': [{'dir_name': {'$regex': re.compile('A', re.IGNORECASE)}}, {'dir_name': {
        '$regex': re.compile('B', re.IGNORECASE)}}]}, {'dir_name': {'$regex': re.compile('C', re.IGNORECASE)}}]}),
        ("A & B | C", {'$or': [{'$and': [{'dir_name': {'$regex': re.compile('A', re.IGNORECASE)}}, {'dir_name': {
        '$regex': re.compile('B', re.IGNORECASE)}}]}, {'dir_name': {'$regex': re.compile('C', re.IGNORECASE)}}]}),
        ("Abc & Bc", {'$and': [{'dir_name': {'$regex': re.compile('Abc', re.IGNORECASE)}}, {
        'dir_name': {'$regex': re.compile('Bc', re.IGNORECASE)}}]}),
        ("A & B & C", {'$and': [{'dir_name': {'$regex': re.compile('A', re.IGNORECASE)}}, {'dir_name': {
        '$regex': re.compile('B', re.IGNORECASE)}}, {'dir_name': {'$regex': re.compile('C', re.IGNORECASE)}}]}),
        ("A | B | C", {'$or': [{'dir_name': {'$regex': re.compile('A', re.IGNORECASE)}}, {'dir_name': {
        '$regex': re.compile('B', re.IGNORECASE)}}, {'dir_name': {'$regex': re.compile('C', re.IGNORECASE)}}]}),
        ("(A & B) | (C & D)", {'$or': [{'$and': [{'dir_name': {'$regex': re.compile('A', re.IGNORECASE)}}, {'dir_name': {'$regex': re.compile('B', re.IGNORECASE)}}]}, {
        '$and': [{'dir_name': {'$regex': re.compile('C', re.IGNORECASE)}}, {'dir_name': {'$regex': re.compile('D', re.IGNORECASE)}}]}]}),
        ("A & (B | C) & D", {'$and': [{'dir_name': {'$regex': re.compile('A', re.IGNORECASE)}}, {'$or': [{'dir_name': {'$regex': re.compile(
            'B', re.IGNORECASE)}}, {'dir_name': {'$regex': re.compile('C', re.IGNORECASE)}}]}, {'dir_name': {'$regex': re.compile('D', re.IGNORECASE)}}]}),
        ("((A & B) | C) & D", {'$and': [{'$or': [{'$and': [{'dir_name': {'$regex': re.compile('A', re.IGNORECASE)}}, {'dir_name': {'$regex': re.compile(
            'B', re.IGNORECASE)}}]}, {'dir_name': {'$regex': re.compile('C', re.IGNORECASE)}}]}, {'dir_name': {'$regex': re.compile('D', re.IGNORECASE)}}]}),
        ("A & B & (C | D | E)", {'$and': [{'dir_name': {'$regex': re.compile('A', re.IGNORECASE)}}, {'dir_name': {'$regex': re.compile('B', re.IGNORECASE)}}, {'$or': [
        {'dir_name': {'$regex': re.compile('C', re.IGNORECASE)}}, {'dir_name': {'$regex': re.compile('D', re.IGNORECASE)}}, {'dir_name': {'$regex': re.compile('E', re.IGNORECASE)}}]}]}),
        ("Apple iPhone & (12 Pro | 13 Pro)", {'$and': [{'dir_name': {'$regex': re.compile('Apple iPhone', re.IGNORECASE)}}, {'$or': [
        {'dir_name': {'$regex': re.compile('12 Pro', re.IGNORECASE)}}, {'dir_name': {'$regex': re.compile('13 Pro', re.IGNORECASE)}}]}]}),
        ("Laptop & (Gaming | Business) & !Refurbished", {'$and': [{'dir_name': {'$regex': re.compile('Laptop', re.IGNORECASE)}}, {'$or': [{'dir_name': {'$regex': re.compile(
            'Gaming', re.IGNORECASE)}}, {'dir_name': {'$regex': re.compile('Business', re.IGNORECASE)}}]}, {'dir_name': {'$regex': re.compile('!Refurbished', re.IGNORECASE)}}]}),
        ("Camera & (DSLR | Mirrorless) & (Canon | Nikon | Sony)", {'$and': [{'dir_name': {'$regex': re.compile('Camera', re.IGNORECASE)}}, {'$or': [{'dir_name': {'$regex': re.compile('DSLR', re.IGNORECASE)}}, {'dir_name': {'$regex': re.compile(
            'Mirrorless', re.IGNORECASE)}}]}, {'$or': [{'dir_name': {'$regex': re.compile('Canon', re.IGNORECASE)}}, {'dir_name': {'$regex': re.compile('Nikon', re.IGNORECASE)}}, {'dir_name': {'$regex': re.compile('Sony', re.IGNORECASE)}}]}]}),
        ("Book & (Fiction | Non-fiction) & !eBook & (Hardcover | Paperback)", {'$and': [{'dir_name': {'$regex': re.compile('Book', re.IGNORECASE)}}, {'$or': [{'dir_name': {'$regex': re.compile('Fiction', re.IGNORECASE)}}, {'dir_name': {'$regex': re.compile(
            'Non-fiction', re.IGNORECASE)}}]}, {'dir_name': {'$regex': re.compile('!eBook', re.IGNORECASE)}}, {'$or': [{'dir_name': {'$regex': re.compile('Hardcover', re.IGNORECASE)}}, {'dir_name': {'$regex': re.compile('Paperback', re.IGNORECASE)}}]}]})
    ]
