#!/usr/bin/env python3
import random
from pathlib import Path

import typer
from ase import Atoms
from ase.io import iread


def main(xyz: Path, nselect: int = 10) -> None:
    new_xyz = xyz.with_suffix(f".select_{nselect}.xyz")
    atoms_lst: list[Atoms] = list(iread(xyz))
    with new_xyz.open("w") as f:  # type: ignore
        for atoms in random.sample(atoms_lst, nselect):
            atoms.write(f, "extxyz")  # type: ignore


typer.run(main)
