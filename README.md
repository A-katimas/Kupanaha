*This project has been created as part
of the 42 curriculum by jtardieu, fde-chec*


# 🧩 A-MAZE-ING

---

## 📖 Description

**A-MAZE-ING** is a terminal-based maze generator and solver written in Python.

The project combines:

* Procedural maze generation algorithms
* Real-time terminal rendering
* A shortest-path solver using **Breadth-First Search (BFS)**

The maze is displayed using ASCII graphics with dynamic colors and effects, allowing full interaction directly from the terminal.

---

## ⚙️ Instructions

### 📦 Installation

Requirements:

* Python 3.10+
* `uv` package manager

Install dependencies:

```bash
make install
```

---

### ▶️ Run the project

```bash
make run
```

With a configuration file:

```bash
make run CONFIG=config.txt
```

---

### 🛠 Available commands

| Command            | Description          |
| ------------------ | -------------------- |
| `make run`         | Run the maze         |
| `make install`     | Setup environment    |
| `make debug`       | Run with debugger    |
| `make clean`       | Remove cache & venv  |
| `make lint`        | Code linting         |
| `make lint-strict` | Strict type checking |

---

### 🎮 Controls

| Key | Action                  |
| --- | ----------------------- |
| `q` | Quit                    |
| `c` | Change theme            |
| `p` | Toggle perfect mode     |
| `b` | Generate (Backtracking) |
| `i` | Generate (Prim's)       |
| `l` | Show solver             |
| `h` | Hack effect             |
| `r` | Invert colors           |
| `o` | Otter mode              |

---

## 📚 Resources

### 🧠 Algorithms

* **Breadth-First Search (BFS)**
  Used for solving the maze and finding the shortest path.

* **Depth-First Search (Backtracking)**
  Used for maze generation (perfect maze).

* **Prim’s Algorithm (Randomized)**
  Alternative maze generation method.

---

### 🧱 Maze Representation

Each cell is encoded using a **bitmask**:

```
       N (1)
        ▲
W (8) ◄─┼─► E (2)
        ▼
       S (4)
```

* Each bit represents a wall
* Bitwise operations determine movement

---

## 📂 Additional Information

### 🏗 Project Structure

```
maze/
 ├── maker.py     # Maze generation -- jtardieu
 ├── solver.py    # BFS solver -- fde-chec

utils/
 ├── draw.py      # Rendering engine
 ├── wall.py      # Tiles system
 ├── color.py     # Terminal colors
```

---

### 🎨 Features

* 40+ visual themes
* Animated maze generation
* Real-time solver visualization
* Terminal-optimized rendering (diff-based updates)
* Fun effects (glitch, invert, emojis)

---

### 📁 Output Format

Generated mazes are saved as:

```
HEX GRID

entry_x,entry_y
exit_x,exit_y
```

* Hex values represent walls
* `F` = special/logo cells

---

### ⚠️ Notes

* Requires a sufficiently large terminal
* Performance optimized using partial redraw
* Uses Python generators for smooth animation

---

### 🔧 Configuration

The project relies on a `BaseConfig` object:

* Width / Height
* Entry / Exit positions
* Algorithm choice
* Theme
* Output file
* Random seed

---

## 👨‍💻 Author

Project built for algorithm practice and terminal rendering experimentation.

---

## 📜 License

MIT License
