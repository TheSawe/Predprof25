import numpy as np
import cv2
import os

def load_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Не удалось загрузить изображение. Проверьте путь.")
    return image

def split_into_tiles(image):
    tiles = []
    tile_size = 64
    for i in range(0, 256, tile_size):
        for j in range(0, 256, tile_size):
            tile = image[i:i + tile_size, j:j + tile_size]
            tiles.append(tile)
    return tiles

def classify_tile(tile):
    borders = [
        tile[0, :], 
        tile[-1, :], 
        tile[:, 0], 
        tile[:, -1] 
    ]
    uniform_borders = [np.all(border == border[0]) for border in borders]
    wall_count = sum(uniform_borders)
    if wall_count == 2:
        return "corner"
    elif wall_count == 1:
        return "wall"
    else:
        return "inner"

def assemble_map(tiles):
    map_size = 256
    tile_size = 64
    map_data = np.zeros((map_size, map_size), dtype=np.uint8)

    corners = [tile for tile in tiles if classify_tile(tile) == "corner"]
    walls = [tile for tile in tiles if classify_tile(tile) == "wall"]
    inners = [tile for tile in tiles if classify_tile(tile) == "inner"]

    map_data[0:tile_size, 0:tile_size] = corners[0]
    map_data[0:tile_size, -tile_size:] = corners[1]
    map_data[-tile_size:, 0:tile_size] = corners[2]
    map_data[-tile_size:, -tile_size:] = corners[3]

    for i in range(1, 3):
        map_data[0:tile_size, i * tile_size:(i + 1) * tile_size] = walls[i - 1]
        map_data[-tile_size:, i * tile_size:(i + 1) * tile_size] = walls[i + 3]
        map_data[i * tile_size:(i + 1) * tile_size, 0:tile_size] = walls[i + 1]
        map_data[i * tile_size:(i + 1) * tile_size, -tile_size:] = walls[i + 5]

    for i in range(1, 3):
        for j in range(1, 3):
            map_data[i * tile_size:(i + 1) * tile_size, j * tile_size:(j + 1) * tile_size] = inners.pop()

    return map_data

def apply_color_map(map_data):
    color_map = np.zeros((map_data.shape[0], map_data.shape[1], 3), dtype=np.uint8)
    color_map[:, :, 2] = map_data 
    return color_map

def save_map(map_data, output_path):
    cv2.imwrite(output_path, map_data)

def main():
    image_path = "final_map.png" 
    image = load_image(image_path)

    tiles = split_into_tiles(image)

    map_data = assemble_map(tiles)

    colored_map = apply_color_map(map_data)

    output_path = os.path.expanduser("~/reconstructed_map.png") 
    save_map(colored_map, output_path)
    print(f"Карта сохранена в {output_path}")

if __name__ == "__main__":
    main()
