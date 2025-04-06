from typing import List, Dict, Set, Optional
from collections import defaultdict

class InMemDB:
    def __init__(self, schema:Dict[str, str], keys: Set[str]):
        self.schema = schema
        self.keys_list = list(keys)
        self.table = defaultdict(dict)

    def insert(self, row: Dict[str, str]):
        key_value = []
        for key in self.keys_list:
            assert key in row
            key_value.append(row[key])
        key_tuple = tuple(key_value)
        for name,value in row.items():
            if name in self.keys_list:
                continue
            self.table[key_tuple][name] = value

    def check_clause(self, result: Dict[str,str], clause:str) -> bool: 
        if len(clause.split('<=')) == 2:
            col,right = clause.split('<=')
            col = col.strip()
            right = right.strip()
            return str(result[col]) <= right
        elif len(clause.split('==')) == 2:
            col,right = clause.split('==')
            col = col.strip()
            right = right.strip()
            return str(result[col]) == right
        elif len(clause.split('>=')) == 2:
            col,right = clause.split('>=')
            col = col.strip()
            right = right.strip()
            return str(result[col]) >= right
        elif len(clause.split('!=')) == 2:
            col,right = clause.split('!=')
            col = col.strip()
            right = right.strip()
            return str(result[col]) != right
        elif len(clause.split('>')) == 2:
            col,right = clause.split('>')
            col = col.strip()
            right = right.strip()
            return str(result[col]) > right
        elif len(clause.split('<')) == 2:
            col,right = clause.split('<')
            col = col.strip()
            right = right.strip()
            return str(result[col]) < right
        else:
            raise Exception
        return False
    
    def filter(self, result: Dict[str, str], where: Optional[List[str]])->bool:
        if where is None:
            return True
        for clause in where:
            if not self.check_clause(result, clause):
                return False
        return True

    def query(self, columns: List[str], where: Optional[List[str]] = None, order_by: Optional[str] = None) -> List[Dict[str, str]]:
        query_result = []
        for key, value in self.table.items():
            result = {self.keys_list[i]: key[i] for i in range(len(self.keys_list))}
            result.update(value)

            should_keep_result = self.filter(result, where)
            if not should_keep_result:
                continue

            selected_columns = list(result.keys())
            for key in selected_columns:
                if key not in columns:
                    del result[key]
            query_result.append(result)
        if order_by is not None:
            query_result.sort(key=lambda row: row[order_by])
        return query_result
            

def test_db():
    schema = {'id': 'str', 'name': 'str', 'score': 'int'}
    primary_keys = {'id'}
    db = InMemDB(schema, primary_keys)
    db.insert({'id': '001', 'name': 'A', 'score': 90})
    db.insert({'id': '002', 'name': 'B', 'score': 80})
    db.insert({'id': '003', 'name': 'C', 'score': 80})
    db.insert({'id': '004', 'name': 'D', 'score': 60})
    
    query_result = db.query({'id', 'name', 'score'})
    expected_result = [
        {'id': '001', 'name': 'A', 'score': 90},
        {'id': '002', 'name': 'B', 'score': 80},
        {'id': '003', 'name': 'C', 'score': 80},
        {'id': '004', 'name': 'D', 'score': 60}
    ]
    assert query_result == expected_result, f"{query_result} not equal {expected_result}"

    query_result = db.query({'id', 'name'})
    expected_result = [
        {'id': '001', 'name': 'A'},
        {'id': '002', 'name': 'B'},
        {'id': '003', 'name': 'C'},
        {'id': '004', 'name': 'D'}
    ]
    assert query_result == expected_result, f"{query_result} not equal {expected_result}"

    query_result = db.query({'id', 'name', 'score'}, ['id < 003', 'score > 70'], 'score')
    expected_result = [
        {'id': '002', 'name': 'B', 'score': 80},
        {'id': '001', 'name': 'A', 'score': 90},
    ]
    assert query_result == expected_result, f"{query_result} not equal {expected_result}"

    query_result = db.query({'id', 'name', 'score'}, ['id <= 003', 'score > 70'], 'score')
    expected_result = [
        {'id': '002', 'name': 'B', 'score': 80},
        {'id': '003', 'name': 'C', 'score': 80},
        {'id': '001', 'name': 'A', 'score': 90},
    ]
    assert query_result == expected_result, f"{query_result} not equal {expected_result}"

    query_result = db.query({'id', 'name', 'score'}, ['id <= 003', 'score > 70', 'score != 90'], 'score')
    expected_result = [
        {'id': '002', 'name': 'B', 'score': 80},
        {'id': '003', 'name': 'C', 'score': 80},
    ]
    assert query_result == expected_result, f"{query_result} not equal {expected_result}"

test_db()