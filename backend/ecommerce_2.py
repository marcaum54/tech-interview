import json


class Ecommerce:
    def __init__(self, level=None):
        self.loaded_json = None

        if level:
            with open(__class__.__get_file_from_level(level)) as file_content:
                self.loaded_json = json.load(file_content)

    @staticmethod
    def __get_file_from_level(level):
        import os.path
        file = "{0}{1}level{2}/data.json".format(os.path.dirname(__file__), os.path.sep, level)
        if not os.path.isfile(file):
            raise Exception("Level ({}) Don't exists".format(level))

        return file

    def get_loaded_json(self):
        return self.loaded_json

    def get_articles(self):
        return self.get_loaded_json().get('articles', [])

    def get_article_by_id(self, id):
        for article in self.get_articles():
            if article.get('id') == id:
                return article

        return None

    def get_carts(self):
        return self.get_loaded_json().get('carts', [])

    def get_cart_by_id(self, id):
        for cart in self.get_carts():
            if cart.get('id') == id:
                return cart

        return None

    def calculate_output(self):
        output = {'carts': []}

        for cart in self.get_carts():
            total = 0

            for item in cart.get('items'):
                article = self.get_article_by_id(item.get('article_id'))
                if article:
                    total += article.get('price') * item.get('quantity')

            output.get('carts').append({'id': cart.get('id'), 'total': total})

        return output

    def toJSON(self):
        return json.dumps(self.calculate_output())

cart = Ecommerce(level=1)
cart.calculate_output()