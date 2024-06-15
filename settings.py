import math

# Game Settings
RATIO = 1
RESOLUTION = WIDTH, HEIGHT = 1600*RATIO, 900*RATIO
HALF_HEIGHT, HALF_WIDTH = HEIGHT //2, WIDTH // 2
FPS = 60

PLAYER_POSITION = 1, 5
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_ROT_SPEED = 0.002
PLAYER_SIZE_SCALE = 60 
# to be honest, I wouldn't think about this only when 
# I'll notice the problem and try to solve it, is that normal ?
# Maybe because I'm used to go and program things without plan, 
# which is a bad habit

# Mouse Settings
MOUSE_SENSITIVITY = 0.0001
MOUSE_MAX_RELATIVE_MOUVEMENT = 40
MOUSE_BORDER_LEFT = 100
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT

FOV = math.pi / 3 # field of view
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20

# Constant value, In Wolfenstein game they used the one that's 
# easy to multipliy by only using the shifts
SCREEN_DISTANCE = HALF_WIDTH / math.tan(HALF_FOV) 
SCALE = WIDTH // NUM_RAYS

TEXTURE_SIZE = 64
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2

# utils
f = lambda txt, idx : txt.split(',')[idx]
names = [chr(65+i)+str(j) for i in range(20) for j in range(1,100)]

# Networking
SERVER_IP = "192.168.1.12"
PORT = 12345
HEADER= 128
ADDR = (SERVER_IP, PORT)
DM = "@disconnect"