from build_embedding_model import get_embeddings
from restaurant_menu import restaurant_menu
import numpy as np

embeddingsForMenu = np.array(get_embeddings(restaurant_menu))
np.save('menu-bot/embeddingsForMenu.npy', embeddingsForMenu)
