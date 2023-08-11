from pymemcache.client import base
from pymemcache import serde
from enum import Enum
import json
from merkle_tree_lib.merkle_tree import MerkleTree
from sha3 import keccak_256
import os

def hash_function(a:str,b:str):
    return keccak_256((a+b).encode()).hexdigest()

class MerkleTreeHandler:
    def __init__(self) -> None:
        self.client = base.Client('memcached:11211', serde=serde.pickle_serde, connect_timeout=10, timeout=10)
        self.update_merkle_tree()

    def upload_file(self, filename: str, file_contents: str):
        print ('filename', filename)
        self.client.set(filename, file_contents)
        self.update_merkle_tree_filenames(filename)
        self.update_merkle_tree()


    def update_merkle_tree_filenames(self, filename):
        filenames = self.client.get('merkle_tree_filenames')
        if not filenames:
            filenames = []
        filenames.append(filename)
        self.client.set('merkle_tree_filenames', filenames)

    def get_root_hash(self):
        tree = self.get_tree()
        root_index = tree.get_root_index()
        print ('leafs', tree.tree, root_index)
        return tree.tree[root_index]

    def get_file_contents(self, filepath):
        content = self.client.get(filepath)
        print ('content', content)
        if not content:
            return None
        return content.decode('utf8')

    def get_all_file_contents(self):
        filenames = self.client.get('merkle_tree_filenames')
        if not filenames:
            return []
        contents = [self.client.get(i).decode('utf8') for i in filenames]
        return contents

    def get_tree(self) -> MerkleTree:
        tree = self.client.get('merkle_tree')
        if not tree:
            return None
        return tree

    def reset_tree(self):
        self.client.delete('merkle_tree')
        self.client.delete('merkle_tree_filenames')

    def update_merkle_tree(self):
        # fetch leafs from file_contents
        contents = self.get_all_file_contents()
        # build tree
        if (contents):
            tree = MerkleTree(contents, hash_function)
            # update
            self.client.set('merkle_tree', tree)

    def generate_proof(self, filename):
        filenames = self.client.get('merkle_tree_filenames')
        print ('filenames', filenames, filename)
        if filename not in filenames:
            return "File not present in tree"
        index = filenames.index(filename)

        tree = self.get_tree()
        if not tree:
            return None
        print ('tree', tree, index)
        proof = tree.generate_proof(index)
        for i in proof:
            print ('proof i',i)
        elements = []
        for (proof_item_index, side) in proof:
            elements.append((tree.tree[proof_item_index], side))
        return elements

