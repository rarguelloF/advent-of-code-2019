#!/usr/bin/env python

from typing import List, Tuple


def image_to_string(size: Tuple[int, int], image: List[int]) -> str:
    codes = {
        0: ' ',
        1: u"\u25A0",
        2: ' ',
    }

    result = '\n'
    size_x, size_y = size
    area = size_x * size_y
    for i in range(area):
        px = image[i]
        result += codes[px]

        if (i+1) % size_x == 0:
            result += '\n'

    return result


def decode_image(size: Tuple[int, int], pixels: List[int]) -> List[int]:
    size_x, size_y = size
    area = size_x * size_y
    num_layers = int(len(pixels) / area)
    layer_imgs = [pixels[i*area:(i*area)+area] for i in range(num_layers)]

    result: List[int] = []
    for px in zip(*layer_imgs):
        res_px = 2
        for p in px:
            if p != 2:
                res_px = p
                break

        result.append(res_px)

    return result


def part_2(pixels: List[int]) -> str:
    size = (25, 6)
    img = decode_image(size, pixels)
    return image_to_string(size, img)


def part_1(pixels: List[int]) -> int:
    size_x, size_y = (25, 6)
    area = size_x * size_y
    num_layers = int(len(pixels) / area)
    layer_imgs = [pixels[i*area:(i*area)+area] for i in range(num_layers)]
    layer_num_zeroes = [layer.count(0) for layer in layer_imgs]
    layer_fewest_zeroes = layer_imgs[layer_num_zeroes.index(min(layer_num_zeroes))]

    return layer_fewest_zeroes.count(1) * layer_fewest_zeroes.count(2)


if __name__ == "__main__":
    with open('08.txt', 'r') as file:
        pixels = [int(x) for x in file.read().replace('\n', '')]

    print(f"Part 1: {part_1(pixels)}")
    print(f"Part 2: {part_2(pixels)}")
