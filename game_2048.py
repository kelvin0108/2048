import numpy as np
import random
import pygame
import sys

class Game:
    def __init__(self, game_mode="ai", render=0, width=4, height=4):
        self.game_mode = game_mode
        self.width = width
        self.height = height
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        if render == 1:
            pygame.init()
            self.clock = pygame.time.Clock()
            self.screen_width = 300
            self.screen_height = 300
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            pygame.display.set_caption("2048")
            if game_mode == "human":
                self.main_loop()     

    def reset(self):
        self.state = np.zeros((self.width, self.height))
        self.state[(random.randrange(0, 4, 1),random.randrange(0, 4, 1))] = 2
        self.done = False
        self.checked = False
        self.total_score = 0
        self.up, self.right, self.down, self.left = False, False, False, False
        return self.state
    
    def step(self, action):
        assert 0 <= action <= 3, "Error: Action values should fall within the interval [0, 3]"       
        assert self.done == False, "The game has ended."
        self.reward = 0
        moved = False

        if action == 0:  # Right
            for i_h in range(self.height):
                row = self.state[i_h, :]
                new_row = [num for num in row if num != 0]
                merged_row = []
                skip = False
                for j in range(len(new_row) - 1, -1, -1):
                    if skip:
                        skip = False
                        continue
                    if j > 0 and new_row[j] == new_row[j - 1]:
                        merged_row.insert(0, new_row[j] * 2)
                        self.reward += new_row[j] * 2
                        skip = True
                        moved = True
                    else:
                        merged_row.insert(0, new_row[j])
                while len(merged_row) < self.width:
                    merged_row.insert(0, 0)
                self.state[i_h, :] = merged_row

        elif action == 1:  # Down
            for i_w in range(self.width):
                col = self.state[:, i_w]
                new_col = [num for num in col if num != 0]
                merged_col = []
                skip = False
                for j in range(len(new_col) - 1, -1, -1):
                    if skip:
                        skip = False
                        continue
                    if j > 0 and new_col[j] == new_col[j - 1]:
                        merged_col.insert(0, new_col[j] * 2)
                        self.reward += new_col[j] * 2
                        skip = True
                        moved = True
                    else:
                        merged_col.insert(0, new_col[j])
                while len(merged_col) < self.height:
                    merged_col.insert(0, 0)
                self.state[:, i_w] = merged_col

        elif action == 2:  # Left
            for i_h in range(self.height):
                row = self.state[i_h, :]
                new_row = [num for num in row if num != 0]
                merged_row = []
                skip = False
                for j in range(len(new_row)):
                    if skip:
                        skip = False
                        continue
                    if j < len(new_row) - 1 and new_row[j] == new_row[j + 1]:
                        merged_row.append(new_row[j] * 2)
                        self.reward += new_row[j] * 2
                        skip = True
                        moved = True
                    else:
                        merged_row.append(new_row[j])
                while len(merged_row) < self.width:
                    merged_row.append(0)
                self.state[i_h, :] = merged_row

        elif action == 3:  # Up
            for i_w in range(self.width):
                col = self.state[:, i_w]
                new_col = [num for num in col if num != 0]
                merged_col = []
                skip = False
                for j in range(len(new_col)):
                    if skip:
                        skip = False
                        continue
                    if j < len(new_col) - 1 and new_col[j] == new_col[j + 1]:
                        merged_col.append(new_col[j] * 2)
                        self.reward += new_col[j] * 2
                        skip = True
                        moved = True
                    else:
                        merged_col.append(new_col[j])
                while len(merged_col) < self.height:
                    merged_col.append(0)
                self.state[:, i_w] = merged_col

        # 若有移動，隨機生成一個新的 2
        if moved:
            zero_positions = np.argwhere(self.state == 0)
            if zero_positions.size > 0:
                random_index = np.random.choice(len(zero_positions))
                random_position = zero_positions[random_index]    
                self.state[random_position[0], random_position[1]] = 2

        self.total_score += self.reward
        info = {"score": self.total_score}
        
        biggest_num = np.max(self.state)

        # 檢查是否還有可以進行的移動
        if not any(self.check_move(act) for act in range(4)):
            self.done = True     

        return self.state, self.reward, self.done, info, biggest_num    

    def check_move(self, action):
        moved = False
        temp_state = self.state.copy()  # 保留原始状态，以便检查后还原
        if action == 0:  # Right
            for i_h in range(self.height):
                row = temp_state[i_h, :]
                new_row = [num for num in row if num != 0]
                skip = False
                for j in range(len(new_row) - 1, -1, -1):
                    if skip:
                        skip = False
                        continue
                    if j > 0 and new_row[j] == new_row[j - 1]:
                        moved = True
                        break
                    elif new_row[j] == 0 or (j > 0 and new_row[j - 1] == 0):
                        moved = True
                        break
                if moved:
                    break

        elif action == 1:  # Down
            for i_w in range(self.width):
                col = temp_state[:, i_w]
                new_col = [num for num in col if num != 0]
                skip = False
                for j in range(len(new_col) - 1, -1, -1):
                    if skip:
                        skip = False
                        continue
                    if j > 0 and new_col[j] == new_col[j - 1]:
                        moved = True
                        break
                    elif new_col[j] == 0 or (j > 0 and new_col[j - 1] == 0):
                        moved = True
                        break
                if moved:
                    break

        elif action == 2:  # Left
            for i_h in range(self.height):
                row = temp_state[i_h, :]
                new_row = [num for num in row if num != 0]
                skip = False
                for j in range(len(new_row)):
                    if skip:
                        skip = False
                        continue
                    if j < len(new_row) - 1 and new_row[j] == new_row[j + 1]:
                        moved = True
                        break
                    elif new_row[j] == 0 or (j < len(new_row) - 1 and new_row[j + 1] == 0):
                        moved = True
                        break
                if moved:
                    break

        elif action == 3:  # Up
            for i_w in range(self.width):
                col = temp_state[:, i_w]
                new_col = [num for num in col if num != 0]
                skip = False
                for j in range(len(new_col)):
                    if skip:
                        skip = False
                        continue
                    if j < len(new_col) - 1 and new_col[j] == new_col[j + 1]:
                        moved = True
                        break
                    elif new_col[j] == 0 or (j < len(new_col) - 1 and new_col[j + 1] == 0):
                        moved = True
                        break
                if moved:
                    break

        return moved

    
    def render(self):
        square_size = min(self.screen_width, self.screen_height) // max(self.width, self.height)
        for x in range(0, self.screen_width, square_size):
            pygame.draw.line(self.screen, (200, 200, 200), (x, 0), (x, self.screen_height))
        for y in range(0, self.screen_height, square_size):
            pygame.draw.line(self.screen, (200, 200, 200), (0, y), (self.screen_width, y))
        pygame.display.flip()
        self.clock.tick(60)

    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.down = True
                    elif event.key == pygame.K_UP:
                        self.up = True
                    elif event.key == pygame.K_LEFT:
                        self.left = True
                    elif event.key == pygame.K_RIGHT:
                        self.right = True
                if self.right:
                    action = 0
                elif self.down:
                    action = 1
                elif self.left:
                    action = 2
                elif self.up:
                    action = 3
                self.state, self.done, self.reward, info = self.step(action)
                if self.done:
                    self.reset() 
                

if __name__ == "__main__":
    game = Game()
    game.reset()
    game.state = np.full((4, 4), 2)
    print(game.state)
    game.step(0)
    print(game.state)
