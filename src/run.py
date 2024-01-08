from MerkleTree import MerkleTree

# our input data
data = ["hello", "world", "how", "are", "you"]

# tree construction
tree = MerkleTree(data)

# getting root and proofs for 2 sample leafs
root_hash = tree.get_root()
proof_0 = tree.get_proof(0)
proof_3 = tree.get_proof(3)

print("Root hash:", root_hash, "\n")
print("Proof for index 0:", proof_0)
print("Proof for index 3:", proof_3, "\n")

# proof verification
print("Verify proof for index 0:", MerkleTree.verify_proof(proof_0, root_hash, data[0]))
print("Verify proof for index 3:", MerkleTree.verify_proof(proof_3, root_hash, data[3]))

# proof manipulation
proof_0_modified = proof_0.copy()
proof_0_modified[0] = (proof_0_modified[0][0] + "a", proof_0_modified[0][1])

# manipulated proof verification
print(
    "Verify modified proof for index 0:",
    MerkleTree.verify_proof(proof_0_modified, root_hash, data[0]),
    "\n",
)

# tree printout
print("Tree:")
tree.print_tree()
