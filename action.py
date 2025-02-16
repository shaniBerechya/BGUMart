from argparse import Action
from persistence import *

import sys

def process_action(action_line):
    ## extract nececary data
    product_id = int(action_line[0])
    quantity = int(action_line[1])
    activator_id = int(action_line[2])
    date = action_line[3]

    ## finding the product 
    product_list = repo.products.find(id=product_id)
    if not product_list:
        return
    
    product = product_list[0]
    
    ## ilegal quantity
    if quantity == 0:
        return
    
    ## sale case
    if quantity < 0: 
        #chack thet is possible to sale
        if product.quantity + quantity < 0:
            return

    ## update the new quantity in the product table
    product.quantity += quantity
    repo.products.update(product)
    
    ##update actions
    activitie = Activitie(product_id,quantity,activator_id,date)
    repo.activities.insert(activitie)


def main(args : list[str]):
    inputfilename : str = args[1]
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline : list[str] = line.strip().split(", ")
            process_action(splittedline)

if __name__ == '__main__':
    main(sys.argv)