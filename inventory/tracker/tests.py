"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
from datetime import timedelta, date

from django.test import TestCase

from inventory.tracker.models import Product, Movement

class SimpleTest(TestCase):
    def test_basic_models(self):
        p, _ = Product.objects.get_or_create(code='0001',
            name='Pendrive Kingston 2GB')

        three_days_ago = date.today() - timedelta(3)
        two_days_ago = date.today() - timedelta(2)
        yesterday = date.today() - timedelta(1)
        today = date.today()
        tomorrow = date.today() + timedelta(1)

        # 3 days ago 10 units came
        Movement.objects.create(product=p, day=three_days_ago, qty=10)
        # 2 days ago 5 were selled
        Movement.objects.create(product=p, day=two_days_ago, qty=-5)
        # yesterday 5 more were selled
        Movement.objects.create(product=p, day=yesterday, qty=-5)
        # today we have 30
        p.update_qty(30)
        # the tests: At the begining of the day, 3 days ago, we had 0
        self.failUnlessEqual(p.qty_on(three_days_ago), 0)
        # 2 days ago we had the 10 that came 3 days ago
        self.failUnlessEqual(p.qty_on(two_days_ago), 10)
        # yesterday we had 5 (5 were selled 2 days ago)
        self.failUnlessEqual(p.qty_on(yesterday), 5)
        # today we have 0 (5 more were selled yesterday)
        self.failUnlessEqual(p.qty_on(today), 0)
        # tomorrow we'll have 30 (the 30 that were added today)
        self.failUnlessEqual(p.qty_on(tomorrow), 30)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

