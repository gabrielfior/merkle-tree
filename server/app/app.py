from typing import List
from fastapi import FastAPI, File, UploadFile
from app.merkle_tree_handler import MerkleTreeHandler

app = FastAPI()
merkle_tree_handler = MerkleTreeHandler()

@app.get("/data/{filename}")
async def get_file(filename: str):
    contents = merkle_tree_handler.get_file_contents(filename)
    print ('contents', contents)

    proof = merkle_tree_handler.generate_proof(filename)
    return {"contents":contents, "proof":proof}

@app.delete('/tree')
def delete_tree():
    merkle_tree_handler.reset_tree()

@app.get("/tree")
def tree():
    return merkle_tree_handler.get_tree()

@app.post("/upload")
def upload(files: List[UploadFile] = File(...)):
    for file in files:
        data = file.file.read()
        merkle_tree_handler.upload_file(file.filename, data)
    root_hash = merkle_tree_handler.get_root_hash()
    return {"message": f"Successfuly uploaded {[file.filename for file in files]}",
            "root_hash": root_hash}
