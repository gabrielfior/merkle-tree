from typing import List, Tuple, Callable, Optional
import math
from enum import Enum
from merkle_tree_lib.constants import Side

def is_power_of_2(number):
    return math.log2(number).is_integer()

class MerkleTree:
    def __init__(self, values:List[str], 
                 hash_function: Optional[Callable[[int,int],int]]):
        self.hash_function = hash_function
        self.raw_leafs = values
        self.leafs = [self.hash_function(i,"") for i in self.raw_leafs]
        self.build_tree()

    def __repr__(self) -> str:
        return str(self.raw_leafs)

    def build_tree(self):
        while not is_power_of_2(len(self.leafs)):
            # add "" until it becomes a full tree
            self.leafs.append("")

        self.tree = self.leafs[::] # deep copy
        nodes_to_process = self.tree[::]
        while len(nodes_to_process) > 1:
            left = nodes_to_process.pop(0)
            right = nodes_to_process.pop(0)
            new_hash = self.hash_function(left,right)
            self.tree.append(new_hash)
            nodes_to_process.append(new_hash)

    def generate_proof(self, index):
        root_index = self.get_root_index()
        target = index
        proof = []
        while target != root_index:
            symmetric = self.get_symmetric(target)
            side = Side.LEFT if symmetric < target else Side.RIGHT
            target = self.get_parent_index(target)
            # move to parent
            proof.append((symmetric,side))
        return proof

    def get_root_index(self):
        n = len(self.leafs)
        num_elements = 0
        n_levels = int(math.log2(n) + 1)
        for i in range(n_levels):
            new_elements = (n // 2**(i))
            num_elements += new_elements
        return num_elements - 1 #0-based indexing
        
    def verify(self, index: int, proof:List[Tuple[int, Side]]) -> bool:
        hash_to_verify = self.tree[index]
        while proof:
            (next_index, side) = proof.pop(0)
            if side == Side.RIGHT:
                hash_to_verify = self.hash_function(hash_to_verify, self.tree[next_index])
            else:
                hash_to_verify = self.hash_function(self.tree[next_index], hash_to_verify)     
        return hash_to_verify == self.tree[-1]
    
    def get_symmetric(self, index):
        # we get the other child of the parent
        if index % 2 == 0:
            return index + 1
        return index - 1
    
    def get_parent_index(self, index):
        if not self.tree:
            self.build_tree()

        # go to right node instead of left node
        if index % 2 == 0:
            index += 1

        delta = len(self.leafs) - 1 - (index//2)
        return index + delta
