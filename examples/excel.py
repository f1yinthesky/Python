from typing import List, Tuple,Set
from collections import defaultdict
from queue import SimpleQueue

class Cell:
    def __init__(self):
        self.incoming_nodes = set()
        self.outgoing_nodes = set()
        self.const_value = None

class Sheet:
    def __init__(self):
        self.name_keyed_cells = defaultdict(Cell)

    def updateDownStream(self, cell:str) -> bool:
        visited_node = {node for node in self.name_keyed_cells[cell].incoming_nodes}
        node_queue = SimpleQueue()
        node_queue.put(cell)
        while not node_queue.empty():
            current_node = node_queue.get()
            #print(f"current_node: {current_node}")
            #print(f"visited node: {visited_node}")

            if current_node in visited_node:
                continue

            if len(self.name_keyed_cells[current_node].incoming_nodes) > 0:
                total_sum = 0
                is_ready = True
                for parent_node in self.name_keyed_cells[current_node].incoming_nodes:
                    if parent_node not in visited_node:
                        is_ready = False
                        break
                    #print(f"parent: {parent_node}")
                    total_sum += self.name_keyed_cells[parent_node].const_value
                if not is_ready:
                    continue
                self.name_keyed_cells[current_node].const_value = total_sum

            for child_node in self.name_keyed_cells[current_node].outgoing_nodes:
                if child_node in visited_node:
                    return False
                node_queue.put(child_node)

            visited_node.add(current_node)

        return True
    
    def setCell(self, cell:str, expression: str) -> bool:
        #print(f"\n sheet.setCell({cell}, {expression})")
        this_cell = self.name_keyed_cells[cell]
        if expression.isnumeric():
            this_cell.const_value = int(expression)
            for parent_node in this_cell.incoming_nodes:
                self.name_keyed_cells[parent_node].outgoing_nodes.remove(cell)
            this_cell.incoming_nodes.clear()
        else:
            parent_nodes = expression[1:].split('+')
            for parent_node in parent_nodes:
                self.name_keyed_cells[cell].incoming_nodes.add(parent_node)
                self.name_keyed_cells[parent_node].outgoing_nodes.add(cell)

        result = self.updateDownStream(cell)
        #for name, node in self.name_keyed_cells.items():
        #    print(f"{name}, {node.const_value}, {node.incoming_nodes}, {node.outgoing_nodes}")
        return result

    def getCell(self, cell:str) -> int:
        return self.name_keyed_cells[cell].const_value

def testSheet(operations: List[Tuple[str, List[str]]]):
    sheet = Sheet()
    for operation in operations:
        name, arg = operation
        if name == "setCell":
            input_arg = arg[0:len(arg) - 1]
            output_arg = True if arg[-1] == 'T' else False
            set_result = sheet.setCell(*input_arg)
            assert set_result == output_arg, f"sheet.setCell({input_arg}) is {set_result} vs {output_arg}"
        else:
            get_result = sheet.getCell(arg[0])
            assert str(get_result) == arg[1], f"sheet.getCell({arg[0]}) is {get_result} vs {arg[1]}"

operations = [
    ('setCell',['A0','1', 'T']),
    ('setCell',['A1','2', 'T']),
    ('getCell',['A0','1']),
    ('setCell',['B0','10', 'T']),
    ('getCell',['B0','10']),
    ('setCell',['B0','=A0+A1', 'T']),
    ('getCell',['B0','3']),
    ('setCell',['A1','=A0', 'T']),
    ('getCell',['B0','2']),
    ('setCell',['A0','10', 'T']),
    ('getCell',['B0','20']),
    ('setCell',['B0','8', 'T']),
    ('getCell',['B0','8']),
    ('setCell',['B0','=A0+A1', 'T']),
    ('setCell',['A0', '=B0', 'F']),
    ('setCell',['A0','9', 'T']),
    ('getCell',['B0','18']),
]

testSheet(operations)