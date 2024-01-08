import hashlib
from LeafNode import LeafNode
from TreeNode import TreeNode
from typing import List, Tuple


class MerkleTree:
    @staticmethod
    def hash_string(data: str) -> str:
        # hash the input string using the sha256 algorithm
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    def print_tree(self):
        # print the tree level by level (from root to leaves)
        to_print = [self.root[1]]
        while len(to_print) != 0:
            print(f"{to_print[0]}")
            for child in to_print[0].children:
                to_print.append(child)
            to_print.pop(0)

    def __init__(self, data: List[str]):
        # construct a class instance
        self.data: List[str] = data
        self.root: Tuple[str, TreeNode] = self.build_tree()

    def build_tree(self) -> Tuple[str, TreeNode]:
        # convert data list to list of leaves
        leaves: List[LeafNode] = [
            LeafNode(data, self.hash_string(data), index)
            for index, data in enumerate(self.data)
        ]
        # build a tree from leaves
        root: TreeNode = self.build_tree_helper(leaves)
        return (root.hash, root)

    def build_tree_helper(self, nodes: List[TreeNode]) -> TreeNode:
        # build tree from leaves to the root

        # if there is only one node it means it's the root
        if len(nodes) == 1:
            return nodes[0]
        else:
            # build parents from combined children
            parent_nodes: List[TreeNode] = [
                # case for even number of children
                TreeNode(
                    self.combine_hash(nodes[i].hash, nodes[i + 1].hash),
                    [nodes[i], nodes[i + 1]],
                )
                if len(nodes) - 1 >= i + 1
                # case for uneven number of children
                else TreeNode(
                    self.combine_hash(nodes[i].hash, nodes[i].hash),
                    [nodes[i], nodes[i]],
                )
                for i in range(0, len(nodes), 2)
            ]
            # recurse up the tree structure to build next level
            return self.build_tree_helper(parent_nodes)

    @staticmethod
    def combine_hash(left: str, right: str) -> str:
        # concatenate both strings
        combined = left + right

        # hash  the resulting string
        return MerkleTree.hash_string(combined)

    def get_root(self) -> str:
        return self.root[0]

    def get_proof(self, index: int) -> List[Tuple[str, bool]]:
        # get the desired leaf node
        node = self.root[1].get_node_by_index(index)
        proof = []

        # traverse up the tree until root
        while node.parent is not None:
            # get node's sibling
            sibling = (
                node.parent.children[0]
                if node == node.parent.children[1]
                else node.parent.children[1]
            )

            # append the sibling's hash together with info on its position (left or right)
            proof.append((sibling.hash, node == node.parent.children[1]))

            # proceed up the tree
            node = node.parent
        return proof

    @staticmethod
    def verify_proof(proof: List[Tuple[str, bool]], root: str, data: str) -> bool:
        # start with hashing the data being checked for inclusion
        hash = MerkleTree.hash_string(data)

        # for each of the steps in the provided proof combine current hash with a hash from proof to generate parent hash (i.e. new current hash)
        for sibling_hash, is_right in proof:
            # make sure to combine the hashes in the correct order
            if is_right:
                hash = MerkleTree.combine_hash(sibling_hash, hash)
            else:
                hash = MerkleTree.combine_hash(hash, sibling_hash)

        # compare the computed root with the desired root and return check result
        return hash == root
