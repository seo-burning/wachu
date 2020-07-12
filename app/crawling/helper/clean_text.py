import re


def get_cleaned_text(text):
    text = text.lower().replace(' ', '').replace('(', '').replace(')', '').replace(':', '').replace('eodưới', '').replace(
        'dưới', '').replace('dưới', '').replace('<', '').replace('kg', '').replace('cm', '').replace('size', '').replace('szie', '').replace(
            'sz', '').replace('mau', '').replace('màu', '').replace('mẫu', '').replace('color', '').replace('-', '').replace(
                '_', '').replace('kí', '').replace('#', '').strip()
    return text


def get_cleaned_text_from_pattern(text):
    text = text.lower().replace('hoa', '').replace('caro', '').replace('hoạ', '').replace(
        'họa', '').replace('tiet', '').replace('tiết', '').replace('ke', '').replace(
            'kẻ', '').replace('checked', '').replace('chấmbi', '').replace(
                'sọc', '').replace('printed', '').replace('logo', '').replace('bông', '').replace('floral', '').replace('patterned', '')
    return text


def get_cleaned_text_from_category(text):
    text = text.lower().replace('áo', '').replace('quan', '').replace('quần', '').replace('set', '').replace(
        'jogger', '').replace('hoodie', '').replace('jeans', '').replace('jean', '').replace(
            'túi', '').replace('dây', '').replace('khoác', '').replace('balo', '').replace('sơmi', '').replace(
                'blazer', '').replace('chânváy', '').replace('bag', '').replace('trouser', '').replace('balo', '')
    return text


def get_cleaned_text_from_color(text):
    text = text.lower().replace('black', '').replace('white', '').replace('đen', '').replace('trắng', '').replace('cam', '')
    return text


def get_cleaned_text_from_size(text):
    text = text.lower().replace('xl', '').replace('xxl', '').replace('free', '').strip()
    if text[-1:] == 'l' or text[-1:] == 'm' or text[-1:] == 's':
        text = text[:-1]
    try:
        print(int(text[-3:]))
        text = text[:-3]
    except:
        pass
    try:
        print(int(text[-2:]))
        text = text[:-2]
    except:
        pass
    try:
        print(int(text[-1:]))
        text = text[:-1]
    except:
        pass
    return text


def remove_html_tags(text):
    text = text.replace('</p>', '\n')
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)
    return text
