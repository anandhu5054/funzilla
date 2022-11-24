from django import template
import math

register = template.Library() 


@ register.simple_tag

def call_sellerprice(price,discount):
    # breakpoint()
    if  discount is 0:
        return price
    
    sellprice = price
    sellprice = price - (price*discount/100)

    return math.floor(sellprice)