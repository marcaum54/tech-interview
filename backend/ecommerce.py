import json


class Ecommerce:
    class Article:
        def __init__(self, article, quantity, discount):
            self._id = article.get('id')
            self._name = article.get('name')
            self._price = article.get('price')
            self._quantity = quantity
            self._discount = discount

        def total(self):
            return self._price * self._quantity

        def calculate_discount(self):
            if self._discount is not None:
                if self._discount.get('type') == 'amount':
                    return self._quantity * self._discount.get('value')
                if self._discount.get('type') == 'percentage':
                    return self.total() * self._discount.get('value') / 100

            return 0

    class Cart:
        def __init__(self, cart):
            self._id = cart.get('id')
            self._articles = []

        def get_id(self):
            return self._id

        def add_article(self, article):
            self._articles.append(article)

        def total(self):
            total = 0
            for article in self._articles:
                total += article.total()
            return total

        def calculate_discounts(self):
            discounts_calculated = 0
            for article in self._articles:
                discounts_calculated += article.calculate_discount()
            return discounts_calculated

    def __init__(self, level):
        self._carts = []
        self._loaded_json = None

        with open(__class__._get_path_file_by_level(level)) as file_content:
            self._loaded_json = json.load(file_content)
            self._discounts = self._loaded_json.get('discounts', [])
            self._delivery_fees = self._loaded_json.get('delivery_fees', [])

            for cart in self._loaded_json.get('carts', []):
                new_cart = __class__.Cart(cart)

                for item in cart.get('items'):
                    article = self._get_article_by_id(id=item.get('article_id'))
                    if article:
                        quantity = item.get('quantity')
                        discount = self._get_discount_by_article(article.get('id'))
                        new_cart.add_article(__class__.Article(article, quantity, discount))

                self._carts.append(new_cart)

    @staticmethod
    def _get_path_file_by_level(level):
        import os.path
        file = "{}/data.json".format(level)
        if not os.path.isfile(file):
            raise Exception("Level ({}) Don't exists".format(level))

        return file

    def _get_article_by_id(self, id):
        for art in self._loaded_json.get('articles', []):
            if art.get('id') == id:
                return art
        return None

    def _get_discount_by_article(self, article_id):
        for discount in self._discounts:
            if discount.get('article_id') == article_id:
                return discount
        return None

    def calculate_delivery_fees(self, total):
        for delivery_fee in self._delivery_fees:
            eligible_transaction_volume = delivery_fee.get('eligible_transaction_volume')

            min_price = eligible_transaction_volume.get('min_price')
            max_price = eligible_transaction_volume.get('max_price')

            has_min_price = min_price is not None
            has_max_price = max_price is not None

            with_both_prices = has_min_price and has_max_price and min_price <= total < max_price
            only_max_price = not has_max_price and min_price <= total

            if with_both_prices or only_max_price:
                return delivery_fee.get('price')

        return 0

    def create_output(self):
        output = {'carts': []}

        for cart in self._carts:
            cart_total = cart.total() - cart.calculate_discounts()
            delivery_fees_calculated = self.calculate_delivery_fees(total=cart_total)

            output.get('carts').append({'id': cart.get_id(), 'total': cart_total + delivery_fees_calculated})

        return output

    def to_json(self):
        return json.dumps(self.create_output(), indent=2)


if __name__ == '__main__':
    import sys
    if not sys.argv[1]:
        raise Exception('Enter with a the desired level')

    print(Ecommerce(level=sys.argv[1]).to_json())
