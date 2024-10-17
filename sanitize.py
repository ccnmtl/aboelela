import re
import os


def sanitize(func, filename):
    body = None
    with open(filename, 'r', encoding='utf-8-sig') as file:
        body = file.read()
    with open(filename, 'w', encoding='utf-8-sig') as file:
        file.write(func(body))


if __name__ == '__main__':
    for file in os.listdir('data'):
        print(f'\tSanitizing {file}...')
        if 'result' in file.lower():
            sanitize(lambda x: ''.join(re.sub(r' †', '', x)), f'data/{file}')
        elif 'item' in file.lower():
            sanitize(lambda x: x[x.find('Item #'):], f'data/{file}')
