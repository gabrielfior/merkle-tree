import streamlit as st
from utils_streamlit_app import *

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