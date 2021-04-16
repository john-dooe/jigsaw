import os
import random
import argparse
from PIL import Image
from tqdm import tqdm


def random_choice():
    return random.randint(-1, 1)


def calc_file(x, y):
    num = str(y * x_sum + x).zfill(zfill_len)
    return f'jigsaw/{num}.png'


def add_border(file):
    img = Image.open(file)
    new_img = Image.new('RGBA', (new_piece_width, new_piece_height), (0, 0, 0, 0))
    new_img.paste(img, (sawtooth_width, sawtooth_width))
    new_img.save(file)


def init_table():
    info_table = []
    for y in range(y_sum):
        row_info = []
        for x in range(x_sum):
            img_info = ['free', 'free', 'free', 'free']
            if x == 0:
                img_info[3] = 'occupied'
            elif x == x_sum - 1:
                img_info[1] = 'occupied'
            if y == 0:
                img_info[0] = 'occupied'
            elif y == y_sum - 1:
                img_info[2] = 'occupied'
            row_info.append(img_info)
        info_table.append(row_info)
    return info_table


def cut(direction, file):
    if direction == 0:
        left_top_x = (piece_width - sawtooth_width) // 2 + sawtooth_width
        left_top_y = sawtooth_width
    elif direction == 1:
        left_top_x = piece_width
        left_top_y = (piece_height - sawtooth_width) // 2 + sawtooth_width
    elif direction == 2:
        left_top_x = (piece_width - sawtooth_width) // 2 + sawtooth_width
        left_top_y = piece_height
    elif direction == 3:
        left_top_x = sawtooth_width
        left_top_y = (piece_height - sawtooth_width) // 2 + sawtooth_width
    right_bottom_x = left_top_x + sawtooth_width
    right_bottom_y = left_top_y + sawtooth_width
    img = Image.open(file)
    cut_img = img.crop((left_top_x, left_top_y, right_bottom_x, right_bottom_y))
    blank_img = Image.new('RGBA', (sawtooth_width, sawtooth_width), (0, 0, 0, 0))
    img.paste(blank_img, (left_top_x, left_top_y))
    img.save(file)
    return cut_img


def paste(direction, file, cut_img):
    if direction == 0:
        left_top_x = (piece_width - sawtooth_width) // 2 + sawtooth_width
        left_top_y = 0
    elif direction == 1:
        left_top_x = piece_width + sawtooth_width
        left_top_y = (piece_height - sawtooth_width) // 2 + sawtooth_width
    elif direction == 2:
        left_top_x = (piece_width - sawtooth_width) // 2 + sawtooth_width
        left_top_y = piece_height + sawtooth_width
    elif direction == 3:
        left_top_x = 0
        left_top_y = (piece_height - sawtooth_width) // 2 + sawtooth_width
    img = Image.open(file)
    img.paste(cut_img, (left_top_x, left_top_y))
    img.save(file)


def create_jigsaw(info_table):
    for y in tqdm(range(y_sum)):
        for x in range(x_sum):
            img_info = info_table[y][x]
            file = calc_file(x, y)
            for direction in range(4):
                if img_info[direction] == 'free':
                    if direction == 0:
                        x2 = x
                        y2 = y - 1
                        file2 = calc_file(x2, y2)
                        direction2 = 2
                    elif direction == 1:
                        x2 = x + 1
                        y2 = y
                        file2 = calc_file(x2, y2)
                        direction2 = 3
                    elif direction == 2:
                        x2 = x
                        y2 = y + 1
                        file2 = calc_file(x2, y2)
                        direction2 = 0
                    elif direction == 3:
                        x2 = x - 1
                        y2 = y
                        file2 = calc_file(x2, y2)
                        direction2 = 1

                    choice = random_choice()

                    if choice == -1:
                        cut_img = cut(direction, file)
                        paste(direction2, file2, cut_img)
                    elif choice == 1:
                        cut_img = cut(direction2, file2)
                        paste(direction, file, cut_img)
                    info_table[y2][x2][direction2] = 'occupied'
                    img_info[direction] = 'occupied'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A jigsaw creator')
    parser.add_argument('-i', '--image_name', type=str, required=True)
    parser.add_argument('-pw', '--piece_width', type=int, required=True)
    parser.add_argument('-ph', '--piece_height', type=int, required=True)
    parser.add_argument('-sw', '--sawtooth_width', type=int, required=True)
    args = parser.parse_args()

    img = Image.open(args.image_name)
    width, height = img.size
    piece_width = args.piece_width
    piece_height = args.piece_height
    sawtooth_width = args.sawtooth_width

    assert width / piece_width == width // piece_width and height / piece_height == height // piece_height
    assert piece_width / sawtooth_width >= 3 and piece_height / sawtooth_width >= 3

    x_sum = width // piece_width
    y_sum = height // piece_height
    zfill_len = len(str(x_sum * y_sum))

    if not os.path.exists('jigsaw'):
        os.mkdir('jigsaw')
    os.system(f'convert -crop {piece_width}x{piece_height} +repage {args.image_name} jigsaw/%0{zfill_len}d.png')

    new_piece_width = piece_width + sawtooth_width * 2
    new_piece_height = piece_height + sawtooth_width * 2

    for i in range(x_sum * y_sum):
        file = 'jigsaw/' + str(i).zfill(zfill_len) + '.png'
        add_border(file)
    info_table = init_table()
    create_jigsaw(info_table)
