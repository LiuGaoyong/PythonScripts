#!/usr/bin/env python3
from pathlib import Path

import typer
from ase import Atoms
from ase.io import read
from dftd3.ase import DFTD3
from tqdm import tqdm


def main(
    xyz: Path,
    d3_method: str = "PBE",
    d3_damping: str = "d3bj",
) -> None:
    new_xyz = xyz.with_suffix(f".dftd3_{d3_method}_{d3_damping}.xyz")
    with new_xyz.open("w") as f:  # type: ignore
        for atoms in tqdm(read(xyz, ":")):
            assert isinstance(atoms, Atoms)
            atoms.calc = DFTD3(method="PBE", damping="d3bj")
            atoms.get_potential_energy()
            atoms.write(f, "extxyz")  # type: ignore


typer.run(main)
