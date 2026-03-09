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
    #              DFTD3 from VASP5.4 (IVDW=12, PBE)
    d3_s6: float = 1.0000,  #  VDW_S6           =    1.0000
    d3_s8: float = 0.7875,  #  VDW_S8           =    0.7875
    d3_a1: float = 0.4289,  #  VDW_A1           =    0.4289
    d3_a2: float = 4.4407,  #  VDW_A2           =    4.4407
    d3_rc: float = 50.2022,  #  VDW_RADIUS      =   50.2022 A
    d3_cn: float = 21.1671,  #  VDW_CNRADIUS    =   21.1671 A
) -> None:
    new_xyz = xyz.with_suffix(f".dftd3_{d3_method}_{d3_damping}.xyz")
    with new_xyz.open("w") as f:  # type: ignore
        for atoms in tqdm(read(xyz, ":")):
            assert isinstance(atoms, Atoms)
            atoms.calc = DFTD3(
                method="PBE",
                damping="d3bj",
                s6=d3_s6,
                s8=d3_s8,
                a1=d3_a1,
                a2=d3_a2,
                disp2=d3_rc,
                cn=d3_cn,
            )
            atoms.get_potential_energy()
            atoms.write(f, "extxyz")  # type: ignore


typer.run(main)
