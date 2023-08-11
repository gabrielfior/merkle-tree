from merkle_tree_lib.merkle_tree import MerkleTree, Side
import pytest
from sha3 import keccak_256

leafs = ['a','b','c','d','e','f','g','h']

def hash_function(a:str,b:str):
    return keccak_256((a+b).encode()).hexdigest()

@pytest.fixture()
def merkle_tree():
    #hash_function = lambda a,b: a+b  
    return MerkleTree(leafs, hash_function)

def test_merkle_tree_raw_leafs_stored_correctly(merkle_tree):
    assert merkle_tree.raw_leafs == leafs

@pytest.mark.parametrize("input,expected", [(0, 1), (1, 0), (10, 11)])
def test_merkle_tree_symmetric(input, expected, merkle_tree):
    assert merkle_tree.get_symmetric(input) == expected

def test_merkle_tree_proof(merkle_tree):
    expected_proof = [(1, Side.RIGHT), (9, Side.RIGHT), (13,Side.RIGHT)]
    proof = merkle_tree.generate_proof(0)
    print('proof',proof)
    assert proof  == expected_proof

def test_merkle_tree_verify_proof(merkle_tree):
    index = 0
    proof = merkle_tree.generate_proof(index)
    print ('proof ',proof)
    is_valid = merkle_tree.verify(index, proof)
    assert is_valid == True