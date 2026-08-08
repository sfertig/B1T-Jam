import asyncio
import pygame
import sys
import os

from src.Net import Net
from src.screens import Title_screen
from src.utils import init_save_dir, Keys
from src.Load_Assets import LoadAssets

init_save_dir()

pygame.init()

width, height = 640, 360

Net.screen = pygame.display.set_mode((width, height), pygame.SCALED | pygame.FULLSCREEN)
pygame.display.set_caption("Tearful Tilling")
Net.clock = pygame.time.Clock()

Net.init()
Keys.add_net(Net)
LoadAssets()

#run
Title_screen().run()

pygame.quit()
os.system('cls')
sys.exit()

