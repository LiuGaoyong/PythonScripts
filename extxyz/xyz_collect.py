from pathlib import Path

import typer
from ase.calculators.calculator import Calculator
from ase.io import iread

DICT = {
    "vasp": "OUTCAR",
}


def main(format: str = "vasp") -> None:
    with Path("dataset.xyz").open("w") as f:
        for p in Path(".").rglob(DICT[format]):
            for atoms in iread(p):
                if isinstance(atoms.calc, Calculator):
                    atoms.info["source"] = p.as_posix()
                    atoms.write(f, "extxyz")


typer.run(main)
