from hashlib import blake2b
from pathlib import Path

import numpy as np
import typer
from ase.calculators.calculator import Calculator
from ase.io import iread


def main(xyz: Path) -> None:
    out_dir = xyz.parent.joinpath(xyz.stem)
    out_dir.mkdir(parents=True, exist_ok=True)
    for atoms in iread(xyz):
        k = atoms.get_chemical_formula("metal") + "_S"
        hb: bytes = atoms.positions.tobytes() + atoms.cell.array.tobytes()
        if isinstance(atoms.calc, Calculator):
            k += "2"
            for k0, v in {
                "E": "energy",
                "F": "forces",
                "S": "stress",
                "M": "magmoms",
                "Q": "charges",
            }.items():
                if v in atoms.calc.results.keys():
                    arr = atoms.calc.results[v]
                    if isinstance(arr, np.ndarray):
                        hb += arr.tobytes()
                    k += k0
        h = blake2b(hb, digest_size=5)
        fname = f"{k}_{h.hexdigest()}.xyz"
        atoms.write(out_dir / fname, "extxyz")


typer.run(main)
