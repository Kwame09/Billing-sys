from cairosvg import svg2png
from PIL import Image

from io import BytesIO
import os


icons = {}

folder = os.path.realpath(os.path.join(os.curdir, 'assets'))

for fd in os.listdir(folder):
    fname, ext = os.path.splitext(fd)
    if ext != '.py':
        img_url = os.path.realpath(os.path.join(os.curdir, 'assets', fd))
        if ext == '.svg':
            img_io = BytesIO()
            svg2png(url=img_url, write_to=img_io)
        icons[fname] = Image.open(img_io)

UserIcon = icons['user']
PlusIcon = icons['plus']
UsersIcon = icons['users']
AddImageIcon = icons['add_img']
ChartBarIcon = icons['chart-bar']
ChartPieIcon = icons['chart-pie']
ChartAreaIcon = icons['chart-area']
ChartLineIcon = icons['chart-line']
PlusSquareIcon = icons['plus-square']
PlusSQuareRIcon = icons['plus-square-r']
ShoppingCartIcon = icons['shopping-cart']
ShoppingBasketIcon = icons['shopping-basket']
