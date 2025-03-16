import requests as r
from PIL import Image
import json

url = 'https://olimp.miet.ru/ppo_it/api'

def fetch_random_json():

    part = json.loads(r.get(url).text)['message']['data']
    return part


def collect_unique_json(num_required):
    unique_jsons = set()

    while len(unique_jsons) < num_required:
        random_json = fetch_random_json()
        json_str = json.dumps(random_json)
        unique_jsons.add(json_str)

    return [json.loads(json_str) for json_str in unique_jsons]


unique_jsons = collect_unique_json(16)

def draw(mapp):
    im = Image.new('RGB', (256, 256), (0, 0, 0))
    sx, sy = 0, 0
    pixels = im.load()
    x, y = im.size
    for i in range(4):
        for j in range(4):
            sx = i * 64
            sy = j * 64
            curr_tail = mapp[i * 4 + j]
            for ii in range(64):
                for jj in range(64):
                    pixels[sy + ii, sx + jj] = curr_tail[ii][jj], 0, 0
    im.save('map.jpg')

map = []
for part in unique_jsons:
    map.append(part)

draw(map)
print(json.dumps(unique_jsons, indent=2))