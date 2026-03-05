from pathlib import Path

import typer
from ase.calculators.calculator import Calculator
from ase.io import iread

DICT = {
    "E": "energy",
    "F": "forces",
    "S": "stress",
    "M": "magmoms",
    "Q": "charges",
}


def main(xyz: Path, keys: str = "EFS") -> None:
    new_xyz = xyz.with_suffix(f".filter-{keys}.xyz")
    dct = {k: DICT[k] for k in keys}
    with new_xyz.open("w") as f:
        for atoms in iread(xyz):
            if not isinstance(atoms.calc, Calculator):
                continue  # skip non SPE info
            if any(v not in atoms.calc.results.keys() for v in dct.values()):
                continue  # skip incomplete SPE info
            for k in list(
                k for k in atoms.calc.results.keys() if k not in dct.values()
            ):
                del atoms.calc.results[k]
            atoms.write(f, "extxyz")


typer.run(main)
