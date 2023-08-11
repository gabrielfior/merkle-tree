## Description of work

We implemented the following on a high-level using Python:
- Merkle tree lib (uploaded to PyPi), shared by both client and server
- Server (FastAPI server) that acts as file server and generates proofs from the Merkle Tree (built from the uploaded file contents)
- Client (Streamlit app) that uploads files, downloads files (with the corresponding proof) and verifies the proof
- Docker-compose orchestrating the whole setup

## If given more time:

- Production-ready code: a few things can be rounded-up: more tests, formatting, documentation, etc.
- Make the application decentralized:
  - Make memcached running independent of server/client
  - Process of uploading files is not user-specific.
  - Process of uploading files can be optimized, currently there is one global Merkle Tree that is freshly built every time a user uploads new file(s).
- I would also like into ways of storing the Merkle tree. Right now we're simply storing the leafs (and the full tree) in a memory-DB (memcached). This can be optimized trivially (avoiding repetitive storage), but also more powerfully (for ex [link](https://ethresear.ch/t/optimizing-sparse-merkle-trees/3751/5)).
