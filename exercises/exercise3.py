from collections import abc

# Global variables to be used in the below functions
transaction_log = """17000372214424 INCOMING 9 
17000372214424 OUTGOING 1 
17000372214424 INCOMING 3 
42100551007977 OUTGOING 3 
42100551007977 INCOMING 1 
17000372214424 OUTGOING 2 
17000372214425 OUTGOING 6""" # Transaction log of all the transactions happenend that day
n = 5 # Number of copies to be listed in the Best Sellers list
publication_type_filter = 'Book' # A filter used to filter the Best Sellers List. Use 17 for books and 42 for magazines. Leave 'None' when no filter is needed

# Created a class to be used as an instance to store the Best Sellers
class BestSeller:

    def __init__(self, cin, publication_type, quantity_sold):
        self.cin = cin
        self.publication_type = publication_type
        self.quantity_sold = quantity_sold

    @property
    def store_item(self, cin, publication_type, quantity_sold):
        return "{} with {} is today sold for {}".format(cin, publication_type, quantity_sold) # If needed as approval

    @store_item.setter
    def store_item(self, cin, publication_type, quantity_sold): 
        self.cin = cin
        self.publication_type = publication_type
        self.quantity_sold = quantity_sold

def main():
    """ The main function to call the function and display the result to keep the actual function bound to it's only function. This gives us in this function free space to do everything we like with the outcome without altering the actual function"""
    best_seller_list = calculate_best_sellers(transaction_log=transaction_log, n=n, publication_type_filter=publication_type_filter)

    # Print the Best Seller list at the end of the day
    for instance in best_seller_list:
        print(instance.cin, instance.publication_type, instance.quantity_sold, sep = ' ')

def calculate_best_sellers(
    transaction_log: str,
    n: int,
    publication_type_filter: str
    ):

    # To only work with an inventory in this function without altering the starting inventory
    temp_inventory = {}

    # Make sure the (multiline) string of the transaction log is split into an array
    refined_transaction_log = split_transaction_log(raw_transaction_log=transaction_log)

    # Determine if an item already exists, if the transaction is INCOMING or OUTGOING and act accordingly (respectively: create inventory, add number, subtract number)
    for transaction in refined_transaction_log:
        if transaction[1] == 'OUTGOING' and int(transaction[2]) > 0:
            if not transaction[0] in temp_inventory:
                temp_inventory[transaction[0]] = int(transaction[2])
            else:
                temp_inventory[transaction[0]] = int(temp_inventory[transaction[0]])+int(transaction[2])

    # Filter the inventory based on what the user requests, see publication_type_filter. If no filter is set, the function is not run but rather given the value of temp_inventory
    filtered_inventory = filter_inventory(calculated_inventory=temp_inventory, publication_type_filter=publication_type_filter) if publication_type_filter != None else temp_inventory
    # Sort the list and return a list
    sorted_inventory = sort_inventory(filtered_inventory=filtered_inventory)

    # The list to be created, to consist instances of the Bestseller class
    list_instances = []

    # To be used to stay within the margin of n
    count = 0
    for item in sorted_inventory:
        count += 1
        publication_type = 'Book' if int(str(item)[0:2]) == 17 else 'Magazine'
        list_instances.append(BestSeller(cin=item, publication_type=publication_type, quantity_sold=sorted_inventory[item]))
        if count == n:
            break

    return list_instances

def split_transaction_log(raw_transaction_log: str):
    """ A function to refined the raw transaction log, from a (multiline) string to an array with the following structure:
    
    total_log_array = [
        [CIN, Direction, Amount],
        ...
    ]

    """
    total_log_array = []

    # Split multiline string into an array split by breakspace
    split_log = raw_transaction_log.split('\n')
    # Construct the total_log_array as displayed in explanation seen above
    for item in split_log:
        sub_log_array = item.split(' ')
        total_log_array.append(sub_log_array)

    return total_log_array

def filter_inventory(
    calculated_inventory: abc.Mapping[str:int],
    publication_type_filter: str
    ):
    """ Sort the data on descending order, based on quantity sold and lexicographical"""
    temp_inventory = calculated_inventory
    filter = '17' if publication_type_filter == 'Book' else '42'

    refined_inventory = {key: value for key, value in temp_inventory.items() if key.startswith(filter)}

    return refined_inventory

def sort_inventory(filtered_inventory: abc.Mapping[str:int]):
    """ Sort the data on descending order, based on quantity sold and lexicographical"""
    temp_inventory = filtered_inventory

    sort_number = dict(sorted(temp_inventory.items(), key=lambda item:item[1], reverse=True))

    return sort_number

if __name__ == "__main__":
    main()
