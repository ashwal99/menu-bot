from build_embedding_model import get_embedding_model
from restaurant_menu import restaurant_menu
import numpy as np

embeddingsForMenu = np.array(
    get_embedding_model().encode(restaurant_menu, 10))
np.save('menu-bot/embeddingsForMenu.npy', embeddingsForMenu)
