# Regular Expression package used to extract digits from strings
import re

# Global variables to be used in the below functions
cin_str = '17000372214424' # Example CIN to be used to test the function
len_cin_deter = 12 # How much of the string needs to be taken in account to determine the total
modulo = 97 # Modulo to be used in validation, alter here whenever is necessary

def main():
    """ The main function to call the function and display the result to keep the actual function bound to it's only function. This gives us in this function free space to do everything we like with the outcome without altering the actual function"""
    
    # Call upon the function to determine if the string is a valid CIN
    validation = is_valid_cin(cin=cin_str)
    # Print the outcome
    print(validation)

def is_valid_cin(cin: str):
    """ An function to determine if the given CIN string is a valid CIN number."""

    # Extract all numbers, in the correct order, from the given string  
    array = re.findall(r'\d', cin)

    # To be used as a box to add, in essence store, all the sub calculations for later use
    total = 0

    # Loop through every number until len_cin_deter is reached
    for n in range(len(array)):
        artificial_n = n+1
        sub_calc = artificial_n*int(array[n])
        total += sub_calc
        if artificial_n == len_cin_deter:
            break

    # Extract the last two digits to use these as a checksum for later use
    checksum = int(str(cin)[-2:])

    # A validation boolean to return True when modulus is the number of the last two digits of the CIN, else False
    val_bool = True if ((total % modulo) == checksum) else False

    return val_bool

if __name__ == '__main__':
    main()