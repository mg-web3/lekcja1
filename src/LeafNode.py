from TreeNode import TreeNode


class LeafNode(TreeNode):
    def __init__(self, data: str, hash: str, index: int):
        self.index: int = index
        self.data: str = data
        super().__init__(hash, [])

    def __str__(self):
        return f"LeafNode(index={self.index}, hash={self.hash}, data={self.data})"
