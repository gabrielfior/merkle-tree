from typing import List, Tuple,Callable, Optional
from merkle_tree_lib.constants import Side

def verify(root_hash: str, content: str, proof_items: List[Tuple[str, Side]],
           hash_function: Optional[Callable[[int,int],int]]):
    hash_to_verify = hash_function(content)
    while proof_items:
        (next_hash, side) = proof_items.pop(0)
        if side == Side.RIGHT.value:
            hash_to_verify = hash_function(hash_to_verify, next_hash)
        else:
            hash_to_verify = hash_function(next_hash, hash_to_verify)
    return hash_to_verify == root_hash