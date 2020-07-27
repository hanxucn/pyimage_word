#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import textwrap
# from constant import TITLE_HEIGHT, WIDTH_LIMIT, AUTHOR_HEIGHT
from PIL import Image, ImageDraw, ImageFont


class processImg(object):

    # def __init__(self, images):
    #     self.images = images
    #     self.fond = ImageFont.truetype('FONT.TTF')

    def get_img(self):
        file_path = os.path.dirname(os.path.abspath(__file__))
        files = [f for f in os.listdir(file_path) if os.path.isfile(f)]
        img_files = []
        for file_name in files:
            if file_name.lower().endswith(('ipeg', 'png', 'jpg')):
                img_files.append(file_name)
        return img_files

    def open_img(self, img_path):
        # with open(img_path, 'wb') as f:
        #     return
        file = Image.open(img_path)
        return file

    def set_font_size(self, img, fn, text):
        W, H = img.size
        height_fraction, width_fraction = 0.2, 0.8
        height_limit, width_limit = int(height_fraction*H), int(width_fraction*W)
        line = 1
        font_size = height_limit
        text_num = len(text)
        if fn == 'long':
            while font_size*text_num > width_limit*line:
                font_size = height_limit // line
                line += 1
        elif fn == 'medium':
            font_size = width_limit // text_num
        elif fn == 'short':
            font_size = height_limit
        font = ImageFont.truetype('FONT.TTF', font_size)
        if fn == 'long':
            width_num = width_limit // font_size
            font_size = width_limit // width_num
        else:
            width_num = text_num
        ascent, descent = font.getmetrics()
        res = font.getmask(text).getbbox()
        true_font_size, word_space = ascent, font_size - ascent
        font = ImageFont.truetype('FONT.TTF', true_font_size)

        return font, true_font_size, word_space, width_num

    def draw_horizon_img(self, image, fn, title, author, top, left,
                         au_top, au_left, style='left', tt_color='#FFFFFF', auth_color='#FFFFFF'):
        text = title
        file = Image.open(image).convert('RGB')
        W, H = file.size
        font, true_font_size, word_space, width_num = self.set_font_size(file, fn, text)

        draw = ImageDraw.Draw(file)
        lines = textwrap.wrap(text, width=width_num)
        offset = H*top
        for line in lines:
            if style == 'left':
                margin = W*left
            elif style == 'center':
                margin = 100 + (int(W * 0.8) - len(line) * (true_font_size + word_space)) // 2
            else:
                margin = W * left

            draw.text((margin, offset), line[0], font=font, fill=tt_color)
            margin += true_font_size + word_space
            for word in line[1:]:
                draw.text((margin, offset), word, font=font, fill=tt_color)
                margin += true_font_size + word_space
            offset += true_font_size + word_space
        self.draw_image_author(draw, author, H*au_top, W*au_left, auth_color, style)
        img_path = os.path.join('.', 'output', 'test_center.png')
        file.save('./output/%s_test_horizon_%s.png' % (fn, style))

    def set_vertical_font_size(self, img, fn, text):
        W, H = img.size
        height_fraction, width_fraction = 0.6, 0.3
        height_limit, width_limit = int(height_fraction*H), int(width_fraction*W)
        line = 1
        font_size = width_limit
        text_num = len(text)
        if fn == 'long':
            while font_size*text_num > height_limit*line:
                font_size = width_limit // line
                line += 1
            width_num = height_limit // font_size
            font_size = height_limit // width_num
        elif fn == 'medium':
            font_size = height_limit // text_num
            width_num = text_num
            font_size = height_limit // width_num
        else:
            font_size = width_limit
            width_num = text_num
        font = ImageFont.truetype('FONT.TTF', font_size)

        ascent, descent = font.getmetrics()

        word_space = font_size - ascent
        if fn == 'long':
            font_size = ascent
        font = ImageFont.truetype('FONT.TTF', font_size)

        return font, font_size, word_space, width_num

    def draw_vertical_img(self, image, fn, title, author, top, left,
                          au_top, au_left, style='left', tt_color='#FFFFFF', auth_color='#FFFFFF'):
        text = title
        file = Image.open(image).convert('RGB')
        W, H = file.size
        font, true_font_size, word_space, width_num = self.set_vertical_font_size(file, fn, text)
        draw = ImageDraw.Draw(file)
        lines = textwrap.wrap(text, width=width_num)
        line_num = len(lines)
        offset = H * top
        word_width = true_font_size + word_space
        blank_size = int(W*0.3 // len(lines))
        for index, line in enumerate(lines):
            if style == 'left':
                res = font.getmask(line[0]).getbbox()
                margin = int(W * left) + (line_num - index - 1)*word_width + word_width-res[2]+res[0]
            elif style == 'center':
                margin = int(W * left) + (line_num - index - 1) * blank_size + (blank_size - true_font_size)//2
            else:
                margin = W * left
            offset = H * top
            draw.text((margin, offset), line[0], font=font, fill=tt_color)
            offset += true_font_size + 1.1
            for word in line[1:]:
                draw.text((margin, offset), word, font=font, fill=tt_color)
                offset += true_font_size + 1.2
            offset += true_font_size + word_space
        self.draw_image_author(draw, author, H*au_top, W*au_left, auth_color, style)
        img_path = os.path.join('.', 'output', 'test_center.png')
        file.save('./output/%s_test_vertical_%s.png' % (fn, style))

    def draw_image_option_author(self, draw, author, top, left, font_fill, style, init_size):
        author = author.split(' ')
        if init_size > 75:
            init_size = 75
        true_font_size, word_space = init_size, 1.5
        font = ImageFont.truetype('FONT.TTF', true_font_size)
        margin, offset = left, top

        res = font.getmask(author[0]).getbbox()
        en_word_width = (res[2] - res[0]) + word_space
        if style == 'center':
            margin += (800 - en_word_width) // 2
        draw.text((margin, offset), author[0], font=font, fill=font_fill)
        margin += en_word_width
        for word in author[1:]:
            draw.text((margin, offset), word, font=font, fill=font_fill)
            res = font.getmask(word).getbbox()
            en_word_width = res[2] - res[0]
            margin += en_word_width

    def draw_image_author(self, draw, author, top, left, font_fill, style):
        init_size = 75
        author_limit = 800 // init_size
        rect_size = 800 // author_limit
        font = ImageFont.truetype('FONT.TTF', init_size)
        true_font_size, word_space = init_size, rect_size - init_size
        font = ImageFont.truetype('FONT.TTF', true_font_size)
        ellipsis = None
        margin, offset = left, top
        if self.is_all_chinese(author):
            if len(author) > author_limit:
                author = author[:author_limit]
                ellipsis = '...'
            if style == 'center':
                word_width = true_font_size*len(author)
                margin += (800-word_width) // 2
            draw.text((margin, offset), author[0], font=font, fill=font_fill)
            margin += true_font_size
            for word in author[1:]:
                draw.text((margin, offset), word, font=font, fill=font_fill)
                margin += true_font_size
        else:
            author = author.split(' ')
            if len(author) > author_limit:
                author = author[:author_limit-1]
                ellipsis = '...'
            res = font.getmask(author[0]).getbbox()
            en_word_width = (res[2] - res[0])*len(author)
            if style == 'center':
                margin += (800-en_word_width) // 2
            draw.text((margin, offset), author[0], font=font, fill=font_fill)
            margin += en_word_width
            for word in author[1:]:
                draw.text((margin, offset), word, font=font, fill=font_fill)
                res = font.getmask(word).getbbox()
                en_word_width = res[2] - res[0]
                margin += en_word_width
        # if ellipsis:
        #     font = ImageFont.truetype('FONT.TTF', init_size)
        #     (width, baseline), (offset_x, offset_y) = font.font.getsize(ellipsis)
        #     offset -= offset_y // 2
        #     for elli in ellipsis:
        #         draw.text((margin, offset), elli, font=font, fill="#7B99CC")
        #         margin += offset_y // 2

    def set_mix_font_size(self, img, fn, text):
        W, H = img.size
        height_fraction, width_fraction = 0.2, 0.8
        height_limit, width_limit = int(height_fraction * H), int(width_fraction * W)
        line = 1
        font_size = height_limit
        text = text.split(' ')
        text_num = len(text)
        if fn == 'en':
            font_size = width_limit // text_num

        elif fn == 'mix':
            text_containers = []
            for word in text:
                if self.is_all_en(word):
                    text_containers.append(word)
                else:
                    for zh_word in word:
                        text_containers.append(zh_word)
            text = text_containers
            text_num = len(text)
            font_size = width_limit // text_num
        elif fn == 'digit':
            text_containers = []
            for word in text:
                temp = ''
                if word.isnumeric():
                    temp += word
                else:
                    if temp:
                        text_containers.append(temp)
                    text_containers.append(word)
            text = text_containers
            font_size = width_limit // text_num
        fit_size = 13
        font = ImageFont.truetype('FONT.TTF', fit_size)
        sum_width = 0
        for word in text:
            rectangle = font.getmask(word).getbbox()
            sum_width += rectangle[2] - rectangle[0]
        while sum_width < width_limit:
            sum_width = 0
            fit_size += 1
            font = ImageFont.truetype('FONT.TTF', fit_size)
            for word in text:
                rectangle = font.getmask(word).getbbox()
                sum_width += rectangle[2] - rectangle[0]
        fit_size -= 1
        font = ImageFont.truetype('FONT.TTF', fit_size)
        sum_width = 0
        for word in text:
            rectangle = font.getmask(word).getbbox()
            sum_width += rectangle[2] - rectangle[0]
        true_font_size, word_space = fit_size, (width_limit - sum_width) // text_num
        return font, true_font_size, word_space, text_num, text

    def draw_option_sec(self, image, fn, title, author, top, left,
                         au_top, au_left, style='left', tt_color='#FFFFFF', auth_color='#FFFFFF'):
        if fn in ('en', 'mix', 'digit'):
            text = title
            file = Image.open(image).convert('RGB')
            W, H = file.size
            font, true_font_size, word_space, width_num, text = self.set_mix_font_size(file, fn, text)
            draw = ImageDraw.Draw(file)
            offset = H*top
            if style == 'left':
                margin = W * left
            elif style == 'center':
                margin = 100 + (int(W * 0.8) - (true_font_size + word_space)) // 2
            else:
                margin = W * left

            draw.text((margin, offset), text[0], font=font, fill=tt_color)

            ret = font.getmask(text[0]).getbbox()
            margin += ret[2] - ret[0] + word_space
            for e_word in text[1:]:
                draw.text((margin, offset), e_word, font=font, fill=tt_color)
                rectangle = font.getmask(e_word).getbbox()
                margin += rectangle[2] - rectangle[0] + word_space
            self.draw_image_option_author(draw, author, H * au_top, W * au_left, auth_color, style, true_font_size)
            img_path = os.path.join('.', 'output', 'test_center.png')
            file.save('./output/%s_test_option2_horizon_%s.png' % (fn, style))

    def is_all_chinese(self, strs):
        for i in strs:
            if not '\u4e00' <= i <= '\u9fa5':
                return False
        return True

    def is_all_en(self, strs):
        for i in strs:
            if '\u4e00' <= i <= '\u9fa5':
                return False
        return True


if __name__ == '__main__':
    for fn, title, author in [
        ('long', '谋杀我的完美完美完美完美完美完美偶像偶像', '作者很长长长长长长长长长长长长'),
        ('medium', '浮城旧梦', '小米贝贝'),
        ('short', '沉默', 'Yohi'),

        # # 选做项1: 避免违反排版规则的标点符号出现在行首
        # ('punctuation', '试管医，手记！八细胞：承诺（完整版）', '小米贝贝'),
        #
        # 选做项2: 纯英文、中英文数字混排
        ('en', 'Fantastic Beasts: The Crimes of Grindelwald', 'J.K. Rowling'),
        ('mix', 'The Lost Stars: 云都', '风倾'),
        ('digit', '逃离20岁', '小米贝贝')
    ]:
        processImg().draw_horizon_img('1.png', fn, title, author, 0.6, 0.1, 0.85, 0.1,
                                      style='left', tt_color='#CBDEFF', auth_color='#7B99CC')
        processImg().draw_vertical_img('2.png', fn, title, author, 0.1, 0.6, 0.9, 0.1,
                                       style='left', tt_color='#21397C', auth_color='#FFFFFF')
        processImg().draw_horizon_img('3.png', fn, title, author, 0.2, 0.1, 0.9, 0.1,
                                      style='center', tt_color='#AED0DC', auth_color='#203940')
        processImg().draw_vertical_img('4.png', fn, title, author, 0.1, 0.35, 0.9, 0.1,
                                       style='center', tt_color='#C2C2C2', auth_color='#A6A6A6')
        processImg().draw_option_sec('1.png', fn, title, author, 0.6, 0.1, 0.85, 0.1,
                                     style='left', tt_color='#CBDEFF', auth_color='#7B99CC')
