import hashlib
import random

class Merchant(object):
    def __init__(self, keys):
        print("Intializing Bank")
        self.keys = keys
    
    def verify_sign(self, moneyorders,signature):
        e = self.keys['e']
        n = self.keys['n']
        moneyorders = moneyorders
        prev_order=[]
        now_signature=[]
        prev_order.append(moneyorders['amount'])
        now_signature.append(signature[0] ** e % n)
        now_signature.append(signature[1] ** e % n)
        prev_order.append(moneyorders['uniqueness'])
        id_keys = ['I1', 'I2', 'I3']
        c=2
        for key in id_keys:
            for i in moneyorders[key]['id_string']:
                now_signature.append(signature[c] ** e % n)
                c=c+1
                prev_order.append(i[0])
                now_signature.append(signature[c] ** e % n)
                c=c+1
                prev_order.append(i[1])
        if prev_order != now_signature:
            print("Digitally certified")
        else:
            print("Not Certified")
