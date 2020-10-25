import math


def has_collided(enemyX, enemyY, shotX, shotY):
    distance = math.sqrt((math.pow(enemyX - shotX, 2)) + (math.pow(enemyY - shotY, 2)))
    if distance < 30:
        return True
    else:
        return False

