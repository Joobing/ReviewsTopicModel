import tensorflow_datasets as tfds



TMSH=pd.read_json('TMSH'+'.json', orient='records')
TMSH.set_index('id')
TMLN=pd.read_json('TMLN'+'.json', orient='records')
TMLN.set_index('id')
PRSH=pd.read_json('PRSH'+'.json', orient='records')
PRSH.set_index('id')
PRLN=pd.read_json('PRLN'+'.json', orient='records')
PRLN.set_index('id')
LGSH=pd.read_json('LGSH'+'.json', orient='records')
LGSH.set_index('id')
LGLN=pd.read_json('LGLN'+'.json', orient='records')
LGLN.set_index('id')




# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 19:26:10 2020

@author: u811717
"""

