from manimlib import *
import random
import numpy as np

class TetrisAnimation(Scene):
    def construct(self):
        self.GRID_WIDTH = 10
        self.GRID_HEIGHT = 20
        self.BLOCK_SIZE = 0.3
        
        # Initialize empty grid with proper dimensions
        self.grid = np.zeros((self.GRID_HEIGHT, self.GRID_WIDTH))
        
        # Create game board
        self.board = VGroup()
        for y in range(self.GRID_HEIGHT):
            for x in range(self.GRID_WIDTH):
                square = Square(
                    side_length=self.BLOCK_SIZE,
                    stroke_width=1,
                    stroke_color=GREY,
                    fill_opacity=0
                )
                square.move_to(
                    RIGHT * x * self.BLOCK_SIZE +
                    DOWN * y * self.BLOCK_SIZE
                )
                self.board.add(square)
        
        self.board.center()
        self.placed_blocks = VGroup()

        # Define Tetris pieces
        self.PIECES = {
            'I': [(0,0), (0,1), (0,2), (0,3)],
            'O': [(0,0), (0,1), (1,0), (1,1)],
            'T': [(0,1), (1,0), (1,1), (1,2)],
            'L': [(0,2), (1,0), (1,1), (1,2)]
        }
        
        self.COLORS = {
            'I': BLUE,
            'O': YELLOW,
            'T': PURPLE,
            'L': ORANGE
        }

        # Define rotation states for each piece
        self.ROTATIONS = {
            'I': [
                [(0,0), (0,1), (0,2), (0,3)],
                [(0,0), (1,0), (2,0), (3,0)]
            ],
            'O': [
                [(0,0), (0,1), (1,0), (1,1)]
            ],
            'T': [
                [(0,1), (1,0), (1,1), (1,2)],
                [(0,1), (1,1), (1,2), (2,1)],
                [(1,0), (1,1), (1,2), (2,1)],
                [(0,1), (1,0), (1,1), (2,1)]
            ],
            'L': [
                [(0,2), (1,0), (1,1), (1,2)],
                [(0,1), (1,1), (2,1), (2,2)],
                [(1,0), (1,1), (1,2), (2,0)],
                [(0,0), (0,1), (1,1), (2,1)]
            ]
        }

        self.score = 0
        # Create simpler scoreboard text
        self.scoreboard = Text(
            f"SCORE: {self.score}",
            color=WHITE,
            weight=BOLD  # Make it bold instead of using complex animations
        ).scale(0.8)
        
        self.scoreboard.next_to(self.board, UP, buff=0.5)
        
        # Add both without complex animation
        self.add(self.board, self.scoreboard)

        # Create preview box with adjusted position and width
        preview_box = Rectangle(
            height=6,  # Height for 3 pieces
            width=3,   # Changed from 4 to 3 (25% reduction)
            color=WHITE,
            stroke_width=2
        ).shift(RIGHT * (self.GRID_WIDTH/2 + 0.01))
        
        # Add "NEXT" text above preview box
        next_text = Text("NEXT", color=WHITE).scale(0.5)
        next_text.next_to(preview_box, UP, buff=0.3)
        
        self.add(preview_box, next_text)
        
        # Initialize preview pieces with adjusted positions
        self.preview_pieces = []
        self.preview_positions = [
            preview_box.get_center() + UP * 2,    # Top piece
            preview_box.get_center(),             # Middle piece
            preview_box.get_center() + DOWN * 2   # Bottom piece
        ]
        
        # Initialize queue of next pieces
        self.piece_queue = [random.choice(list(self.PIECES.keys())) for _ in range(3)]
        self.update_preview()

        self.play_round()  # Just play one round at normal speed

    def update_preview(self):
        """Optimized preview update"""
        if hasattr(self, 'preview_pieces'):
            self.remove(*self.preview_pieces)
        self.preview_pieces = []
        
        # Create all preview pieces at once
        preview_group = VGroup()
        for i, piece_type in enumerate(self.piece_queue):
            preview_piece = self.create_piece(piece_type, 0, 0)
            preview_piece.scale(0.7)
            preview_piece.move_to(self.preview_positions[i])
            preview_group.add(preview_piece)
            self.preview_pieces.append(preview_piece)
        
        self.add(preview_group)

    def play_round(self):
        """Optimized play round with proper exit handling"""
        running = True
        
        try:
            while running:
                try:
                    piece_type = self.piece_queue.pop(0)
                    self.piece_queue.append(random.choice(list(self.PIECES.keys())))
                    
                    if len(self.preview_pieces) > 0:
                        self.remove(*self.preview_pieces)
                    self.update_preview()
                    
                    if self.check_board_height():
                        self.reset_top_portion()
                    
                    best_x, best_rotation = self.find_best_move(piece_type)
                    piece = self.create_piece(piece_type, best_x, best_rotation)
                    
                    if self.check_collision(piece):
                        self.reset_top_portion()
                        continue
                    
                    self.add(piece)
                    landing_height = self.find_landing_height(piece)
                    
                    try:
                        self.play(
                            piece.animate.shift(DOWN * landing_height * self.BLOCK_SIZE),
                            run_time=0.05
                        )
                    except Exception:
                        # If play fails, assume window was closed
                        running = False
                        break
                    
                    if not self.place_piece(piece):
                        self.reset_top_portion()
                        continue
                    
                    self.check_lines()
                    
                    try:
                        self.wait(0.02)
                    except Exception:
                        # If wait fails, assume window was closed
                        running = False
                        break
                    
                except Exception as e:
                    if "window" in str(e).lower() or "renderer" in str(e).lower():
                        running = False
                        break
                    print(f"Recovered from error: {e}")
                    self.reset_top_portion()
                    continue
        except KeyboardInterrupt:
            print("Animation stopped by user")
        finally:
            # Clean up resources
            try:
                if hasattr(self, 'preview_pieces'):
                    for piece in self.preview_pieces:
                        self.remove(piece)
                if hasattr(self, 'placed_blocks'):
                    self.remove(self.placed_blocks)
            except Exception:
                pass  # Ignore cleanup errors

    def check_board_height(self):
        """Check if the board is getting too high"""
        # Count filled cells in top 6 rows
        top_rows = self.grid[:6]
        filled_count = np.sum(top_rows)
        return filled_count > (6 * self.GRID_WIDTH * 0.4)  # Increased threshold to 40%

    def reset_top_portion(self):
        """Optimized board reset"""
        clear_height = self.GRID_HEIGHT // 2
        
        # Update grid in one operation
        self.grid = np.vstack([
            np.zeros((clear_height, self.GRID_WIDTH)),
            self.grid[clear_height:]
        ])
        
        # Batch remove blocks more efficiently
        blocks_to_remove = [block for block in self.placed_blocks 
                          if self.get_grid_position(block)[0] < clear_height]
        
        if blocks_to_remove:
            self.remove(*blocks_to_remove)
            for block in blocks_to_remove:
                self.placed_blocks.remove(block)

    def create_piece(self, piece_type, x_pos=3, rotation_index=0):
        shape = self.ROTATIONS[piece_type][rotation_index]
        color = self.COLORS[piece_type]
        
        piece = VGroup()
        for rel_y, rel_x in shape:
            square = Square(
                side_length=self.BLOCK_SIZE,
                fill_color=color,
                fill_opacity=1,
                stroke_width=1,
                stroke_color=WHITE
            ).set_fill(color, opacity=1)
            
            square.move_to(
                self.board.get_corner(UL) +
                RIGHT * ((rel_x + x_pos) * self.BLOCK_SIZE + self.BLOCK_SIZE/2) +
                DOWN * (rel_y * self.BLOCK_SIZE + self.BLOCK_SIZE/2)
            )
            piece.add(square)
        return piece

    def get_grid_position(self, square):
        rel_pos = square.get_center() - self.board.get_corner(UL)
        grid_x = int(round((rel_pos[0] / self.BLOCK_SIZE) - 0.5))
        grid_y = int(round((rel_pos[1] / self.BLOCK_SIZE * -1) - 0.5))
        return (grid_y, grid_x)

    def check_collision(self, piece):
        """Strict collision detection"""
        for square in piece:
            pos = self.get_grid_position(square)
            # Check grid boundaries
            if not (0 <= pos[0] < self.GRID_HEIGHT and 0 <= pos[1] < self.GRID_WIDTH):
                return True
            # Check collision with existing blocks
            if self.grid[pos[0]][pos[1]] == 1:
                return True
        return False

    def find_landing_height(self, piece):
        """More accurate landing height calculation"""
        max_height = self.GRID_HEIGHT
        test_piece = piece.copy()
        
        for height in range(max_height):
            test_piece.shift(DOWN * self.BLOCK_SIZE)
            if self.check_collision(test_piece):
                test_piece.shift(UP * self.BLOCK_SIZE)
                return height
        
        return max_height

    def place_piece(self, piece):
        """Reliable piece placement"""
        # Verify final position is valid
        if self.check_collision(piece):
            return False
        
        # Update grid
        for square in piece:
            pos = self.get_grid_position(square)
            if 0 <= pos[0] < self.GRID_HEIGHT and 0 <= pos[1] < self.GRID_WIDTH:
                self.grid[pos[0]][pos[1]] = 1
            else:
                return False
        
        # Add to placed blocks
        self.placed_blocks.add(*piece)
        return True

    def check_lines(self):
        """Optimized line clearing"""
        lines_to_clear = []
        for y in range(self.GRID_HEIGHT):
            if np.all(self.grid[y]):
                lines_to_clear.append(y)
        
        if lines_to_clear:
            self.score += len(lines_to_clear) * 100
            
            # Update scoreboard more efficiently
            new_score_text = Text(
                f"SCORE: {self.score}",
                color=WHITE,
                weight=BOLD
            ).scale(0.8).move_to(self.scoreboard.get_center())
            self.remove(self.scoreboard)
            self.scoreboard = new_score_text
            self.add(self.scoreboard)
            
            # Process lines more efficiently
            blocks_to_remove = []
            blocks_to_move = {}
            
            for line in lines_to_clear:
                for block in self.placed_blocks:
                    pos = self.get_grid_position(block)
                    if pos[0] == line:
                        blocks_to_remove.append(block)
                    elif pos[0] < line:
                        blocks_to_move[block] = blocks_to_move.get(block, 0) + 1
            
            # Update grid efficiently
            new_grid = np.zeros_like(self.grid)
            current_row = self.GRID_HEIGHT - 1
            for y in range(self.GRID_HEIGHT - 1, -1, -1):
                if y not in lines_to_clear:
                    new_grid[current_row] = self.grid[y]
                    current_row -= 1
            self.grid = new_grid
            
            # Remove blocks without animation for better performance
            if blocks_to_remove:
                self.remove(*blocks_to_remove)
                for block in blocks_to_remove:
                    self.placed_blocks.remove(block)
            
            # Move remaining blocks
            if blocks_to_move:
                for block, distance in blocks_to_move.items():
                    block.shift(DOWN * distance * self.BLOCK_SIZE)
            
            # Small delay for visual feedback
            self.wait(0.02)

    def try_rotation(self, piece, piece_type, current_x, current_rotation_index):
        next_rotation = (current_rotation_index + 1) % len(self.ROTATIONS[piece_type])
        new_piece = self.create_piece(piece_type, current_x, next_rotation)
        
        # Check if rotation is possible
        if not self.check_collision(new_piece):
            return new_piece, next_rotation
        
        # Try wall kicks (shift left or right if rotation is blocked)
        for x_offset in [-1, 1, -2, 2]:
            test_piece = self.create_piece(piece_type, current_x + x_offset, next_rotation)
            if not self.check_collision(test_piece):
                return test_piece, next_rotation
        
        return piece, current_rotation_index

    def evaluate_position(self, piece_type, x_pos, rotation_index):
        test_piece = self.create_piece(piece_type, x_pos, rotation_index)
        if self.check_collision(test_piece):
            return -float('inf')
        
        drop_height = self.find_landing_height(test_piece)
        filled_positions = []
        for square in test_piece:
            pos = self.get_grid_position(square)
            new_y = pos[0] + drop_height
            new_x = pos[1]
            if 0 <= new_y < self.GRID_HEIGHT and 0 <= new_x < self.GRID_WIDTH:
                filled_positions.append((new_y, new_x))
        
        if not filled_positions:
            return -float('inf')
        
        score = 0
        
        # Prioritize bottom-up filling
        max_height = max(self.GRID_HEIGHT - y for y, _ in filled_positions)
        score -= max_height * 100  # Penalize height
        
        # Check for complete lines
        rows_affected = set(y for y, x in filled_positions)
        complete_lines = 0
        for row in rows_affected:
            temp_row = list(self.grid[row])
            for _, x in [pos for pos in filled_positions if pos[0] == row]:
                temp_row[x] = 1
            if all(temp_row):
                complete_lines += 1
                score += 10000  # High bonus for completing lines
        
        # Penalize holes heavily
        holes = self.count_holes(filled_positions)
        score -= holes * 5000
        
        # Encourage piece connections
        connections = self.count_connections(filled_positions)
        score += connections * 100
        
        # Penalize unevenness
        heights = self.get_column_heights(filled_positions)
        height_diff = self.calculate_height_differences(heights)
        score -= height_diff * 50
        
        return score

    def evaluate_t_spin_opportunity(self, x, rotation, positions):
        """Evaluate potential T-spin setups"""
        score = 0
        if len(positions) == 4:  # T piece has 4 blocks
            corners = 0
            for dy, dx in [(1,1), (1,-1), (-1,1), (-1,-1)]:
                new_x = x + dx
                if 0 <= new_x < self.GRID_WIDTH:
                    if self.grid[positions[0][0] + dy][new_x] == 1:
                        corners += 1
            if corners >= 2:
                score += corners * 2
        return score

    def evaluate_well_placement(self, positions):
        """Enhanced well evaluation"""
        score = 0
        well_positions = set()
        
        # Find potential well columns
        for x in range(self.GRID_WIDTH):
            consecutive_empty = 0
            for y in range(self.GRID_HEIGHT-1, -1, -1):
                if (y, x) not in positions and self.grid[y][x] == 0:
                    consecutive_empty += 1
                    well_positions.add((y, x))
                else:
                    break
            
            # Score based on well depth and position
            if consecutive_empty >= 3:
                multiplier = 1
                if x == 0 or x == self.GRID_WIDTH-1:  # Prefer edge wells
                    multiplier = 2
                score += consecutive_empty * multiplier * 100
        
        return score

    def is_edge_safe(self, positions):
        """Ensure edges are well-maintained"""
        heights = self.get_column_heights(positions)
        
        # Check if edges are lower than center
        edge_safe = True
        center_height = max(heights[2:-2])  # Height of center columns
        
        # Edges should be at most 2 blocks higher than center
        if heights[0] > center_height + 2 or heights[-1] > center_height + 2:
            edge_safe = False
        
        return edge_safe

    def check_need_reset(self):
        """Ultra-conservative reset checking"""
        # Check multiple danger signs
        top_sixth = self.grid[:self.GRID_HEIGHT // 6]
        filled_cells = np.sum(top_sixth)
        danger_threshold = (self.GRID_WIDTH * (self.GRID_HEIGHT // 6)) * 0.3  # Lowered to 30%
        
        # Also check for uneven stack
        heights = [0] * self.GRID_WIDTH
        for x in range(self.GRID_WIDTH):
            for y in range(self.GRID_HEIGHT):
                if self.grid[y][x] == 1:
                    heights[x] = self.GRID_HEIGHT - y
                    break
        
        max_height_diff = max(abs(heights[i] - heights[i+1]) for i in range(len(heights)-1))
        
        return filled_cells > danger_threshold or max_height_diff > 4

    def count_holes(self, new_positions):
        """Enhanced hole detection"""
        holes = 0
        temp_grid = self.grid.copy()
        
        # Add new piece positions to temporary grid
        for y, x in new_positions:
            if 0 <= y < self.GRID_HEIGHT and 0 <= x < self.GRID_WIDTH:
                temp_grid[y][x] = 1
        
        # Count holes (empty cells with filled cells above them)
        for x in range(self.GRID_WIDTH):
            found_block = False
            for y in range(self.GRID_HEIGHT):
                if temp_grid[y][x] == 1:
                    found_block = True
                elif found_block and temp_grid[y][x] == 0:
                    holes += 1
        
        return holes

    def count_connections(self, filled_positions):
        connections = 0
        for y, x in filled_positions:
            # Check adjacent cells
            for dy, dx in [(0,1), (0,-1), (1,0), (-1,0)]:
                new_y, new_x = y + dy, x + dx
                if (0 <= new_y < self.GRID_HEIGHT and 
                    0 <= new_x < self.GRID_WIDTH and 
                    self.grid[new_y][new_x] == 1):
                    connections += 1
        return connections

    def check_game_over(self):
        # Check if any blocks in top row
        return np.any(self.grid[0]) or np.any(self.grid[1])

    def calculate_well_bonus(self, filled_positions):
        """Encourage creating and maintaining wells for long pieces"""
        bonus = 0
        column_heights = [0] * self.GRID_WIDTH
        
        # Calculate current column heights
        for y in range(self.GRID_HEIGHT):
            for x in range(self.GRID_WIDTH):
                if self.grid[y][x] == 1:
                    column_heights[x] = max(column_heights[x], self.GRID_HEIGHT - y)
        
        # Update with new piece
        for y, x in filled_positions:
            column_heights[x] = max(column_heights[x], self.GRID_HEIGHT - y)
        
        # Check for wells (gaps between higher columns)
        for x in range(self.GRID_WIDTH):
            if x > 0 and x < self.GRID_WIDTH - 1:
                if (column_heights[x] + 3 < column_heights[x-1] and 
                    column_heights[x] + 3 < column_heights[x+1]):
                    bonus += 500  # Bonus for maintaining wells for long pieces
        
        return bonus

    def get_column_heights(self, filled_positions):
        heights = [0] * self.GRID_WIDTH
        for y, x in filled_positions:
            heights[x] = max(heights[x], self.GRID_HEIGHT - y)
        return heights

    def calculate_height_differences(self, heights):
        total_diff = 0
        for i in range(len(heights) - 1):
            total_diff += abs(heights[i] - heights[i + 1])
        return total_diff

    def find_best_move(self, piece_type):
        best_score = float('-inf')
        best_x = 3  # Default to middle
        best_rotation = 0
        
        for rotation_index in range(len(self.ROTATIONS[piece_type])):
            for x in range(-2, self.GRID_WIDTH + 2):
                score = self.evaluate_position(piece_type, x, rotation_index)
                if score > best_score:
                    best_score = score
                    best_x = x
                    best_rotation = rotation_index
        
        return best_x, best_rotation