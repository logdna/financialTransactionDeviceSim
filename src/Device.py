
import time
import json
import random
import datetime
import requests
from faker import Faker

class Device:
    '''Simuluate a single device generating financial transactions.  No real internal logic, just random.'''
    def __init__(self, device_id, device_name, device_vrs, device_location, device_status, mezmo_key, mezmo_url, output_packet, debug, output_volume):
        self.device_id = device_id
        self.device_name = device_name
        self.device_vrs = device_vrs
        self.device_location = device_location
        self.device_status = device_status
        self.mezmo_key = mezmo_key
        self.mezmo_url = mezmo_url
        self.retries = 5
        self.output_packet = output_packet
        self.debug = debug
        self.output_volume = output_volume
        self.running_volume = 0.0

        # Faker
        self.faker = Faker()
        Faker.seed(time.time())
    
    def genAndSendTransaction( self ):
        '''Generate a transaction and send it to Mezmo'''
        if self.debug: print('Transaction on device {} being logged'.format(self.device_id))

        # Using a selection of functions to give variety from the devices.
        # Each returns a JSON object to be posted
        new_transaction = random.choice([
              self.genFinancialTransactionLog
            , self.genFinancialTransactionLog
            , self.genBootupLog
            , self.genAccessLog
            , self.genAccessLog
            , self.genAccessLog
            , self.genAccessLog
            , self.genAccessLog
        ])()

        self.running_volume += 0.0 #sizeof(new_transaction)
        self.postToMezmo(new_transaction)
    
    def genDeviceLogStatic( self ):
      '''Generate the device part of the log'''
      return {
              'device': {
                  'id': self.device_id
                , 'name': self.device_name
                , 'vrs': self.device_vrs
                , 'location': self.device_location
                , 'status': self.device_status
            }
            , 'buffer': self.faker.uuid4()
      }


    def genAccessLog( self ):
        '''Generate an access log'''
        tmp = self.genDeviceLogStatic()
        tmp.update({
              'datetime': datetime.datetime.now().isoformat()
            , 'access': {
                  'name': self.faker.name()
                , 'user_id': self.faker.uuid4()
                , 'action': random.choice(['login', 'check_balance', 'remove_charge', 'add_charge', 'logout'])
            }
            , 'event': 'access'
        })
        return tmp

    def genBootupLog( self ):
        '''Generate a bootup log'''
        tmp = self.genDeviceLogStatic()
        tmp.update({
              'datetime': datetime.datetime.now().isoformat()
            , 'bootup': {
                  'uptime': random.randint(0, 100000)
                , 'memory': random.randint(0, 30000)
                , 'cpu': random.randint(0, 100)
                , 'disk': random.randint(0, 100)
            }
            , 'event': 'bootup'
        })
        return tmp

    def genFinancialTransactionLog( self ):
        '''Generate a fake financial transaction'''
        tmp = self.genDeviceLogStatic()
        tmp.update({
              'datetime': datetime.datetime.now().isoformat()
            , 'transaction': {
                  'product_id': self.faker.uuid4()
                , 'customer_id': self.faker.uuid4()
                , 'quantity': random.randint(1,20)
                , 'unit_price': float('{:.2f}'.format(random.uniform(0.01, 250.00)))
                , 'net_price': 0.0
                , 'tax': float('{:.4f}'.format(random.choice([0.0610,0.0725,0.0290,0.0,0.06,0.07])))
                , 'total_price': 0.0
                , 'cc': {
                      'cc_number': self.faker.credit_card_number(card_type=None)
                    , 'cc_exp': self.faker.credit_card_expire(start='now', end='+10y', date_format='%m/%y')
                    , 'cc_cvv': self.faker.credit_card_security_code(card_type=None)
                    , 'cc_name': self.faker.name()
                    , 'cc_zip': self.faker.postcode()
                }
                , 'result': random.choice(['success','fail'])
                , 'result_reason': 'card_accepted'
            }
            , 'event': 'transaction'
        })
        tmp['transaction']['net_price'] = float('{:.2f}'.format(tmp['transaction']['quantity'] * tmp['transaction']['unit_price']))
        tmp['transaction']['total_price'] = float('{:.2f}'.format(tmp['transaction']['net_price'] * (1.0 + tmp['transaction']['tax'])))
        if tmp['transaction']['result'] == 'fail': tmp['transaction']['status_reason'] = self.faker.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None)

        return tmp

    def postToMezmo( self, transaction ):
        '''Use requests to forward to Mezmo'''
        if self.debug: print('Posting transaction to Mezmo')
        if self.debug or self.output_packet: print(json.dumps(transaction,indent=3))
        if self.output_volume: print('{:.3f} GB'.format(self.running_volume))
        # Try a few times and then move on if there are issues
        for i in range(self.retries):
          try:
            # Using a simple approach but there are many integration paths
            requests.post(
                  url=self.mezmo_url
                , headers={'authorization': '{}'.format(self.mezmo_key)}
                , json=transaction
                )
            break
          except:
            if self.debug: print('Trying to send again...')
