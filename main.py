from pathlib import Path

from mazeb.models.maze import Maze

from mazeenv.utils.params import Params

from run_experiment import run_experiment

def_params = Params(
  n_episodes=2000,
  n_runs=10,
  obs_ranges=[5, 7, 9],
  alpha=0.8,
  gamma=0.99,
  savedf_folder=None,
  savefig_folder=None,
  maze_folder=None
)

def main():
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument(
    'maze',
    type=str
  )
  parser.add_argument(
    '-e', '--eps',
    nargs='+',
    type=float,
    required=False
  )

  args = parser.parse_args()

  eps = [1, 0.66, 0.5, 0.33, 0.0] if not args.eps else args.eps


  params = def_params._replace(maze_folder=Path(args.maze))
  maze_file = params.maze_folder / 'src' / f'{args.maze}.maze'
  maze = Maze.load(maze_file)

  params = params._replace(savedf_folder=params.maze_folder/'df')
  params.savedf_folder.mkdir(parents=True, exist_ok=True)

  params = params._replace(savefig_folder=params.maze_folder/'imgs')
  params.savefig_folder.mkdir(parents=True, exist_ok=True)

  for e in eps:
    res_all, st_all, states_all, actions_all, table_all = run_experiment(maze, e, params)
    res_all.to_csv(params.savedf_folder / f'res.{e}.csv')
    st_all.to_csv(params.savedf_folder / f'step.{e}.csv')
    states_all.to_csv(params.savedf_folder / f'states.{e}.csv')
    actions_all.to_csv(params.savedf_folder / f'actions.{e}.csv')
    table_all.to_csv(params.savedf_folder/ f'qtables.{e}.csv')

if __name__=='__main__':
  main()
    
  