'''
Requirement:
Input: 
  search string
Output:
  mongodb aggregation pipeline
Test Case:
1. A & B => {'$and': [{'title': {'$regex': re.compile("A")}}, {'title': {'$regex': re.compile("B")}}]}
2. A | B => {'$or': [{'title': {'$regex': re.compile("A")}}, {'title': {'$regex': re.compile("B")}}]}
3. A, B => {'$and': [{'title': {'$regex': re.compile("A")}}, {'title': {'$regex': re.compile("B")}}]}
4. A & (B | C) => {'$and': [{'title': {'$regex': re.compile("A")}},{'$or': [{'title': {'$regex': re.compile("B")}}, {'title': {'$regex': re.compile("C")}}]}]}
5. (A & B) | C => {'$or': [{'$and': [{'title': {'$regex': re.compile("A")}}, {'title': {'$regex': re.compile("B")}}]}, {'title': {'$regex': re.compile("C")}}]}
6. A & B | C => {'$or': [{'$and': [{'title': {'$regex': re.compile("A")}}, {'title': {'$regex': re.compile("B")}}]}, {'title': {'$regex': re.compile("C")}}]}
7. Abc & Bc => {'$and': [{'title': {'$regex': re.compile("Abc")}}, {'title': {'$regex': re.compile("Bc")}}]}
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
        return {'title': {'$regex': re.compile(expr, re.IGNORECASE)}}

def search_string_to_mongodb_pipeline(search_string):
    parsed_expr = parse_search_string(search_string)
    return build_mongodb_query(parsed_expr)

def test_search2mongodb_pipeline():
    test_cases = [
        ("A & B", {'$and': [{'title': {'$regex': re.compile('A', re.IGNORECASE)}}, {
        'title': {'$regex': re.compile('B', re.IGNORECASE)}}]}),
        ("A | B", {'$or': [{'title': {'$regex': re.compile('A', re.IGNORECASE)}}, {
        'title': {'$regex': re.compile('B', re.IGNORECASE)}}]}),
        ("A, B", {'$and': [{'title': {'$regex': re.compile('A', re.IGNORECASE)}}, {
        'title': {'$regex': re.compile('B', re.IGNORECASE)}}]}),
        ("A & (B | C)", {'$and': [{'title': {'$regex': re.compile('A', re.IGNORECASE)}}, {'$or': [{'title': {
        '$regex': re.compile('B', re.IGNORECASE)}}, {'title': {'$regex': re.compile('C', re.IGNORECASE)}}]}]}),
        ("(A & B) | C", {'$or': [{'$and': [{'title': {'$regex': re.compile('A', re.IGNORECASE)}}, {'title': {
        '$regex': re.compile('B', re.IGNORECASE)}}]}, {'title': {'$regex': re.compile('C', re.IGNORECASE)}}]}),
        ("A & B | C", {'$or': [{'$and': [{'title': {'$regex': re.compile('A', re.IGNORECASE)}}, {'title': {
        '$regex': re.compile('B', re.IGNORECASE)}}]}, {'title': {'$regex': re.compile('C', re.IGNORECASE)}}]}),
        ("Abc & Bc", {'$and': [{'title': {'$regex': re.compile('Abc', re.IGNORECASE)}}, {
        'title': {'$regex': re.compile('Bc', re.IGNORECASE)}}]}),
        ("A & B & C", {'$and': [{'title': {'$regex': re.compile('A', re.IGNORECASE)}}, {'title': {
        '$regex': re.compile('B', re.IGNORECASE)}}, {'title': {'$regex': re.compile('C', re.IGNORECASE)}}]}),
        ("A | B | C", {'$or': [{'title': {'$regex': re.compile('A', re.IGNORECASE)}}, {'title': {
        '$regex': re.compile('B', re.IGNORECASE)}}, {'title': {'$regex': re.compile('C', re.IGNORECASE)}}]}),
        ("(A & B) | (C & D)", {'$or': [{'$and': [{'title': {'$regex': re.compile('A', re.IGNORECASE)}}, {'title': {'$regex': re.compile('B', re.IGNORECASE)}}]}, {
        '$and': [{'title': {'$regex': re.compile('C', re.IGNORECASE)}}, {'title': {'$regex': re.compile('D', re.IGNORECASE)}}]}]}),
        ("A & (B | C) & D", {'$and': [{'title': {'$regex': re.compile('A', re.IGNORECASE)}}, {'$or': [{'title': {'$regex': re.compile(
            'B', re.IGNORECASE)}}, {'title': {'$regex': re.compile('C', re.IGNORECASE)}}]}, {'title': {'$regex': re.compile('D', re.IGNORECASE)}}]}),
        ("((A & B) | C) & D", {'$and': [{'$or': [{'$and': [{'title': {'$regex': re.compile('A', re.IGNORECASE)}}, {'title': {'$regex': re.compile(
            'B', re.IGNORECASE)}}]}, {'title': {'$regex': re.compile('C', re.IGNORECASE)}}]}, {'title': {'$regex': re.compile('D', re.IGNORECASE)}}]}),
        ("A & B & (C | D | E)", {'$and': [{'title': {'$regex': re.compile('A', re.IGNORECASE)}}, {'title': {'$regex': re.compile('B', re.IGNORECASE)}}, {'$or': [
        {'title': {'$regex': re.compile('C', re.IGNORECASE)}}, {'title': {'$regex': re.compile('D', re.IGNORECASE)}}, {'title': {'$regex': re.compile('E', re.IGNORECASE)}}]}]}),
        ("Apple iPhone & (12 Pro | 13 Pro)", {'$and': [{'title': {'$regex': re.compile('Apple iPhone', re.IGNORECASE)}}, {'$or': [
        {'title': {'$regex': re.compile('12 Pro', re.IGNORECASE)}}, {'title': {'$regex': re.compile('13 Pro', re.IGNORECASE)}}]}]}),
        ("Laptop & (Gaming | Business) & !Refurbished", {'$and': [{'title': {'$regex': re.compile('Laptop', re.IGNORECASE)}}, {'$or': [{'title': {'$regex': re.compile(
            'Gaming', re.IGNORECASE)}}, {'title': {'$regex': re.compile('Business', re.IGNORECASE)}}]}, {'title': {'$regex': re.compile('!Refurbished', re.IGNORECASE)}}]}),
        ("Camera & (DSLR | Mirrorless) & (Canon | Nikon | Sony)", {'$and': [{'title': {'$regex': re.compile('Camera', re.IGNORECASE)}}, {'$or': [{'title': {'$regex': re.compile('DSLR', re.IGNORECASE)}}, {'title': {'$regex': re.compile(
            'Mirrorless', re.IGNORECASE)}}]}, {'$or': [{'title': {'$regex': re.compile('Canon', re.IGNORECASE)}}, {'title': {'$regex': re.compile('Nikon', re.IGNORECASE)}}, {'title': {'$regex': re.compile('Sony', re.IGNORECASE)}}]}]}),
        ("Book & (Fiction | Non-fiction) & !eBook & (Hardcover | Paperback)", {'$and': [{'title': {'$regex': re.compile('Book', re.IGNORECASE)}}, {'$or': [{'title': {'$regex': re.compile('Fiction', re.IGNORECASE)}}, {'title': {'$regex': re.compile(
            'Non-fiction', re.IGNORECASE)}}]}, {'title': {'$regex': re.compile('!eBook', re.IGNORECASE)}}, {'$or': [{'title': {'$regex': re.compile('Hardcover', re.IGNORECASE)}}, {'title': {'$regex': re.compile('Paperback', re.IGNORECASE)}}]}]})
    ]
