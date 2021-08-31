# -*- coding: utf-8 -*-

__author__ = """Yngve Mardal Moe"""
__email__ = 'yngve.m.moe@gmail.com'
__version__ = '0.0.1'


from pathlib import Path
import sys

from git import Repo


class Journal:
    def __init__(self, directory):
        self.repo = Repo(directory)
    
    def log_experiment(self, name, hash_path):
        if len(self.repo.index.diff("HEAD")) != 0:
            raise ValueError("Staging area must be empty before running experiment")

        untracked_files = {untracked_file for untracked_file in self.repo.untracked_files}
        changed_files = {diff.a_path for diff in self.repo.index.diff(None)}
        
        if len(untracked_files) == 0 and len(changed_files) == 0:
            with open(hash_path, "w") as f:
                f.write(self.repo.head.commit.hexsha)
            return

        self.repo.index.add(untracked_files | changed_files)
        self.repo.index.commit(f"AUTOCOMMIT FOR EXPERIMENT: {name}")

        try:
            with open(hash_path, "w") as f:
                f.write(self.repo.head.commit.hexsha)
        except Exception as e:
            self.repo.head.reset("HEAD~")
            raise e
        else:
            self.repo.head.reset("HEAD~")
        
