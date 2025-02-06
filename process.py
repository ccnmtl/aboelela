import csv
import os
import re


def find_nth(haystack: str, needle: str, n: int) -> int:
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start


def sanitize(func, filename):
    """
    Modify a file with the the function provided.
    """
    body = None
    with open(filename, 'r', encoding='utf-8') as file:
        body = file.read()
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(func(body))


def getFilename(name: str) -> str:
    """
    Get the target file name
    """
    return next(x for x in os.listdir('data') if name.lower() in x.lower())


def sanitizeIDs(ids):
    """
    Sanitize the data from the ID file. Sanitization is file specific and
    likely needs to be refactored later for more general use
    """
    id_set = {}
    for id in ids:
        if id.get('UNI (ID)') and id['UNI (ID)'] == 'Item ID / Rev':
            i = 1
            key = 'Q1'
            while id.get(key):
                id_set[key] = id[key].split('/')[0].strip()
                i += 1
                key = f'Q{i}'
            return id_set


def sanitizeItems():
    """
    Sanitize the data from the Items file. Sanitization if file specific and
    likely needs to be refactored later for more general use.
    """
    with open(f'data/{getFilename("item")}', 'r',
              encoding='utf-8') as file:
        tables = [
            'Item #' + x for x in file.read().split('Item #') if len(x) > 0]
        print('Tables Found:', len(tables))
        clean = {}
        count = {}

        for table in tables:
            items = csv.DictReader(table.splitlines())
            for item in items:
                if item['Item #'].isnumeric():
                    print('Item #', item['Item #'])
                    # Clean up the categories
                    categories = [
                        x.strip() for x in item['Categories'].split(',')]
                    bloom = ''
                    subcategory = ''

                    for category in categories:
                        # Find highest bloom level
                        if 'Bloom' in category:
                            clean_cat = category.title()
                            if clean_cat > bloom:
                                bloom = clean_cat
                        # Find the subcategory
                        elif len(category) > len(subcategory):
                            subcategory = category

                # Drop unnecessary columns
                # Reformat category as "Bloom Level, Category/Subcategory"
                if subcategory != '' and bloom != '':
                    short_bloom = bloom[
                        re.search(r'.loom.{1,3}evel', bloom).start():]
                    bloom_parts = short_bloom.split(' - ')
                    bloom_parts[1] = re.sub(' ', '', bloom_parts[1])
                    short_bloom = ' - '.join(bloom_parts)
                    print(item['ItemID'], '\t', short_bloom)
                    short_cat = subcategory[find_nth(subcategory, '/', 2) + 1:]
                    cat = ', '.join([short_bloom.title(), short_cat])
                    clean[item['ItemID']] = cat
                    if cat not in count:
                        count[cat] = 2
                    else:
                        count[cat] += 2
        return clean, count


def main():
    for file in [x for x in os.listdir('data') if x[-4:] == '.csv']:
        print(f' -- Sanitizing {file}...')
        sanitize(lambda x: re.sub(r'⁄', '/', x), f'data/{file}')
        if 'result' in file.lower():
            sanitize(lambda x: ''.join(
                re.sub(r' ?[^\w\s\(\),/\-<>\*\?%]', '', x)), f'data/{file}')
        elif 'item' in file.lower():
            sanitize(lambda x: x[x.find('Item #'):], f'data/{file}')
    # Sanitize Item data
    items, cat_count = sanitizeItems()
    print('Number of Questions:', len(items))
    print('Category Count:', len(cat_count))

    # Open the results file and return the DictReader
    with open(f'data/{getFilename("results")}', 'r',
              encoding='utf-8') as file:
        results = csv.DictReader(file)
        item_dir = sanitizeIDs(results)
        print(item_dir)
        print('Item Directory Size:', len(item_dir))

        # Process the results into a new CSV
        with open('results/processed.csv', 'w') as file:
            # Write the header
            header = ['UNI (ID)', 'Category', 'Max Score', 'Student Score',
                      '% Correct']
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()

            # Accumulate the data for each student
            for row in results:
                if row['UNI (ID)']:
                    out_data = {}
                    categories = {}

                    # Iterate through the questions to get the category scores
                    for key in item_dir:
                        category = items[item_dir[key]]
                        if category not in categories:
                            categories[category] = 0
                        try:
                            categories[category] += int(row[f'{key} Pts'])
                        except ValueError:
                            pass

                    # Check for consistent category length
                    if len(cat_count) != len(categories):
                        print('Inconsistent category length for (',
                              row['UNI (ID)'], '\t', len(categories), ')')

                    # Write the row to the file
                    for category in categories:
                        out_data['UNI (ID)'] = row['UNI (ID)']
                        out_data['Category'] = category
                        out_data['Max Score'] = cat_count[category]
                        out_data['Student Score'] = categories[category]
                        percentage = int(
                            categories[category] / cat_count[category] * 100)
                        out_data['% Correct'] = f'{percentage}%'
                        writer.writerow(out_data)


if __name__ == '__main__':
    main()
