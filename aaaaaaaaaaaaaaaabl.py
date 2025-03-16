import requests as r
import json
from PIL import Image


def draw(mapp):
    im = Image.new('RGB', (256, 256), (0, 0, 0))
    sx, sy = 0, 0
    pixels = im.load()
    for i in range(4):
        for j in range(4):
            sx = i * 64
            sy = j * 64
            curr_tail = mapp[i * 4 + j]
            for ii in range(64):
                for jj in range(64):
                    pixels[sy + ii, sx + jj] = curr_tail[ii][jj], 0, 0
    im.save('map.webp')


url = 'https://olimp.miet.ru/ppo_it/api'
map = []
for _ in range(16):
    req = json.loads(r.get(url).text)['message']['data']
    while req not in map:
        req = json.loads(r.get(url).text)['message']['data']
    map.append(req)
draw(map)
print(map)
