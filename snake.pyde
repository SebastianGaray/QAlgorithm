import random
import time
actionSize = 4
stateSize = 25
qTable = [[0]*actionSize for n in range(stateSize)]

total_episodes = 15000        # Total episodes
learning_rate = 0.8           # Learning rate
max_steps = 99                # Max steps per episode
gamma = 0.95                  # Discounting rate

# Exploration parameters
epsilon = 1.0                 # Exploration rate
max_epsilon = 1.0             # Exploration probability at start
min_epsilon = 0.01            # Minimum exploration probability 
decay_rate = 0.005             # Exponential decay rate for exploration prob






generation = 1
myBoard = None
print("Puntos: 0")
def setup():
    global myBoard
    myBoard = Board(5,5)
    global x
    x = 0
    size(800, 600)
    
        

def moveSnake(dir):
    myBoard.grid[myBoard.snake.posX][myBoard.snake.posY] = 1
    if(dir == "w"):
        myBoard.snake.posX = myBoard.snake.posX-1
    if(dir == "s"):
        myBoard.snake.posX = myBoard.snake.posX+1
    if(dir == "a"):
        myBoard.snake.posY = myBoard.snake.posY-1
    if(dir == "d"):
        myBoard.snake.posY = myBoard.snake.posY+1

def step(action):
    # 0 -> Mover a izquierda
    if(action == 0):
        moveSnake("a")
    # 1 -> Mover a arriba
    if(action == 1):
        moveSnake("w")
    # 2 -> Mover a derecha
    if(action == 2):
        moveSnake("d")
    # 3 -> Mover a abajo
    if(action == 3):
        moveSnake("s")
def randomAction():
    posX = myBoard.snake.posX
    posY = myBoard.snake.posY
    # Solo derecha y abajo
    if((posX == 0)and(posY == 0)):
        newAction = random.randint(0,1)
        if(newAction == 0):
            newAction = 2
        else:
            newAction = 3
    # Solo izquierda, abajo y derecha
    if((posX == 0)and(posY != 0)and(posY != 4)):
        newAction = random.randint(0,2)
        # No es necesario con newAction = 0, ya que el 0 
        # representa izquierda
        if(newAction == 1):
            newAction = 3
    # Solo izquierda y abajo
    if((posX == 0)and(posY == 4)):
        newAction = random.randint(0,1)
        # No es necesario con newAction = 0, ya que el 0 
        # representa izquierda
        if(newAction == 1):
            newAction = 3
    # Cualquier movimiento
    if((posX > 0) and (posX < 4) and (posY > 0) and (posY < 4)):
        newAction = random.randint(0,3)
    # Solo arriba, derecha, abajo
    if((posX != 0)and(posX != 4) and (posY ==0)):
        newAction = random.randint(1,3)
    # Solo arriba y derecha
    if((posX == 4) and (posY ==0)):
        newAction = random.randint(1,2)
    # Solo arriba, derecha e izquierda
    if((posX == 4) and (posY != 0) and (posY != 4)):
        newAction = random.randint(0,2)
    # Solo arriba e izquierda
    if((posX == 4) and (posY == 4)):
        newAction = random.randint(0,1)
    # Solo arriba, izquierda y abajo
    if((posX != 4) and (posX != 0) and (posY == 4)):
        newAction = random.randint(0,2)
        if(newAction == 2):
            newAction = 3
    return newAction

def move():
    exp_exp_tradeoff = random.uniform(0, 1)
    
    ## If this number > greater than epsilon --> exploitation (taking the biggest Q value for this state)
    if exp_exp_tradeoff > epsilon:
        action = index(max(qTable[myBoard.state,:]))
    # Else doing a random choice --> exploration
    else:
        action = randomAction()
    print(action)
    step(action)


def update():
    # Sumar puntaje si la nueva posicion era un 2
    if(myBoard.grid[myBoard.snake.posX][myBoard.snake.posY] == 2):
        myBoard.snake.points = myBoard.snake.points + 100
        myBoard.total_rewards = myBoard.total_rewards+1
    # Restar puntaje si la nueva posicion era un -1
    if(myBoard.grid[myBoard.snake.posX][myBoard.snake.posY] == -1):
        myBoard.snake.points = myBoard.snake.points - 10
    # Actualizar la posicion de la serpiente en el tablero
    myBoard.grid[myBoard.snake.posX][myBoard.snake.posY] = 0


def draw():
    global generation
    background(0)
    print("Generacion: %d\nPuntaje: %d"%(generation, myBoard.snake.points))
    update()
    myBoard.draw()
    move()
    delay(200)
    if(myBoard.total_rewards == 2):
        setup()
        generation = generation + 1


class Board:
    def __init__(self, nCol, nRow):
        self.nCol = nCol
        self.nRow = nRow
        self.total_rewards = 0
        self.state = 0
        self.grid = [[1]*nCol for n in range(nRow)]
        self.grid[3][4] = 2
        self.grid[1][4] = 2
        self.grid[2][4] = -1
        
        self.grid[2][2] = -1
        self.grid[1][2] = -1
        self.grid[0][2] = -1
        self.grid[0][0] = 0
        self.snake = Snake()
    def draw(self):
        x, y = 0,0
        w = 70
        for row in self.grid:
            for col in row:
                if col == 2:
                    fill(255,0,0)
                elif col == 1:
                    fill(255)
                elif col == 0:
                    fill(0,255,0)
                else:
                    fill(100)
                rect(x, y, w, w)
                x = x+w
            y = y+w
            x = 0
class Snake():
    def __init__(self):
        self.posX = 0
        self.posY = 0
        self.points = 0
