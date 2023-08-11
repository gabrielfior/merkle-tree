# merkle-tree

## Getting started

```
cd /path/to/merkle-tree-repo
docker compose up --build --force-recreate --remove-orphans
```

Now navigate to
- `http://localhost:5000/docs` for the server endpoints specs
- `http://localhost:8501` for the client webpage

# Description of work

We implemented the following on a high-level using Python:
- Merkle tree lib (uploaded to PyPi), shared by both client and server
- Server (FastAPI server) that acts as file server and generates proofs from the Merkle Tree (built from the uploaded file contents)
- Client (Streamlit app) that uploads files, downloads files (with the corresponding proof) and verifies the proof
- Docker-compose orchestrating the whole setup

# If given more time:

## How to decentralize this
  - Make memcached running independent of server/client
  - Process of uploading files could be incremental and user-specific (i.e. one Merkle Tree per user) - currently there is one global Merkle Tree that is only built once and gets replaced if users uploads new files

# Shortcomings

You can use any programming language you want (we use Rust internally). We would like to see a solution with networking that can be deployed across multiple machines, and as close to production-ready as you have time for. Please describe the short-coming your solution have in a report, and how you would improve on them given more time.

We expect you to send us within 7 days:

a demo of your app that we can try (ideally using eg Docker Compose)
OK the code of the app
a report explaining your approach, your other ideas, what went well or not, etc..


