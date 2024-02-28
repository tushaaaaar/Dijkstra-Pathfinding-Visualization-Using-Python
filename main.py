from tkinter import messagebox, Tk
import pygame
import sys

WIDTH = 1200
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))

COLUMNS = 60
ROWS = 40

BOX_WIDTH = WIDTH // COLUMNS
BOX_HEIGHT = HEIGHT // ROWS

grid = []
queue = []
path = []

class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None

    def draw (self, win, color):
        pygame.draw.rect(win, color, (self.x * BOX_WIDTH, self.y * BOX_HEIGHT, BOX_WIDTH - 2, BOX_HEIGHT - 2))

    def set_neighbours (self):
        if self.x > 0:
            self.neighbours.append(grid[self.x-1][self.y])
        if self.x < COLUMNS - 1:
            self.neighbours.append(grid[self.x+1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y-1])
        if self.y < ROWS - 1:
            self.neighbours.append(grid[self.x][self.y+1])


# Create Grid
for i in range (COLUMNS):
    arr = []
    for j in range (ROWS):
        arr.append(Box(i ,j))
    grid.append(arr)

# Set Neighbours
for i in range (COLUMNS):
    for j in range (ROWS):
        grid[i][j].set_neighbours()



def main ():
    begin_search = False
    target_box_set = False
    searching = True
    target_box = None
    start_box_set = False

    while True:
        for event in pygame.event.get():
            # Quit Window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mouse Controls
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]

                # Draw Walls
                if event.buttons[0]:
                    i = x // BOX_WIDTH
                    j = y // BOX_HEIGHT
                    grid[i][j].wall = True
            
            if pygame.mouse.get_pressed()[0] and not start_box_set:
                i = x // BOX_WIDTH
                j = y // BOX_HEIGHT
                start_box = grid[i][j]
                start_box.start = True
                start_box.visited = True
                queue.append(start_box)
                start_box_set = True
            # Set Target
            if pygame.mouse.get_pressed()[2] and not target_box_set and start_box_set:
                i = x // BOX_WIDTH
                j = y // BOX_HEIGHT
                grid[i][j].target = True
                target_box_set = True
                target_box = grid[i][j]
           
            # Start Algorithm
            if event.type == pygame.KEYDOWN and target_box_set:
                begin_search = True
        
        if begin_search:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                if current_box == target_box:
                    searching = False
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = current_box
                            queue.append(neighbour) 
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No solution", "There is no solution!")
                    searching = False

        screen.fill((0, 0, 0))

        for i in range (COLUMNS):
            for j in range (ROWS):
                box = grid[i][j]
                box.draw(screen, (30, 30, 30))
                if box.queued:
                    box.draw (screen, (200, 0, 0))
                if box.visited:
                    box.draw (screen, (0, 200, 0))
                if box in path:
                    box.draw (screen, (0, 0, 200))
                if box.start:
                    box.draw (screen, (0, 200, 200))
                if box.wall:
                    box.draw (screen, (90, 90, 90))
                if box.target:
                    box.draw (screen, (200, 200, 0))

        pygame.display.flip()
    
main()