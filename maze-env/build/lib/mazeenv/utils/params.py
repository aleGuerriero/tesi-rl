from __future__ import annotations

from typing import NamedTuple
from pathlib import Path

class Params(NamedTuple):
  #Experiment parameters
  n_episodes: int
  n_runs: int
  alpha: float
  gamma: float
  #File parameters
  savedf_folder: Path | None
  savefig_folder: Path | None
  maze_folder: Path