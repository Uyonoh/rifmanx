from django.db import models
from django.utils import timezone as tz
from drugs.models import Drug

# Create your models here.

class Credit(models.Model):
    """ Records of all crediting transactions """

    item = models.CharField(max_length=100)
    amount = models.IntegerField()
    price = models.FloatField()
    date = models.DateField(default=tz.now)

    def __str__(self) -> str:
        return f"Credit for {self.item}"


class Debit(models.Model):
    """ Records of all debiting transactions """

    item = models.CharField(max_length=100)
    amount = models.IntegerField()
    price = models.FloatField()
    date = models.DateField(default=tz.now)

    def __str__(self) -> str:
        return f"Debit for {self.item}"


class Sale(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    amount = models.IntegerField()
    price = models.FloatField()
    time = models.DateTimeField(default=tz.now)

    def save(self, *args, **kwargs) -> None:
        item_set = self.drug.get_item_set() # Itemset is currently ony a single (first) item
        item_set.sell(self.amount)
        return super(Sale, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Sale of {self.amount} {self.drug.name}(s) on {self.time.date()} at {self.time.time()}"
    

class Purchase(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    amount = models.IntegerField()
    price = models.FloatField()
    date = models.DateField(default=tz.now)

    def __str__(self) -> str:
         return f"Purchase of {self.amount} {self.drug.name}(s) on {self.date}"


class BusinessMonth(models.Model):
    " A bussiness month recording all transactions, profits or losses within the month """

    opening_cash = models.FloatField()
    opening_stock = models.IntegerField()
    opening_date = models.DateField(default=tz.now)
    closing_cash = models.FloatField(null=True)
    closing_stock = models.IntegerField(null=True)
    closing_date = models.DateField(null=True)
    margin = models.FloatField(default=0)

    def any(self) -> bool:
        """ Check if any business month exists """

        months = BusinessMonth.objects.all()

        if months.count() != 0:
            return True
        return False

    def get_credits_price(self, opening: tz.datetime=None, closing: tz.datetime=tz.now()) -> float:
        """ Get total price of credits within a timeframe """

        credit = 0

        if not opening:
            opening = self.opening_date
        if not closing:
            closing = self.closing_date
        
        credits = Credit.objects.filter(date__gte=opening)
        credits = credits.filter(date__lte=closing)

        for item in credits:
            credit += item.price
        
        return float(credit)

    def get_debits_price(self, opening: tz.datetime=None, closing: tz.datetime=tz.now()) -> float:
        """ Get total price of debits within a timeframe """

        debit = 0

        if not opening:
            opening = self.opening_date
        if not closing:
            closing = self.closing_date

        debits = Debit.objects.filter(date__gte=opening)
        debits = debits.filter(date__lte=closing)

        for item in debits:
            debit += item.price

        return float(debit)

    def get_sales_price(self, opening: tz.datetime=None, closing: tz.datetime=tz.now()) -> float:
        """ Get total price of sales within a timeframe """

        sale = 0

        if not opening:
            opening = self.opening_date
        if not self.closing_date:
            closing = closing

        sales = Sale.objects.filter(time__gte=opening)
        sales = sales.filter(time__lte=closing)

        for item in sales:
            sale += item.price #com

        return float(sale)

    def get_purchases_price(self, opening: tz.datetime=None, closing: tz.datetime=tz.now()) -> float:
        """ Get total price of purchases within a timeframe """

        purchase = 0

        if not opening:
            opening = self.opening_date
        if not self.closing_date:
            closing = closing
        
        purchases = Purchase.objects.filter(date__gte=opening)
        purchases = purchases.filter(date__lte=closing)

        for item in purchases:
            purchase += item.price
        
        return float(purchase)

    def get_costs_price(self, opening: tz.datetime=None, closing: tz.datetime=tz.now()) -> float:
        """ Get total cost price of drugs sold within a timeframe """

        cost = 0

        if not opening:
            opening = self.opening_date
        if not self.closing_date:
            closing = closing

        sales = Sale.objects.filter(time__gte=opening)
        sales = sales.filter(time__lte=closing)

        for item in sales:
            cost += (item.drug.cost_price * item.amount)
        
        return float(cost)

    def balance_cash(self, opening: tz.datetime=None, closing: tz.datetime=tz.now()) -> float:
        """ Compute balance on cash """

        credits = self.get_credits_price(opening=opening, closing=closing)
        debits = self.get_debits_price(opening=opening, closing=closing)

        balance = self.opening_cash + credits - debits
        return balance

    def balance_stock(self, opening: tz.datetime=None, closing: tz.datetime=tz.now()) -> float:
        """ Compute balance on stock """

        bought = self.get_purchases_price(opening=opening, closing=closing)
        sold = self.get_sales_price(opening=opening, closing=closing)

        balance = self.opening_stock + bought - sold
        return balance

    def calculate_margin(self,opening: tz.datetime=None, closing: tz.datetime=tz.now(), commit: bool=True) -> float:
        margin = self.get_sales_price(opening=opening, closing=closing) - self.get_costs_price(opening=opening, closing=closing)
        self.margin = margin

        return margin

    def close(self, dates: str=None) -> None:
        """ Close the accounts for a month """

        self.closing_cash = self.balance_cash()
        self.closing_stock = self.balance_stock()
        self.closing_date = tz.now().date()

        if dates:
            try:
                y, m, d = dates.split("-")
            except Exception:
                raise ValueError(f"Invalid date: Date must be in the format 'yyyy-mm-dd'")

            self.calculate_margin()
            self.save()

    def __str__(self):
        return f"Bussiness month from {self.opening_date} to {self.closing_date}"