## Description of work

We implemented the following on a high-level using Python:
- Merkle tree lib (uploaded to PyPi), shared by both client and server
- Server (FastAPI server) that acts as file server and generates proofs from the Merkle Tree (built from the uploaded file contents)
    - We used memcached (https://memcached.org/) having decentralization in mind. It's basically a decentralized in-memory DB, allowing additional nodes to be added to the in-memory DB network. I also considered using Redis, but considering decentralization I opted for memcached.
- Client (Streamlit app) that uploads files, downloads files (with the corresponding proof) and verifies the proof
- Docker-compose orchestrating the whole setup

## If given more time:

I would have implemented the following if I had more time:

- Production-ready code: a few things can be rounded-up: more tests, formatting, documentation, etc.
- Make the application decentralized:
  - Make memcached running independent of server/client
  - Process of uploading files is not user-specific.
  - Process of uploading files can be optimized, currently there is one global Merkle Tree that is freshly built every time a user uploads new file(s).
- I would also like into ways of storing the Merkle tree. Right now we're simply storing the leafs (and the full tree) in a memory-DB (memcached). This can be optimized trivially (avoiding repetitive storage), but also more powerfully (for ex [link](https://ethresear.ch/t/optimizing-sparse-merkle-trees/3751/5)).


# Shortcomings

Currently the app (based on docker compose) entails a database (memcached), a server and a client, all running in the same machine. This has the drawback that it's a centralized system, hence the user would lose all his/her files if the system went down.

 For achieving a distributed system (as proposed in the challenge), we antecipate following changes:
    - Instead of docker-compose, Kubernetes should be employed for easier deployment across multiple machines (nodes)
    - The server interacts with one Merkle tree only. We would need to make the Merkle-Tree user-specific (one tree per user)
    - More nodes should be added to memcached (currently only 1). Additionally, memcached could either be independent of server and client (hence able to scale independently), or it should be possible to make every memcached node communicate with each other (e.g. each one is a node).
