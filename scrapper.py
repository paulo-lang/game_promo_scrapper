from bs4 import BeautifulSoup
from requests_html import HTMLSession

#with open('./pages_test/steam.html', encoding='utf-8') as page:
#    soup = BeautifulSoup(page, 'html.parser')

session = HTMLSession()
url = 'https://store.steampowered.com/specials?offset=24'
r = session.get(url)

r.html.render(sleep=5, scrolldown=15)

soup = BeautifulSoup(r.html.raw_html, 'html.parser')
#with open('steam_page.html', 'w', encoding='utf-8') as file:
#    file.write(request.text)
offersId = 'SaleSection_13268'
itemClass = 'ImpressionTrackedElement'

offers = soup.find(id=offersId)
offersProducts = offers.findAll(class_=itemClass)
products = []

for product in offersProducts:
    #productId = product['data-ds-appid']

    productImage = product.find('img')['src']

    productInfo = product.div.div.div.find_next_sibling('div')

    productTitle = productInfo.div.find_next_sibling('div').text
    productPriceInfo = productInfo.div.find_next_sibling('div').find_next_sibling('div').find_next_sibling('div').find_next_sibling('div').div

    isProductFree = product.find(string='Grátis para Jogar')
    productPrice = 0
    productLastPrice = 0
    productDiscount = 0

    if isProductFree:
        isProductFree = True
    else:
        isProductFree = False
        productPrice = productPriceInfo.div.find_next_sibling('div').div.find_next_sibling('div').div.find_next_sibling('div').text
        productPrice = float(productPrice.replace('R$', '').replace(',', '.'))
        productHasLastPrice = productPriceInfo.div.find_next_sibling('div').div.find_next_sibling('div').div
        if productHasLastPrice:
            productLastPrice = productHasLastPrice.text
            productLastPrice = float(productLastPrice.replace('R$', '').replace(',', '.'))
            productDiscount = productPriceInfo.div.find_next_sibling('div').div.text
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


print(products)