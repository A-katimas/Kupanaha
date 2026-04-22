# from pydantic import config

from maze.maker import Direction

# from utils.wall as wall
from parthing import BaseConfig

# from utils.color import bg_color
# from utils.cursor import cursor
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
    def __init__(self, maze: list[Any], config: BaseConfig):
        self.maze = maze
        self.config = config

    def solve_maze(self) -> list[tuple[int, int]]:
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
        path = []  # Liste finale qui contiendra le chemin solution
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

            for dir in Direction:  # Parcourt les quatre directions possibles
                cell = self.maze[x][
                    y
                ]  # valeur binaire de la cas actuelle(mur ou pas)
                dx, dy = (
                    dir.delta()
                )  # deplacement selon la direction (ex: 0,1 pour droite)
                nx, ny = x + dx, y + dy  # coordonnées de la case voisine
                if 0 <= nx < len(self.maze) and 0 <= ny < len(self.maze[0]):
                    if (nx, ny) not in visited:
                        if (
                            not cell & dir.value
                        ):  # verifie si le mur est fermé dans la direction
                            # actuelle
                            continue  # Si le mur est fermé, on ne peut pas
                        # aller dans cette direction
                        if (
                            cell & dir.value
                        ):  # verifie si le mur est ouvert dans
                            # la direction actuelle
                            visited.add(
                                (nx, ny)
                            )  # marque la case voisine comme visitée
                            # pour éviter de la revisiter
                            came_from[(nx, ny)] = (
                                x,
                                y,
                            )  # Ajouter à la file pour exploration future
                            queue.append(
                                (nx, ny)
                            )  # Ajouter la case voisine à la file d'attente
                            # pour l'explorer plus tard

        while step != self.config.ENTRY:
            if step not in came_from:
                break
            path.append(step)  # Ajouter la case actuelle au chemin
            step = came_from[step]  # Passer au parent de la case actuelle

        path.reverse()  # Inverser le chemin pour qu'il aille de l'entrée à
        # la sortie

        return path  # Retourner le chemin trouvé


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
