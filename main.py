# Acorn

import pygame as pg
import random

pg.init()
pg.display.set_caption("Conway's Game of Life")

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_COLOR = (4, 0, 10)
CELL_SIZE = 10
GEN_INTERVAL = 60
game_running = True

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Grid:
	def __init__(self, width = SCREEN_WIDTH, height = SCREEN_HEIGHT, 
				 cell_size = CELL_SIZE, color = SCREEN_COLOR):
		self.color_dead = color
		self.color_alive = (250, 250, 250)
		self.color_hover_dead = (54, 50, 60)
		self.color_hover_alive = (200, 200, 200)

		self.cell_size = cell_size
		self.col = width // cell_size
		self.row = height // cell_size
		self.grid = self.generate_grid()
		self.live_cells = []

		self.paused = True

	def generate_grid(self):
		return [[0 for x in range(self.col)] for y in range(self.row)]

	def regenerate_grid(self):
		self.grid = self.generate_grid()

		for cell in self.live_cells:
			self.grid[cell[1]][cell[0]] = 1 

	def update_state(self, screen, mouse_pos, mouse_buttons):
		col = mouse_pos[0] // self.cell_size
		row = mouse_pos[1] // self.cell_size

		if mouse_buttons[0]:
			self.grid[row][col] = 1

			if(col, row) not in self.live_cells:
				self.live_cells.append((col, row))

		elif mouse_buttons[2]:
			self.grid[row][col] = 0

			if(col, row) in self.live_cells:
				self.live_cells.remove((col, row))

	def advance_gen(self):
		next_grid = [[0 for x in range(self.col)] for y in range(self.row)]

		for row in range(self.row):
			for col in range(self.col):
				num_neighbors = 0

				for i in [-1, 0, 1]:
					for j in [-1, 0, 1]:
						if i == 0 and j == 0:
							continue

						neighbor_row = (row + j) % self.row 
						neighbor_col = (col + i) % self.col

						if self.grid[neighbor_row][neighbor_col] == 1:
							num_neighbors += 1

				if self.grid[row][col] == 1:
					if num_neighbors < 2 or num_neighbors > 3:
						next_grid[row][col] = 0	

					else:
						next_grid[row][col] = 1

				else:
					if num_neighbors == 3:
						next_grid[row][col] = 1

		self.grid = next_grid

	def draw_grid(self, screen):
		for row in range(self.row):
			for col in range(self.col):
				cell = pg.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)

				if self.grid[row][col] == 0:
					pg.draw.rect(screen, self.color_dead, cell, 0)

				elif self.grid[row][col] == 1:
					pg.draw.rect(screen, self.color_alive, cell, 0)
				
	def handle_mouse_hover(self, screen, mouse_pos):
		for row in range(self.row):
			for col in range(self.col):
				cell = pg.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)

				if cell.collidepoint(mouse_pos) and self.grid[row][col] == 0:
					pg.draw.rect(screen, self.color_hover_dead, cell, 0)

				if cell.collidepoint(mouse_pos) and self.grid[row][col] == 1:
					pg.draw.rect(screen, self.color_hover_alive, cell, 0)

	def reset(self):
		self.grid = self.generate_grid()


grid = Grid()
last_gen = pg.time.get_ticks()


while game_running:
	screen.fill(SCREEN_COLOR)

	current_gen = pg.time.get_ticks()
	if not grid.paused and current_gen - last_gen > GEN_INTERVAL:
		grid.advance_gen()

		last_gen = current_gen

	grid.draw_grid(screen)
	mouse_pos = pg.mouse.get_pos()
	grid.handle_mouse_hover(screen, mouse_pos)

	mouse_buttons = pg.mouse.get_pressed()
	if mouse_buttons[0] or mouse_buttons[2]:
		grid.update_state(screen, mouse_pos, mouse_buttons)

	for event in pg.event.get():
		if event.type == pg.QUIT:
			game_running = False

		if event.type == pg.KEYDOWN:
			if event.key == pg.K_SPACE:
				grid.paused = not grid.paused

			if event.key == pg.K_x:
				grid.reset()

	pg.display.update()
	pg.time.Clock().tick(60)

pg.quit()