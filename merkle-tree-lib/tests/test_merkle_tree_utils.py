from merkle_tree_lib.merkle_tree_utils import verify

def hash_function(a:str,b:str=''):
    #return keccak_256((a+b).encode()).hexdigest()
    return (a+b)
def test_verify_4leafs():
    root_hash = 'abcd'
    hash_to_verify = 'a'
    proof_items = [('b',1),('cd',1)]
    assert verify(root_hash, hash_to_verify,  proof_items,hash_function)

def test_verify_2leafs():
    root_hash = 'ab'
    hash_to_verify = 'a'
    proof_items = [('b',1)]
    assert verify(root_hash, hash_to_verify,  proof_items,hash_function)

def test_verify_1leaf():
    root_hash = 'a'
    hash_to_verify = 'a'
    proof_items = []
    assert verify(root_hash, hash_to_verify,  proof_items,hash_function)

def test_verify_fails():
    root_hash = 'abcd'
    hash_to_verify = 'a'
    proof_items = [('b',1),('whatever',1)]
    assert verify(root_hash, hash_to_verify,  proof_items,hash_function) == False