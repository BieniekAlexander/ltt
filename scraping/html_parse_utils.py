#%% imports
import sys, os
from bs4 import BeautifulSoup, Tag, NavigableString

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.data_structure_utils import list_pop_adjacent_same_values, dict_key_list_assign, flatten_dict_keys, split_dict_vals


#%% utils
def bs_clone(el):
    """
    Function that safely clones BeautifulSoup elements.

    Deepcopy produces infinite recursion, so we need this function to achive the deepcopy functionality.
    """
    # https://www.generacodice.com/en/articolo/2268593/clone+element+with+beautifulsoup
    if isinstance(el, NavigableString):
        return type(el)(el)

    copy = Tag(None, el.builder, el.name, el.namespace, el.nsprefix)
    # work around bug where there is no builder set
    # https://bugs.launchpad.net/beautifulsoup/+bug/1307471
    copy.attrs = dict(el.attrs)
    for attr in ('can_be_empty_element', 'hidden'):
        setattr(copy, attr, getattr(el, attr))
    for child in el.contents:
        copy.append(bs_clone(child))
    return copy


def bs_minify(el):
    """
    Helper that recusively removes whitespace children from a BeautifulSoup tree.
    """
    if isinstance(el, Tag):
        for item in list(el.children):
            bs_minify(item)
    elif isinstance(el, NavigableString) and el == '\n':
        el.extract()

    return el


def insert_table_element(table, row_idx, col_idx, element):
    """
    Helper function that inserts an element into a BeautifulSoup table by index.
    """
    table.find_all('tr')[row_idx].insert(col_idx, element)


def spread_table_spans(table):
    """
    Helper function that duplicates out table cells that span multiple rows and columns.

    Note: in some tables, header rowspans on the right side exceed the width of the contents.
    TODO maybe add a note on how the header row sometimes has too many elements
    """
    # spread the colspan items
    dc_table = bs_clone(table)
    rows = dc_table.find_all('tr')
    
    for i in range(len(rows)):
        row = rows[i]
        children = row.find_all(['td', 'th'])
        j = 0
        
        while (j < len(children)):
            child = children[j]

            if child.has_attr('colspan'):
                colspan = int(child['colspan'])
                del child['colspan']

                for _ in range(colspan-1):
                    child_clone = bs_clone(child)
                    insert_table_element(dc_table, i, j, child_clone)
                    j+=1

                children = row.find_all()

            j += 1

    # spread the rowspan items
    rows = dc_table.find_all('tr')
    
    for i in range(len(rows)):
        row = rows[i]
        children = row.find_all(['td', 'th'])
        
        for j in range(len(children)):
            child = children[j]

            if child.has_attr('rowspan'):
                rowspan = int(child['rowspan'])
                del child['rowspan']

                for k in range(rowspan-1):
                    child_clone = bs_clone(child)
                    insert_table_element(dc_table, i+k+1, j, child_clone)

    return dc_table


def get_table_col_headers(table):
    """
    Gets the lists of column headers for the table.

    TODO maybe add visual notes on how this works.
    """
    # discover the number and depth of the column header rows
    col_header_rows = []
    rows = table.find_all('tr')

    for i in range(len(rows)):
        row = rows[i]

        if row.find('td') != None:
            n_header_rows = i
            col_padding = len(row.find_all('th'))
            break

    for row in rows[:n_header_rows]:
        col_header_row = [header.text.strip() for header in row.find_all('th')[col_padding:]]
        col_header_row = list(map(lambda x: x.replace(u'\xa0', u' '), col_header_row))
        col_header_rows.append(col_header_row)

    return col_header_rows


def get_table_row_headers(table):
    """
    Gets the lists of row headers for the table.

    TODO maybe add visual notes on how this works.
    """
    # discover the number and width of the row header rows
    row_header_cols = []
    rows = table.find_all('tr')

    for i in range(len(rows)):
        row = rows[i]

        if row.find('td') != None:
            n_header_rows = i
            break

    for row in rows[n_header_rows:]:
        headers = row.find_all('th')
        
        for (i, header) in enumerate(headers):
            text = header.text.strip()
            text = text.replace(u'\xa0', u' ') # replace '&nbsp;' (no break space) 
        
            if len(row_header_cols) <= i:
                row_header_cols.append([])

            row_header_cols[i].append(text)

    return row_header_cols


def get_table_data(table):
    """
    Gets all of the data from the table as a list of rows.
    """
    data_rows = []
    rows = table.find_all('tr')
    
    for row in rows:
        data = row.find_all('td')
        
        if data:
            data_rows.append([datum.text.strip() for datum in data])

    return data_rows


def parse_inflection_table(table):
    """
    Parse and read header and cell data from the table, and return a dictionary mapping headers to cells.
    """
    if type(table) != Tag or table.name != 'table':
        raise ValueError("Input must be an HTML table")

    table = bs_minify(table)
    table = spread_table_spans(table)
    row_headers = get_table_row_headers(table)
    col_headers = get_table_col_headers(table)
    table_data = get_table_data(table)

    parsed = {}

    col_header_tuples = list(zip(*col_headers))
    row_header_tuples = list(zip(*row_headers))

    for i in range(len(row_header_tuples)):
        for j in range(len(col_header_tuples)):
            keys = list(col_header_tuples[j]+row_header_tuples[i])
            list_pop_adjacent_same_values(keys)
            dict_key_list_assign(parsed, keys, table_data[i][j])

    parsed = flatten_dict_keys(parsed)
    parsed = split_dict_vals(parsed)
    return parsed


#%% main
def main():
    html = open('tests/scraping/data/czerwony_inflections.html').read()
    soup = BeautifulSoup(html, "html.parser")
    table = soup.table
    parsed = parse_inflection_table(table)
    print(parsed)


if __name__ == "__main__":
    main()