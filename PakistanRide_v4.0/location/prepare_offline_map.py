from pathlib import Path
import tkintermapview
root=Path(__file__).resolve().parent.parent
db=root/'data'/'pakistan'/'offline_tiles.db'
loader=tkintermapview.OfflineLoader(path=str(db),tile_server='https://tile.openstreetmap.org/{z}/{x}/{y}.png')
loader.save_offline_tiles((37.2,60.8),(23.4,77.9),4,8)
print('Created',db)
