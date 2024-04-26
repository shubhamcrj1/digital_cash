import Customer as customer
import bank
import merchant 
import storee
import sys
customer1_keys = {'e': 528, 'n': 4153}
bank1_keys = {'d': 936, 'n': 4153}
merchant1_keys = {'e': 528, 'n': 4153}
amount = 100
customer1_id = 123432
customer1 = customer.Customer(amount=amount, identity=customer1_id, keys=customer1_keys)
bank1 = bank.Bank(keys=bank1_keys)
merchant1 = merchant.Merchant(keys=merchant1_keys)
storee1=storee.Storee()
storee1.unique={}
storee1.unique[customer1.moneyorders['mo1']['uniqueness']]=1
storee1.unique[customer1.moneyorders['mo2']['uniqueness']]=1
storee1.unique[customer1.moneyorders['mo3']['uniqueness']]=1
if(storee1.unique[customer1.moneyorders['mo1']['uniqueness']]!=1):
     print('Duplicate')
     sys.exit()
if(storee1.unique[customer1.moneyorders['mo2']['uniqueness']]!=1):
    print('Duplicate')
    sys.exit()
if(storee1.unique[customer1.moneyorders['mo3']['uniqueness']]!=1):
    print('Duplicate')
    sys.exit()
customer1.blind()
bank1.receive_blindmoneyorders(customer1.blind_moneyorders)
bank1.unblind_request()
customer1.unblind(bank1.to_unblind_moneyorders)
bank1.receive_unblindedmoneyorders(customer1.unblinded_moneyorders)
bank1.receive_revealinfo(customer1.reveal(bank1.to_unblind_moneyorders))
bank1.sign_moneyorder()
merchant1.verify_sign(moneyorders=bank1.to_sign_moneyorder,signature=bank1.bank_signature)
customer1.receive_signature(bank1.to_sign_moneyorder_key, bank1.bank_signature)
customer1.unblind_signed_moneyorder()
customer1.print_moneyorder2(customer1.moneyorders, 'unblinded')
customer1.print_moneyorder(customer1.blind_moneyorders, 'blind')
customer1.print_moneyorder(customer1.unblinded_moneyorders, 'unblinded')
customer1.print_moneyorder(customer1.signed_moneyorder, 'signed')
customer1.print_moneyorder(customer1.unblindedsigned_moneyorder, 'unblindsigned')