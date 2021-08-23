from books.models import Book
from decimal import Decimal

CART_SESSION_ID = 'cart'


class Cart:
    """کلاس cart شامل متدهایی برای اضافه کردن و حذف کردن ار سبذ خرید میباشد / مقادیر را در session سبذ دخیره میکند"""
    def __init__(self, request):
        """طبق درخواست (request) انحام شده session های مربوط به سبد را ذخیره میکند """
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """ار این قسمت برای قابل iterable کردن cart و قابل حلقه زدن در صفحه detail.html است """
        book_ids = self.cart.keys()
        """کلیدهای کارت که همان آی دی کتاب انتخاب شده میباشد را برمیگرداند"""
        books = Book.objects.filter(id__in=book_ids)
        cart = self.cart.copy()
        for book in books:
            cart[str(book.id)]['book'] = book
            cart[str(book.id)]['discount'] = book.get_item_discount()

        for item in cart.values():
            """قیمت کل هر ردیف از سبد را حساب میکند"""
            item['total_price'] = Decimal(item['price']) * item['quantity'] - Decimal(item['discount'])
            yield item

    def add(self, book, quantity):
        """کتاب و تعداد آن را به سبد اضافه میکند"""
        book_id = str(book.id)
        if book_id not in self.cart:
            """اگر محصول در سبد خرید نبود یک session  از آن میسازد"""
            self.cart[book_id] = {'quantity': 0, 'price': str(book.price)}
            """اگر محصول در سبد خرید بود تعداد آن را اضافه میکند"""
        self.cart[book_id]['quantity'] += quantity
        self.save()

    def remove(self, book):
        """برای حذف تک تک آیتم های سبد خرید"""
        book_id = str(book.id)
        quantity = self.cart[book_id]['quantity']
        if book_id in self.cart:
            del self.cart[book_id]
            book.add_stock(quantity)
            self.save()

    def save(self):
        """برای ذخیره تغییر تعداد کتاب در سبد (quantity) """
        self.session.modified = True

    def get_final_price(self):
        """قیمت کل سبد را حساب میکند"""
        return sum(Decimal(item['price']) * item['quantity'] - Decimal(item['discount']) for item in self.cart.values())

    def clear(self):
        """کل سبذ را پاک میکند"""
        del self.session[CART_SESSION_ID]
        self.save()
