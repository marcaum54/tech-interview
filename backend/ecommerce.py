import json


class Ecommerce:
    class Article:
        def __init__(self, article, quantity):
            self._id = article.get('id')
            self._name = article.get('name')
            self._price = article.get('price')
            self._quantity = quantity

        def get_id(self):
            return self._id

        def get_name(self):
            return self._name

        def get_price(self):
            return self._price

        def get_quantity(self):
            return self._quantity

        def total(self):
            return self._price * self._quantity

    class Cart:
        def __init__(self, cart):
            self._id = cart.get('id')
            self._articles = []

        def get_id(self):
            return self._id

        def get_articles(self):
            return self._articles

        def add_article(self, article):
            self._articles.append(article)

        def total(self):
            total = 0
            for article in self.get_articles():
                total += article.total()
            return total

    def __init__(self, level=None):
        self.loaded_json = None
        self._carts = []

        if level:
            with open(__class__.__get_file_from_level(level)) as file_content:
                self.loaded_json = json.load(file_content)

                for cart in self.loaded_json.get('carts', []):
                    new_cart = __class__.Cart(cart)

                    for item in cart.get('items'):
                        article = None
                        for art in self.loaded_json.get('articles', []):
                            if art.get('id') == item.get('article_id'):
                                article = art
                                continue

                        if article:
                            quantity = item.get('quantity')
                            new_cart.add_article(__class__.Article(article, quantity))

                    self._carts.append(new_cart)

    @staticmethod
    def __get_file_from_level(level):
        import os.path
        file = "{0}{1}level{2}/data.json".format(os.path.dirname(__file__), os.path.sep, level)
        if not os.path.isfile(file):
            raise Exception("Level ({}) Don't exists".format(level))

        return file

    def get_carts(self):
        return self._carts

    def calculate_output(self):
        output = {'carts': []}
        for cart in self.get_carts():
            output.get('carts').append({'id': cart.get_id(), 'total': cart.total()})
        return output

    def to_json(self):
        return json.dumps(self.calculate_output())


ecommerce = Ecommerce(level=1)
ecommerce.to_json()