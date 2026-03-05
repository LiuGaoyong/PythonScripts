from pathlib import Path

import numpy as np
import typer
from ase.calculators.calculator import Calculator
from ase.io import iread


def main(xyz: Path, fmax: float = 50.0) -> None:
    new_xyz = xyz.with_suffix(f".F{int(fmax)}.xyz")
    with new_xyz.open("w") as f:
        for atoms in iread(xyz):
            if not isinstance(atoms.calc, Calculator):
                continue  # skip non SPE info
            if "forces" not in atoms.calc.results.keys():
                continue  # skip incomplete SPE info
            f: np.ndarray = atoms.calc.results["forces"]
            if np.max(np.linalg.norm(f, axis=1)) >= float(fmax):
                continue
            atoms.write(f, "extxyz")


typer.run(main)
