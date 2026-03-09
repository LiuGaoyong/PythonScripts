#!/usr/bin/env python3
from pathlib import Path

import numpy as np
import typer
from ase.calculators.calculator import Calculator
from ase.io import iread
from tqdm import tqdm


def main(xyz: Path, fmax: float = 50.0) -> None:
    new_xyz = xyz.with_suffix(f".F{int(fmax)}.xyz")
    with new_xyz.open("w") as f:
        for atoms in tqdm(iread(xyz)):
            if not isinstance(atoms.calc, Calculator):
                continue  # skip non SPE info
            if "forces" not in atoms.calc.results.keys():
                continue  # skip incomplete SPE info
            forces: np.ndarray = atoms.calc.results["forces"]
            if np.max(np.linalg.norm(forces, axis=1)) >= float(fmax):
                continue
            atoms.write(f, "extxyz")


typer.run(main)
