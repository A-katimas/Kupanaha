# from pydantic import config
from maze.maker import Direction
from parthing import BaseConfig
from typing import Any

# from utils.wall import Wall

###############################################################################
#                                                                             #
#                          MAZE SOLVER - ALGORITHME BFS                       #
#                                                                             #
#        Exploration par vagues successives pour garantir le chemin           #
#        le plus court à travers le labyrinthe.                               #
#                                                                             #
#        [Entrée] ●────► [ ] ────► [ ] ────► [ ]                              #
#                         │         │         │                               #
#                  [ ] ───┘  [ ] ───┘  [ ] ───┤                               #
#                   │         │         │     ▼                               #
#                  [ ] ────── [ ] ───── [ ] ──► [Sortie]                      #
#                                                                             #
###############################################################################


class Solver:
    """
    Solves a maze using the Breadth-First Search (BFS) algorithm.

    The solver explores the maze level by level, starting from the entry point.
    It keeps track of visited cells to avoid infinite loops, and records the
    parent of each visited cell in order to reconstruct the solution path once
    the exit is reached.

    Attributes:
        maze (list): A 2D grid where each cell contains a binary value
                     representing which walls are open or closed.
        config (BaseConfig): Configuration object containing the maze entry
                             point, exit point, and other settings.

    Methods:
        solve_maze(): Runs the BFS algorithm and returns the solution path
                      as a tuple (list of directions, list of coordinates),
                      or an empty list if no path exists.
    """
    def __init__(self, maze: list[Any], config: BaseConfig):
        self.maze = maze
        self.config = config

    def solve_maze(self) -> Any:
        """
        Explores the maze using BFS and reconstructs the solution path.

        Starting from the entry point, the algorithm explores all reachable cells
        level by level. For each cell, it checks the four possible directions and
        moves to a neighbor only if there is no wall blocking the way. Once the
        exit is reached, it reconstructs the path by backtracking through the
        came_from dictionary, then reverses it to get the correct order.

        Returns:
            tuple: A tuple (directions, path) where:
                - directions is a list of Direction values from entry to exit.
                - path is a list of (x, y) coordinates from entry to exit.
            list: An empty list if no path exists between entry and exit.
        """

        queue = [
            self.config.ENTRY
        ]  # File d'attente pour l'exploration (FIFO), commence par l'entrée
        visited = {
            self.config.ENTRY
        }  # Ensemble des cases déjà explorées pour éviter les boucles infinies
        came_from = (
            {}
        )  # came_from : Dictionnaire pour mémoriser le parent de chaque case
        # (clé=enfant, valeur=parent)
        path: list[tuple[int, int]] = []
        # Liste finale qui contiendra le chemin solution
        step = (
            self.config.EXIT
        )  # Variable de suivi pour la reconstruction du chemin

        while queue:
            current = queue.pop(
                0
            )  # Récupère la première case de la file d'attente pour l'explorer
            x, y = current
            if current == self.config.EXIT:
                break

            for dir in Direction:
                # Parcourt les quatre directions possibles
                cell = self.maze[x][y]
                # valeur binaire de la cas actuelle(mur ou pas)
                dx, dy = dir.delta()
                # deplacement selon la direction (ex: 0,1 pour droite)
                nx, ny = x + dx, y + dy  # coordonnées de la case voisine
                if 0 <= nx < len(self.maze) and 0 <= ny < len(self.maze[0]):
                    if (nx, ny) not in visited:
                        if cell & dir.value:
                            # verifie si le mur est fermé dans la direction
                            # actuelle
                            continue  # Si le mur est fermé, on ne peut pas
                        # aller dans cette direction
                        visited.add((nx, ny))
                        came_from[(nx, ny)] = (x, y)
                        queue.append((nx, ny))

        while step != self.config.ENTRY:
            if self.config.EXIT not in came_from:
                return []
            path.append(step)  # Ajouter la case actuelle au chemin
            step = came_from[step]  # Passer au parent de la case actuelle
        path.append(self.config.ENTRY)
        path.reverse()
        # Inverser le chemin pour qu'il aille de l'entrée à
        # la sortie

        result = self.tuple_to_dir(path)
        return (result, path)  # Retourner le chemin trouvé

    def tuple_to_dir(self, path: list[tuple[int, int]]) -> list[str]:
        """
        Convert a list of positions into movement directions.

        Args:
            path: List of (x, y) positions.

        Returns:
            A list of direction names corresponding to movements.
        """
        result: list[str] = []

        for i in range(len(path) - 1):
            dx = path[i + 1][0] - path[i][0]
            dy = path[i + 1][1] - path[i][1]

            for dir in Direction:
                name, delta = dir.to_char(), dir.delta()
                if (dx, dy) == delta:
                    result.append(name)
                    break

        return result


"""
    REPRÉSENTATION D'UNE CELLULE (Masquage Binaire)
    ----------------------------------------------
                   (NORD: 1)
                      ▲
    (OUEST: 8) ◄── [ CELL ] ──► (EST: 2)
                      ▼
                   (SUD: 4)

    Si (cell & Direction.NORD): le passage est OUVERT vers le haut.
"""
