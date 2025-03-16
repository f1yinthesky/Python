from typing import Dict

class Node:
    id: int
    upper_node: "Node"

    def __init__(self, id: int):
        self.id = id
        self.upper_node = self

class UnionFind:
    node_map: Dict[int, Node]

    def __init__(self):
        self.node_map = {}

    def printUnionFind(self) -> None:
        for id, node in self.node_map.items():
            print(f"node id: {node.id} upper node id: {node.upper_node.id}")
        print("")

    def connectTwoNodes(self, left:int, right: int) -> None:
        left_label = self.getClusterLabelId(left, True)
        right_label = self.getClusterLabelId(right, True)
        if left_label == right_label:
            return
        if left_label < right_label:
            self.node_map[right_label].upper_node = self.node_map[left_label]
        else:
            self.node_map[left_label].upper_node = self.node_map[right_label]

    def isConnected(self, left:int, right: int) -> bool:
        left_label = self.getClusterLabelId(left)
        right_label = self.getClusterLabelId(right)
        return left_label == right_label

    def getClusterLabelId(self, id: int, create_node: bool = False) -> int:
        if id not in self.node_map:
            assert create_node
            self.node_map[id] = Node(id)
        chain_nodes = [self.node_map[id]]
        while chain_nodes[-1].upper_node != chain_nodes[-1]:
            chain_nodes.append(chain_nodes[-1].upper_node)

        for i in range(0, len(chain_nodes) - 1):
            chain_nodes[i].upper_node = chain_nodes[-1]
        return chain_nodes[-1].id

union_find = UnionFind()
union_find.printUnionFind()
union_find.connectTwoNodes(1,2)
union_find.printUnionFind()
union_find.connectTwoNodes(3,2)
union_find.printUnionFind()
union_find.connectTwoNodes(4,5)
union_find.printUnionFind()
union_find.connectTwoNodes(3,5)
union_find.printUnionFind()

assert union_find.isConnected(1, 5)
union_find.printUnionFind()
assert union_find.isConnected(1, 3)
union_find.printUnionFind()
