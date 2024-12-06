import csv
import os
import re
from sanitize import sanitize


def find_nth(haystack: str, needle: str, n: int) -> int:
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start


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
        if id['UNI (ID)'] == 'Item ID / Rev':
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
              encoding='utf-8-sig') as file:
        items = csv.DictReader(file)
        clean = {}
        count = {}

        for item in items:
            # Clean up the categories
            categories = [x.strip() for x in item['Categories'].split(',')]
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
                short_bloom = bloom[re.search(r'.loom..evel', bloom).start():]
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
        if 'result' in file.lower():
            sanitize(lambda x: ''.join(re.sub(r' †', '', x)), f'data/{file}')
        elif 'item' in file.lower():
            sanitize(lambda x: x[x.find('Item #'):], f'data/{file}')
    # Sanitize Item data
    items, cat_count = sanitizeItems()
    print('Number of Questions:', len(items))
    print('Category Count:', len(cat_count))

    # Open the results file and return the DictReader
    with open(f'data/{getFilename("results")}', 'r',
              encoding='utf-8-sig') as file:
        results = csv.DictReader(file)
        item_dir = sanitizeIDs(results)

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
                              row['UNI (ID)'], ')')

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
