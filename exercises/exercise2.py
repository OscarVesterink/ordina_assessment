from collections import abc

# Global variables to be used in the below functions
start_inventory = {         # Dictionary to start the inventory with
    '17000372214424' : 9,
    '42100551007977' : 2,
}

transaction_log = """17000372214424 INCOMING 9 17000372214424 OUTGOING 1 17000372214424 INCOMING 3 42100551007977 OUTGOING 3 42100551007977 INCOMING 1 17000372214424 OUTGOING 2 17000372214425 OUTGOING 2""" # Transaction log of all the transactions happenend that day

def main():
    """ The main function to call the function and display the result to keep the actual function bound to it's only function. This gives us in this function free space to do everything we like with the outcome without altering the actual function"""
    end_inventory = calculate_inventory(start_inventory=start_inventory, transaction_log=transaction_log)
    warnings = validate_inventory(end_inventory=end_inventory)

    # Print the inventory at the end of the day + possible warnings
    print(end_inventory)
    print(warnings)

def calculate_inventory(
    start_inventory: abc.Mapping[str:int],
    transaction_log: str
    ):

    # To only work with an inventory in this function without altering the starting inventory
    temp_inventory = start_inventory

    # Make sure the (multiline) string of the transaction log is split into an array
    refined_transaction_log = split_transaction_log(raw_transaction_log=transaction_log)

    # Determine if an item already exists, if the transaction is INCOMING or OUTGOING and act accordingly (respectively: create inventory, add number, subtract number)
    for transaction in refined_transaction_log:
        if not transaction[0] in temp_inventory:
            temp_inventory[transaction[0]] = 0
        if transaction[1] == 'INCOMING':
            temp_inventory[transaction[0]] = int(temp_inventory[transaction[0]])+int(transaction[2])
        elif transaction[1] == 'OUTGOING':
            temp_inventory[transaction[0]] = int(temp_inventory[transaction[0]])-int(transaction[2])

    return temp_inventory

def split_transaction_log(raw_transaction_log: str):
    """ A function to refined the raw transaction log, from a (multiline) string to an array with the following structure:
    
    total_log_array = [
        [CIN, Direction, Amount],
        ...
    ]

    """
    total_log_array = []
    sub_log_array = []

    # Split multiline string into an array split by breakspace
    split_log = raw_transaction_log.split(' ')
    # Construct the total_log_array as displayed in explanation seen above
    for item in split_log:
        sub_log_array.append(item)
        
        if len(sub_log_array) == 3:
            total_log_array.append(sub_log_array)
            sub_log_array = []

    return total_log_array

def validate_inventory(end_inventory: abc.Mapping[str:int]):
    """ A function to validate if any item in the inventory ends the day with a negative value. If so, a string with the appropiate data is added to the array of warnings. """
    warnings = []

    for key in end_inventory:
        if end_inventory[key] < 0:
            str = "Warning: {} has an value below zero. The value is {}".format(key, end_inventory[key])
            warnings.append(str)

    return warnings

if __name__ == "__main__":
    main()
