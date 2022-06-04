from bs4 import BeautifulSoup
import requests
import re

search_term = input('what product do you want to search: ')
a = search_term.split(' ')
space = '%20'
new_search = space.join(a)
url = f"https://www.bukalapak.com/products?search%5Bkeywords%5D={new_search}"
print(url)
req = requests.get(url)
doc = BeautifulSoup(req.text, 'html.parser')

page_bar = doc.find_all(class_='bl-pagination__link')

last_page = page_bar[-1].string

num_of_last_page = last_page.split('\n')
num_of_it = num_of_last_page[1].split(' ')
last_num = num_of_it[-1]
real_page_num = int(last_num)
# finding the correct page num (this was hard)
items_found = {}
print(f"there are {real_page_num} page(s) of {search_term}")

for page in range(1, real_page_num + 1):
    url = f'https://www.bukalapak.com/products?page={page}&search%5Bkeywords%5D={new_search}'
    req = requests.get(url).text
    doc = BeautifulSoup(req, 'html.parser')
    div = doc.find(class_='bl-flex-container flex-wrap is-gutter-16')
    items = div.find_all(text=re.compile(search_term.upper()))  # finding name
    for item in items:
        parent = item.parent
        if parent.name != 'a':
            continue

        link = parent['href']
        next_parent = item.find_parent(class_='bl-product-card te-product-card')  # finding the product card
        price_not_yet = next_parent.find(class_='bl-product-card__description-price').p.string  # finding price
        actual_price_almost = price_not_yet.split(' ')
        one_more = actual_price_almost[10].split('\n')
        price = one_more[0]

        name_item_not = next_parent.find(class_='bl-product-card__description-name').a.string
        now_string = name_item_not.split('\n')
        not_again = now_string[1]
        items_found[item] = {'price': price, 'link': link}

sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])


if __name__ == '__main__':
    for item in sorted_items:
        print(item[0])
        print(f"{item[1]['price']}")
        print(item[1]['link'])
        print('-------------------------------')
