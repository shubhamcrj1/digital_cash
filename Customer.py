import hashlib
import random


class Customer(object):
    def __init__(self, amount, identity, keys):
        print("Initalizing Customer")
        self.amount = amount
        self.identity = identity
        self.keys = keys
        self.moneyorders = {}

        # Create 3 different money orders.
        for i in range(1, 4):
            mo_name = "mo" + str(i)
            self.moneyorders[mo_name] = self.create_moneyorder(mo_name)


    def create_moneyorder(self, name):
        print("Creating Money Order %s" % name)
        print("Running Bit Commitment")
        mo = {}
        mo['name'] = name
        mo['amount'] = self.amount
        mo['uniqueness'] = self.random_num_generator()
        mo['k'] = self.random_num_generator()
        mo['I1'] = self.create_identity_string()
        print("Creating Identity String I1")
        mo['I2'] = self.create_identity_string()
        print("Creating Identity String I2")
        mo['I3'] = self.create_identity_string()
        print("Creating Identity String I3")

        return mo

    def create_identity_string(self):
        r, s = self.secret_splitting()
        l_hash, r1, r2 = self.bit_commitment(id_int=r)
        r_hash, s1, s2 = self.bit_commitment(id_int=s)
        id_string = [[l_hash, r1], [r_hash, s1]]
        reveal_array = [[r, r1, r2], [s, s1, s2]]

        return {'id_string':id_string, 'reveal_array':reveal_array}
    
    def secret_splitting(self):
        r = self.random_num_generator()
        s = r ^ self.identity

        return r,s
    
    def bit_commitment(self, id_int):
        r1 = self.random_num_generator()
        r2 = self.random_num_generator()

        int_string = str(id_int) + str(r1) + str(r2)
        byte_string = bytes(int_string, encoding='utf-8')
        hash_value = hashlib.sha256(byte_string).hexdigest()
        int_value = int(hash_value, 16) % self.keys['n']

        return [int_value, r1, r2]


    def blind(self):
        print("Blinding Money Orders")
        self.blind_moneyorders = {}
        n = self.keys['n']
        for mo in self.moneyorders.keys():
            blind_mo = {}
            orig_mo = self.moneyorders[mo]
            blind_factor = orig_mo['k'] ** self.keys['e'] % n
            blind_mo['name'] = orig_mo['name']
            blind_mo['amount'] = (orig_mo['amount'] * blind_factor % n)
            blind_mo['uniqueness'] = (orig_mo['uniqueness'] * blind_factor % n)

            for key in orig_mo.keys():
                if not key.startswith('I'):
                    continue
                blind_mo[key] = {}
                blind_mo[key]['id_string'] = []
                for i in orig_mo[key]['id_string']:
                    blind_hash = (i[0] * blind_factor % n)
                    blind_random = (i[1] * blind_factor % n)
                    blind_mo[key]['id_string'].append([blind_hash, blind_random])

            self.blind_moneyorders[mo] = blind_mo


    def print_moneyorder(self, money_orders, type_mo):
        print("Printing Money Order...")
        for mo in money_orders.keys():
            strings_array = []
            filename = '%s_%s.txt' % (type_mo,mo)

            print_mo = money_orders[mo]
            name_str = "Name: %s" % print_mo['name']
            strings_array.append(name_str)
            amount_digi = "Amount: %d" % print_mo['amount']
            strings_array.append(amount_digi)
            uniqueness_digi = "Uniqueness %d" % print_mo['uniqueness']
            strings_array.append(uniqueness_digi)

            I1_idstring = "I1 id string: %s" % str(print_mo['I1']['id_string'])
            strings_array.append(I1_idstring)
            I2_idstring = "I2 id string: %s" % str(print_mo['I2']['id_string'])
            strings_array.append(I2_idstring)
            I3_idstring = "I3 id string: %s" % str(print_mo['I3']['id_string'])
            strings_array.append(I3_idstring)

            if 'signature' in print_mo:
                sig_string = "signature: %s" % str(print_mo['signature'])
                strings_array.append(sig_string)
            with open(filename, 'w') as f:
                for i in strings_array:
                    f.write(i + '\n')


    def print_moneyorder2(self, money_orders, type_mo):
        print("Printing Money Order...")
        for mo in money_orders.keys():
            strings_array = []
            filename = '%s_%sfirst.txt' % (type_mo,mo)

            print_mo = money_orders[mo]
            name_str = "Name: %s" % print_mo['name']
            strings_array.append(name_str)
            amount_digi = "Amount: %d" % print_mo['amount']
            strings_array.append(amount_digi)
            uniqueness_digi = "Uniqueness %d" % print_mo['uniqueness']
            strings_array.append(uniqueness_digi)
            I1_idstring = "I1 id string: %s" % str(print_mo['I1']['id_string'])
            strings_array.append(I1_idstring)
            I2_idstring = "I2 id string: %s" % str(print_mo['I2']['id_string'])
            strings_array.append(I2_idstring)
            I3_idstring = "I3 id string: %s" % str(print_mo['I3']['id_string'])
            strings_array.append(I3_idstring)

            if 'signature' in print_mo:
                sig_string = "signature: %s" % str(print_mo['signature'])
                strings_array.append(sig_string)
            with open(filename, 'w') as f:
                for i in strings_array:
                    f.write(i + '\n')



    def random_num_generator(self):
        rand_low_num = 100
        rand_high_num = 10000
        return random.randint(rand_low_num, rand_high_num) % self.keys['n']


    def receive_signature(self, moneyorder, signature):
        print("Recieved Signed Money Order")
        signed_mo = {}
        signed_mo[moneyorder] = dict(self.blind_moneyorders[moneyorder])
        signed_mo[moneyorder]['signature'] = signature
        self.signed_moneyorder = signed_mo


    def reveal(self, moneyorders):
        print("Revealing Selected Money Orders")
        revealed_nums = {}
        for mo in moneyorders:
            orig_mo = self.moneyorders[mo]
            revealed_nums[mo] = {}
            for key in orig_mo.keys():
                if key.startswith('I'):
                    revealed_nums[mo][key] = orig_mo[key]['reveal_array']

        return revealed_nums


   

    def mod_inverse(self,a, n):
        def extended_gcd(a, b):
            if a == 0:
                return (b, 0, 1)
            else:
                g, y, x = extended_gcd(b % a, a)
                return (g, x - (b // a) * y, y)
    
        gcd, x, y = extended_gcd(a, n)
    
        if gcd != 1:
            return -1
        else:
            return x % n

    def unblind(self, moneyorders):
        print("Unblinding Money Orders")
        self.unblinded_moneyorders = {}
        n = self.keys['n']
        for mo in moneyorders:
            orig_mo = self.moneyorders[mo]
            blind_mo = self.blind_moneyorders[mo]

            inv_k = int(self.mod_inverse(orig_mo['k'], n))
            unblind_factor = (inv_k ** self.keys['e']) % n

            unblind_mo = {}
            unblind_mo['name'] = orig_mo['name']
            unblind_mo['amount'] = (blind_mo['amount'] * unblind_factor % n)
            unblind_mo['uniqueness'] = (blind_mo['uniqueness'] * unblind_factor
                                        % n)
            for key in blind_mo.keys():
                if not key.startswith('I'):
                    continue
                unblind_mo[key] = {'id_string': []}
                for i in blind_mo[key]['id_string']:
                    unblind_hash = (i[0] * unblind_factor % n)
                    unblind_random = (i[1] * unblind_factor % n)
                    unblind_mo[key]['id_string'].append([unblind_hash,
                                                         unblind_random])

            self.unblinded_moneyorders[mo] = unblind_mo


    def unblind_signed_moneyorder(self):
        print("Unblinding Money Orders")
        self.unblindedsigned_moneyorder = {}
        n = self.keys['n']

        for mo in self.signed_moneyorder.keys():
            orig_mo = self.moneyorders[mo]
            blind_mo = self.signed_moneyorder[mo]

            inv_k = int(self.mod_inverse(orig_mo['k'], n))
            unblind_factor = (inv_k ** self.keys['e']) % n

            unblind_mo = {}
            unblind_mo['name'] = orig_mo['name']
            unblind_mo['amount'] = (blind_mo['amount'] * unblind_factor % n)
            unblind_mo['uniqueness'] = (blind_mo['uniqueness'] * unblind_factor
                                        % n)
            for key in blind_mo.keys():
                if key == 'signature':
                    unblind_sig = []
                    for i in blind_mo[key]:
                        unblind_i = i * unblind_factor % n
                        unblind_sig.append(unblind_i)
                    unblind_mo[key] = unblind_sig

                elif key.startswith('I'):
                    unblind_mo[key] = {'id_string': []}
                    for i in blind_mo[key]['id_string']:
                        unblind_hash = (i[0] * unblind_factor % n)
                        unblind_random = (i[1] * unblind_factor % n)
                        unblind_mo[key]['id_string'].append([unblind_hash,
                                                             unblind_random])

            self.unblindedsigned_moneyorder[mo] = unblind_mo