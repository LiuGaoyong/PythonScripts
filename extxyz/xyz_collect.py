#!/usr/bin/env python3
from pathlib import Path

import typer
from ase.calculators.calculator import Calculator
from ase.io import iread
from tqdm import tqdm

DICT = {
    "vasp": "OUTCAR",
}


def main(format: str = "vasp") -> None:
    with Path("dataset.xyz").open("w") as f:
        for p in tqdm(Path(".").rglob(f"*{DICT[format]}*")):
            for atoms in iread(p):
                if isinstance(atoms.calc, Calculator):
                    atoms.info["source"] = p.as_posix()
                    atoms.write(f, "extxyz")


typer.run(main)

