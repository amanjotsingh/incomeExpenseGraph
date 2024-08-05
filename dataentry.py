from datetime import datetime
date_format = "%d-%m-%Y"
CATEGORIES = {'I':'Income','E':'Expense'}

def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)
    
    try:
        validate_date = datetime.strptime(date_str,date_format)
        return validate_date.strftime(date_format)
    except ValueError:
        print(" Enter the valid date of format dd-mm-yyyy")
        return get_date(prompt,allow_default)

def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <=0:
            raise ValueError("Enter value greater than zero")
        return amount
    except ValueError as e:
        print (e)
        return get_amount()

        

def get_catgory():
    category = input("Enter a category 'I' for income and 'E' for expense :").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    print ("Enter the valid entry ")
    return get_catgory()

def get_description():
    return input("Enter the description (optional): ")


    