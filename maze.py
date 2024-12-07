from manimlib import *
import random

class MazeGenerator(Scene):
    def construct(self):
        # Maze configuration
        self.rows = 15
        self.cols = 15
        self.cell_size = 0.4
        
        # Initialize maze grid (True means wall exists)
        self.grid = [[True for _ in range(2 * self.cols + 1)] for _ in range(2 * self.rows + 1)]
        self.visited = set()
        
        # Generate maze using recursive backtracking
        self.generate_maze(1, 1)
        
        # Create entrance and exit
        self.grid[0][1] = False  # Top entrance
        self.grid[2 * self.rows][2 * self.cols - 1] = False  # Bottom exit
        
        # Draw the maze
        self.draw_maze()
        
        # Solve the maze
        self.solve_maze_animation()
        
        # Final pause
        self.wait(2)
    
    def generate_maze(self, row, col):
        self.visited.add((row, col))
        self.grid[row][col] = False
        
        # Define possible directions (right, down, left, up)
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        
        for dy, dx in directions:
            new_row, new_col = row + dy, col + dx
            if (0 < new_row < len(self.grid) - 1 and 
                0 < new_col < len(self.grid[0]) - 1 and 
                (new_row, new_col) not in self.visited):
                
                # Remove wall between cells
                self.grid[row + dy//2][col + dx//2] = False
                self.generate_maze(new_row, new_col)
    
    def draw_maze(self):
        maze = VGroup()
        
        # Draw walls
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j]:
                    wall = Square(
                        side_length=self.cell_size/2,
                        fill_color=WHITE,
                        fill_opacity=1,
                        stroke_width=0
                    )
                    wall.move_to(np.array([
                        j * self.cell_size/2 - self.cols * self.cell_size/2,
                        -i * self.cell_size/2 + self.rows * self.cell_size/2,
                        0
                    ]))
                    maze.add(wall)
        
        self.add(maze)
        self.maze = maze
    
    def solve_maze_animation(self):
        # Convert maze coordinates to path coordinates
        start = (1, 1)
        end = (2 * self.rows - 1, 2 * self.cols - 1)
        
        # Initialize path tracker
        self.path_tracker = VGroup()
        self.add(self.path_tracker)
        
        # Solve using DFS with animation
        visited = set()
        path = []
        self.dfs_animate(start, end, visited, path)
    
    def dfs_animate(self, current, end, visited, path):
        if current == end:
            return True
        
        if current in visited:
            return False
        
        visited.add(current)
        path.append(current)
        
        # Create yellow line to current position
        if len(path) > 1:
            prev_pos = self.cell_to_coords(path[-2])
            curr_pos = self.cell_to_coords(current)
            line = Line(
                start=prev_pos,
                end=curr_pos,
                color=YELLOW,
                stroke_width=3
            )
            self.play(ShowCreation(line), run_time=0.1)
            self.path_tracker.add(line)
        
        # Try all possible directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        
        for dy, dx in directions:
            new_row, new_col = current[0] + dy, current[1] + dx
            next_cell = (new_row + dy, new_col + dx)
            
            if (0 <= new_row < len(self.grid) and 
                0 <= new_col < len(self.grid[0]) and 
                not self.grid[new_row][new_col] and 
                next_cell not in visited):
                
                if self.dfs_animate(next_cell, end, visited, path):
                    return True
        
        # If dead end, backtrack
        path.pop()
        if len(path) > 0:
            prev_pos = self.cell_to_coords(path[-1])
            curr_pos = self.cell_to_coords(current)
            line = Line(
                start=curr_pos,
                end=prev_pos,
                color=RED,
                stroke_width=3
            )
            self.play(ShowCreation(line), run_time=0.05)
            self.path_tracker.add(line)
        
        return False
    
    def cell_to_coords(self, cell):
        row, col = cell
        return np.array([
            col * self.cell_size/2 - self.cols * self.cell_size/2,
            -row * self.cell_size/2 + self.rows * self.cell_size/2,
            0
        ])
