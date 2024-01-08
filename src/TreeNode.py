from typing import List


class TreeNode:
    def __init__(self, hash: str, children: List["TreeNode"]):
        self.hash: str = hash
        self.children: List["TreeNode"] = children
        for child in self.children:
            child.parent = self
        self.parent: "TreeNode" = None

    def get_node_by_index(self, index: int) -> "TreeNode":
        # check whether the current object is a LeafNode and is the index we are looking for
        if hasattr(self, "index") and self.index == index:
            return self
        else:
            # for each child call the get_node_by_index method recursively
            for child in self.children:
                node = child.get_node_by_index(index)
                if node is not None:
                    return node
            return None

    def __str__(self):
        return f"TreeNode(hash={self.hash})"
