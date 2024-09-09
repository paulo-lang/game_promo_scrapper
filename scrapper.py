from bs4 import BeautifulSoup
import requests

#with open('./pages_test/steam.html', encoding='utf-8') as page:
#    soup = BeautifulSoup(page, 'html.parser')

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
request = requests.get('https://store.steampowered.com/?l=portuguese', headers=headers)
with open('steam_page.html', 'w', encoding='utf-8') as file:
    file.write(request.text)
soup = BeautifulSoup(request.text, 'html.parser')

offersId = 'tab_specials_content'
itemClass = 'tab_item'

offers = soup.find(id=offersId)
offersProducts = offers.findAll(class_=itemClass)
print(soup.find(string=''))
products = []

for product in offersProducts:
    productId = product['data-ds-appid']

    productImage = product.find(class_='tab_item_cap_img')['src']

    productTitle = product.find(class_='tab_item_name').text
    productPriceInfo = product.find(class_='discount_block')

    isProductFree = product.find(string='Grátis para Jogar')
    productPrice = 0
    productLastPrice = 0
    productDiscount = 0

    if isProductFree:
        isProductFree = True
    else:
        isProductFree = False
        productPrice = productPriceInfo.find(class_='discount_final_price').text
        productPrice = float(productPrice.replace('R$', '').replace(',', '.'))
        productHasLastPrice = productPriceInfo.find(class_='discount_original_price')
        if productHasLastPrice:
            productLastPrice = productHasLastPrice.text
            productLastPrice = float(productLastPrice.replace('R$', '').replace(',', '.'))
            productDiscount = productPriceInfo.find(class_='discount_pct').text
            productDiscount = int(productDiscount.replace('%', '').replace('-', ''))
        else:
            productLastPrice = productPrice

    product = {
        'title': productTitle,
        'price': productPrice,
        'lastPrice': productLastPrice,
        'discount': productDiscount,
        'isFree': isProductFree,
        'image': productImage
    }

    products.append(product)


#print(products)