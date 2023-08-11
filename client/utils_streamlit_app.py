import os
import requests
#from merkle_tree_lib.merkle_tree_utils import verify
from merkle_tree_lib.constants import Side
from typing import Tuple, List
import streamlit as st
from sha3 import keccak_256

BASE_URL = os.environ['SERVER_BASE_URL']

def hash_function(a:str,b:str=''):
    return keccak_256(((a+b)).encode()).hexdigest()

def upload_files(uploaded_files):
    if uploaded_files:
        files = [('files', (file_object.name, file_object.getbuffer(), 'application/txt')) for file_object in uploaded_files]
        resp = requests.post(url=BASE_URL + '/upload', files=files)
        print ('resp', resp.json())
        st.session_state['root_hash'] = resp.json()['root_hash']
            
def get_first_proof_from_storage_else_mock():
    for key,value in st.session_state.items():
        if 'proof' in value:
            return value['proof']
    return [(hash_function('a',""),0),(hash_function('b',""),1)]

def reset_tree():
    url = BASE_URL + '/tree'
    response = requests.delete(url=url)
    return response.json()

def get_file(file):
    print ('entered get file')
    url = BASE_URL + f'/data/{file.name}'
    response = requests.get(url=url)
    st.session_state[file.name] = response.json()

def verify_proof(root_hash,file_content, proof_items):
    print (root_hash, file_content, proof_items)
    # converting to tuples
    proof_items_as_tuples = []
    for proof in proof_items:
        print ('proof', proof)
        hash, side_int = proof[0],proof[1]
        print ('proof2', hash, side_int)
        proof_items_as_tuples.append((hash, side_int))
    is_verified = verify(root_hash, file_content, proof_items_as_tuples, hash_function)
    st.session_state['proof_verified'] = str(is_verified)

def verify(root_hash: str, content: str, proof_items, hash_function):
    print ('entered verify, content', content)
    hash_to_verify = hash_function(content.decode(), "")
    print ('here')
    while proof_items:
        (next_hash, side) = proof_items.pop(0)
        print ('next_hash', next_hash, 'side', side)
        if side == Side.RIGHT.value:
            hash_to_verify = hash_function(hash_to_verify, next_hash)
        else:
            hash_to_verify = hash_function(next_hash, hash_to_verify)
    return hash_to_verify == root_hash