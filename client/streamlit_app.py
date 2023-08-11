import streamlit as st
import os
import requests
from merkle_tree_lib.merkle_tree_utils import verify
from typing import Tuple, List
import streamlit as st
from sha3 import keccak_256

## functions

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
    url = BASE_URL + f'/data/{file.name}'
    response = requests.get(url=url)
    st.session_state[file.name] = response.json()

def verify_proof(root_hash,file_content, proof_items):
    # converting to tuples
    proof_items_as_tuples = []
    for proof in proof_items:
        hash, side_int = proof[0],proof[1]
        proof_items_as_tuples.append((hash, side_int))
    is_verified = verify(root_hash, file_content.decode(), proof_items_as_tuples, hash_function)
    st.session_state['proof_verified'] = str(is_verified)

## app

st.title('File storage powered by Merkle Tree')

# File upload -> display root_hash as text
uploaded_files = st.file_uploader("Upload files to storage", accept_multiple_files=True)
if uploaded_files:
    st.header('Files to upload')
    cols = st.columns(len(uploaded_files))
for index, uploaded_file in enumerate(uploaded_files):
    bytes_data = uploaded_file.read()
    cols[index].subheader(uploaded_file.name)
    cols[index].write(bytes_data)

st.divider()
col1,col2 = st.columns(2)
col1.button('Upload files', 
            on_click=upload_files,
            args=(uploaded_files,),
            disabled=not uploaded_files)
# Reset tree
if 'root_hash' in st.session_state:
    col1.write(f'Root hash {st.session_state["root_hash"]}')
col2.button('Reset tree', on_click=reset_tree)
# Get file -> display proof as text
col11, col22 = st.columns(2)

file_to_upload = col22.selectbox('Select an uploaded file', uploaded_files,
               format_func=lambda x: x.name)
col11.button('Retrieve file', on_click=get_file,
             args=(file_to_upload,),
             disabled=not file_to_upload)

# Verify proof -> display True
if file_to_upload:
    if file_to_upload.name not in st.session_state:
       proof = get_first_proof_from_storage_else_mock()
    else:
        proof = st.session_state[file_to_upload.name]['proof'][::]
    print ('proof', proof)
    if 'root_hash' in st.session_state:
        col11.button('Verify proof', on_click=verify_proof,
                args=(st.session_state['root_hash'],
                    file_to_upload.getvalue(),
                    proof),
                )
if 'proof_verified' in st.session_state:
    st.write(f'Proof verified {st.session_state["proof_verified"]}')

st.json(st.session_state)