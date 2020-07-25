class PointAction(object):
    def __init__(self, user):
        self.user = user

    def accumulate(self, amount, **kwargs):
        pass

    def accumulate_by_order(self, order):
        pass

    def use(self, coupon, amount):
        pass

    def cancel(self):
        pass

    def withdraw(self):
        pass

    def points(self, expire=False):
        pass

    def logs(self, order, cateogry=None):
        pass

    def amount(self):
        pass

    def will_expire_amount(self):
        pass

    def debt_amount(reverse_order):
        pass

    def withdraw_point(self, reverse_order):
        pass

    def debt_point(self, reverse_order):
        pass
