import os
import argparse
from PIL import Image
from tqdm import tqdm


def calc_file(x, y):
    num = str(y * x_sum + x).zfill(zfill_len)
    return f'jigsaw/{num}.png'


def check_info(file):
    img_info = [0, 0, 0, 0]
    img = Image.open(file)
    pix_out1 = img.getpixel((new_piece_width // 2, 0))[3]
    pix_out2 = img.getpixel((new_piece_width - 1, new_piece_height // 2))[3]
    pix_out3 = img.getpixel((new_piece_width // 2, new_piece_height - 1))[3]
    pix_out4 = img.getpixel((0, new_piece_height // 2))[3]
    pix_out = [pix_out1, pix_out2, pix_out3, pix_out4]
    pix_in1 = img.getpixel((new_piece_width // 2, sawtooth_width))[3]
    pix_in2 = img.getpixel((new_piece_width - sawtooth_width - 1, new_piece_height // 2))[3]
    pix_in3 = img.getpixel((new_piece_width // 2, new_piece_height - sawtooth_width - 1))[3]
    pix_in4 = img.getpixel((sawtooth_width, new_piece_height // 2))[3]
    pix_in = [pix_in1, pix_in2, pix_in3, pix_in4]
    for i in range(4):
        if pix_out[i] == 0 and pix_in[i] == 0:
            img_info[i] = -1
        elif pix_out[i] != 0 and pix_in[i] != 0:
            img_info[i] = 1
        elif pix_out[i] == 0 and pix_in[i] != 0:
            img_info[i] = 0
        else:
            raise Exception("Invalid jigsaw!", file)
    return img_info


def init_table():
    info_table = []
    for y in range(y_sum):
        row_info = []
        for x in range(x_sum):
            file = calc_file(x, y)
            img_info = check_info(file)
            row_info.append(img_info)
        info_table.append(row_info)
    return info_table


def cut(direction, file):
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

    img = Image.open(file)
    img.paste(cut_img, (left_top_x, left_top_y))
    img.save(file)


def recover_jigsaw(info_table):
    for y in tqdm(range(y_sum)):
        for x in range(x_sum):
            img_info = info_table[y][x]
            for direction in range(4):
                if img_info[direction] != 'free':
                    file = calc_file(x, y)

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

                    if img_info[direction] == 1:
                        cut_img = cut(direction, file)
                        paste(direction2, file2, cut_img)
                    elif img_info[direction] == -1:
                        cut_img = cut(direction2, file2)
                        paste(direction, file, cut_img)
                    info_table[y2][x2][direction2] = 'free'
                    img_info[direction] = 'free'


def remove_border(file):
    img = Image.open(file)
    new_img = img.crop(
        (sawtooth_width, sawtooth_width, new_piece_width - sawtooth_width, new_piece_height - sawtooth_width))
    new_img.save(file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A jigsaw restorer')
    parser.add_argument('-px', '--piece_x_sum', type=int, required=True)
    parser.add_argument('-py', '--piece_y_sum', type=int, required=True)
    parser.add_argument('-sw', '--sawtooth_width', type=int, required=True)
    args = parser.parse_args()

    x_sum = args.piece_x_sum
    y_sum = args.piece_y_sum
    sawtooth_width = args.sawtooth_width
    zfill_len = len(str(x_sum * y_sum))

    new_piece_width, new_piece_height = Image.open('jigsaw/' + os.listdir('jigsaw')[0]).size
    piece_width = new_piece_width - (sawtooth_width * 2)
    piece_height = new_piece_height - (sawtooth_width * 2)
    width = piece_width * x_sum
    height = piece_height * y_sum

    info_table = init_table()
    recover_jigsaw(info_table)
    for i in range(x_sum * y_sum):
        file = 'jigsaw/' + str(i).zfill(zfill_len) + '.png'
        remove_border(file)

    os.system(f'montage jigsaw/* -tile {x_sum}x{y_sum} -geometry {piece_width}x{piece_height}+0+0 restored.jpg')
