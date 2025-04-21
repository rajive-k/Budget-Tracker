## Name: RAJIVE PRASHAD KUMARANAYAKE
# General Assembly 
# Reference list: Study Notes, Python.org,assignment cheat sheet, stackoverflow.com, w3schools.com
##### ## Python Fundamentals Lab -
# #### Budget Tracker
import csv
import os
from datetime import datetime
# Stretch goal - manage multiple accounts
# Declare list of available accounts
account_list = ["Lemonade Stand"]
headings = ["title", "type", "income_amount", "expense_amount", "transaction_date", "account", "customer", "vendor"]

# #### Technical Requirements
# - Stores all entries in a .csv file
if not os.path.exists("./budget_tracker.csv"):
    with open("./budget_tracker.csv", "w", newline='') as file: # syntax from stackoverflow
        # removed extra line https://stackoverflow.com/questions/3348460/csv-file-written-with-python-has-blank-lines-between-each-row
        writer = csv.DictWriter(file, fieldnames=headings)
        writer.writeheader()

    # 2.	If I choose to add a new entry, I am asked to provide:
    # - a.	A title describing the budget item
    # - b.	Whether the budget item is Income or Expense
    # - c.	The total amount of the budget item
    # - d.	The date of the transaction in "MM-DD-YYYY" string format 06-03-2024
# START - ADD NEW TRANSACTION FUNCTION
def add_new_transaction_def(account_name):
    with open("./budget_tracker.csv", 'a+', newline='') as file:
        writer = csv.writer(file)
        # option to continuously add transactions
        while True:
            add_more = input(f"{'-'*100}\n *  Press 'Enter key' to add a budget item or type 'Q' to quit:")
            print(f"{'-'*100}\n ")
            if add_more.lower() == "q": # if user enter Q or q then exit the while loop > go to Main Menu
                break
            if add_more != "": # until user press Enter key it will show the following message.
                print("Invalid input! press 'Enter key' or 'Q' to quit.  Please try again.")
            else:
                # limiting the number of characters allowed for title to maintain the transaction table design
                while True:
                    title = input("\n *   Enter the description of the budget Item: ")
                    if len(title) <= 30:
                        break
                    else:
                        print(' => Enter a shorter description, maximum 30 characters allowed! ')
                        continue
                # restrict the user to enter only i for income and e for expense
                while True:
                    type = input(" *   Is the budget item is an Income or Expense? (I/E): ")
                    if type.lower() == "i" or type.lower() == "e":
                        break
                    else:
                        print(' => Invalid answer! Enter "I" for income and "E" for expense. ')
                        continue
                        # Validate the amount entered is a float
                # stretch goal- track transaction by custoer and vendor
                customer_vendor = input(f" *   {'Customer' if type.lower() == 'i' or type.lower() == 'income' else 'Vendor'} Name: ")
                if type.lower() == "i" or type.lower() == "income":
                    customer = customer_vendor
                    vendor = '0'
                elif type.lower() == "e" or type.lower() == "expense":
                    vendor = customer_vendor
                    customer = '0'
                # Validate the amount entered is a float
                while True: # syntax from assignment cheat sheet
                    try:
                        amount = float(input(" *   Enter the amount of the budget item: $"))
                        break
                    except ValueError:
                        print(' => Invalid amount! Enter amount in numbers, with/without decimals ')
                        continue
                tdate = str(input(" *   Enter the transaction date (MM-DD-YYYY): "))
                # validate the date format
                valid = False
                while not valid:
                    try:
                        date = datetime.strptime(tdate, "%m-%d-%Y").strftime("%m-%d-%Y") # syntax from stackoverflow
                        #https://stackoverflow.com/questions/44808807/how-to-ensure-user-input-date-is-in-correct-format
                        valid = True
                    except ValueError:
                        tdate = input(" *   Wrong date format. please enter Month-day-year like MM-DD-YEAR: ")
                        # separate the amount entered by the user into income or expense fields
                if type.lower() == "i":
                    income = round(float(amount), 2)
                    expense = 0
                    type = "Income"
                elif type.lower() == "e":
                    income = 0
                    expense = round(float(amount), 2)
                    type = "Expense"
                account = account_name
                writer.writerow([title, type, income, expense, tdate, account, customer, vendor])
# END - ADD NEW TRANSACTION FUNCTION

    # 3.	If I choose to display the total account balance:
    # - a.	The program adds all income and subtracts all expense items to display the net balance
# START - PRINT TOTAL ACCOUNT BALANCE FUNCTION
def tot_bal_def(account_name):
    with open("./budget_tracker.csv", "r") as file:
        file.seek(0)
        total_income = 0
        total_expense = 0
        reader = csv.DictReader(file)
        for row in reader:
            if row["account"] == account_name: # calculate income and expense only for the selected account (Stretch goal)
                total_income += float(row["income_amount"])
                total_expense += float(row["expense_amount"])
        net_balance = total_income - total_expense
        str_net_balance = "%.2f" % float(net_balance) # syntax from stackoverflow
        # https://stackoverflow.com/questions/6149006/how-to-display-a-float-with-two-decimal-places
        str_total_income = "%.2f" % float(total_income)
        str_total_expense = "%.2f" % float(total_expense)
        print(f"Total Income                : ${' ' * (15 - len(str(str_total_income)))}{total_income:.2f}")
        print(f"Total Expenses              : ${' ' * (15 - len(str(str_total_expense)))}{total_expense:.2f}\n{' '*31}{'-'*16}")
        print(f"Net Balance                 : ${' ' * (15 - len(str_net_balance))}{net_balance:.2f}\n{' '*31}{'='*16}")
        return str_total_income
# END - PRINT TOTAL ACCOUNT BALANCE FUNCTION

    # 4.	If I choose to view all previous entries:
    # - a.	The program prints all details of all previous entries in a human readable format
# START - VIEW ALL PREVIOUS ENTRIES FUNCTON
def view_all_previous(account_name):
    with open("./budget_tracker.csv", "r") as file:
        file.seek(0)
        reader = csv.DictReader(file)
        #print(f"{"-" * 100}")
        print(f" Date{' '*9}Description{' '*26}Type{' '*8}Income{' '*10}Expense \n{'-' * 94}")
        for row in reader:
            row_list = list(row.values())
            if row_list[5] == account_name: # Display transactions only for selected account (stretched goal)
                income_str = "%.2f" % float(row_list[2]) # syntax from stackoverflow
                # https://stackoverflow.com/questions/6149006/how-to-display-a-float-with-two-decimal-places
                expense_str = "%.2f" % float(row_list[3])
                print(f" {row_list[4]} {' ' * (11 - len(row_list[4]))}"
                    f" {row_list[0]} {' ' * (36 - len(row_list[0]))}" \
                      f"{row_list[1]} {' ' * (10 - len(row_list[1]))}" \
                      f" ${' ' * (13 - len(income_str))}{income_str} " \
                      f" ${' ' * (13 - len(expense_str))}{expense_str} " )

                #print("-" * 100)
# END - VIEW ALL PREVIOUS ENTRIES FUNCTION

# START ---------   Stretch Goals FUNCTIONS -----------

# split month and year and add it to transaction list to use for monthly calculations
month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
def full_list_with_month_year(account_name):
    with open("./budget_tracker.csv", "r") as file:
        file.seek(0)
        total_income = 0
        no_of_transactions = 0
        reader = csv.DictReader(file)
        # Calculate Average transaction amount
        list_of_dict = []
        for row in reader:
            list_of_dict.append(row) if row["account"] == account_name else None
        # split month and year and create a new list including month and year keys.
        full_list_with_month_year = []
        for row in list_of_dict:
            dict_with_month_year = {}
            m_d_y_list = row["transaction_date"].split("-")
            dict_with_month_year["month_split"] = month_list[int(m_d_y_list[0])-1] # find the month name
            dict_with_month_year["year_split"] = m_d_y_list[2]
            dict_with_month_year.update(row) # syntax from w3schools
            # https://www.w3schools.com/python/ref_dictionary_update.asp
            #print(dict_with_month_year)
            full_list_with_month_year.append(dict_with_month_year)
        return full_list_with_month_year
# full_list_with_month_year(account_name)

# START - Monthly Profit and loss account Report fUNCTION
def monthly_pnl(account_name):
    with open("./budget_tracker.csv", "r") as file:
        file.seek(0)
        reader = csv.DictReader(file)
        list_of_months_to_choose = []
        for row in full_list_with_month_year(account_name):
            if row["month_split"]+" "+row["year_split"] not in list_of_months_to_choose:
                list_of_months_to_choose.append(row["month_split"]+" "+row["year_split"])
        #print(list_of_months_to_choose)
        print("\n * Please choose the month to display the Monthly Profit and Loss Statement.\n ")
        # show list of available months and years to choose
        num = 1
        #month_and_year = []
        for list_of_months in list_of_months_to_choose:
            print(f" {num}. {list_of_months}")
            num += 1
        #print(list_of_months_to_choose)
        # getting input from the user
        while True: # syntax from Assignment cheat sheet
            try:
                print(f"\n{'-' * 100}")
                selected_mm_yyyy = input(f" * Enter your choice (1-{num-1}) : ")
                print(f"{'-' * 100}")
                if int(selected_mm_yyyy) in range(1,num):
                    print(f"\n{'_' * 100}\n\n{(account_name.upper()).center(100)}\n{'MONTHLY PROFIT AND LOSS STATEMENT'.center(100)} ")
                    print(f" {('FOR ' + list_of_months_to_choose[int(selected_mm_yyyy)-1]).center(100)}\n{'_' * 100} ")
                    break
                else:
                    print(f" => Invalid answer! Enter only numbers between 1-{num-1}. ")
                    continue
            except ValueError as ve:
                # Customize the error message for non-numeric inputs
                if str(ve) == "invalid literal for int() with base 10: ":
                    print("You did not enter a number. Please enter a valid positive number.")
                else:
                    # Print the specific error message for the ValueError raised
                    print(ve)
                    print("Let's try again...\n")
        #Sales
        sales_dict_list = []
        for item in full_list_with_month_year(account_name):
            sales_dict_list.append(item) if item["type"] == "Income" else None

        #print(sales_dict_list)  # use sales_dict_list to find all the sales
        year_month_sales_dict_list = []
        for item in sales_dict_list:
            if (item["month_split"]+" "+item["year_split"]) == list_of_months_to_choose[int(selected_mm_yyyy)-1]:
                year_month_sales_dict_list.append(item)
        #print(year_month_sales_dict_list) # sales in selected month and year
        # prepare dictionary with aggregate sales amount of same sales items.
        totals_by_sale_item =  {}
        for item in year_month_sales_dict_list:
            sale_item = item["title"]
            sale_item_amount = float(item["income_amount"])
            if sale_item in totals_by_sale_item:
                totals_by_sale_item[sale_item] += sale_item_amount # totals_by_sale_item[sale_item] is the amount of the sales_item
            else:
                totals_by_sale_item[sale_item] = sale_item_amount
        # print(totals_by_sale_item) # this dictionary keys are sales items and values are totals of same sales items.
        # pnl - display sales
        print("\n\n Sales") # ----------------------------------------------------------------------------------------sales
        for keys, values in totals_by_sale_item.items(): # code from stackoverflow
            # https://stackoverflow.com/questions/24746712/dictionary-iterating-for-dict-vs-for-dict-items
            print (f"      {keys}{' '*(40 - len(keys))}      : $ {' '*(11-len('%.2f' % values))}{values:.2f}") # ---sales items
        # print total/gross Sales amount
        total_sales = 0
        for item in year_month_sales_dict_list:
            total_sales += float(item["income_amount"])
        print(f"      {'-'*61}") # ---------------------------------------------------------------------------------divider
        print(f"      Total Revenue {' '*53} ${' '*(11-len('%.2f' % total_sales))} {total_sales:.2f}") # --------------------total sales

        # Cost of goods sold and other expenses
        ###############################################################################################################################
        cosgs_items_list = ["fresh fruits", "cups", "ice cream" ] # Add all items belongs to 'Cost of Goods Sold' to this list
        ###############################################################################################################################
        cogs_dict_list = [] # list of cost of goods sold
        other_exp_dict_list = [] # list of all other expenses
        for item in full_list_with_month_year(account_name):
            if item["type"] == "Expense":
                cogs_dict_list.append(item) if item["title"].lower() in cosgs_items_list else other_exp_dict_list.append(item)
        # print(other_exp_dict_list)
        year_month_cogs_dict_list = [] # year and month of cost item
        for item in cogs_dict_list:
            if (item["month_split"]+" "+item["year_split"]) == list_of_months_to_choose[int(selected_mm_yyyy)-1]:
                year_month_cogs_dict_list.append(item)
        # print(year_month_cogs_dict_list)
        totals_by_cost_item =  {}
        for item in year_month_cogs_dict_list:
            cost_item = item["title"]
            cost_item_amount = float(item["expense_amount"])
            if cost_item in totals_by_cost_item:
                totals_by_cost_item[cost_item] += cost_item_amount
            else:
                totals_by_cost_item[cost_item] = cost_item_amount
        #print(totals_by_cost_item)
        print(f"\n - Cost of Goods Sold ({', '.join(cosgs_items_list)})") #---------------------------------------------cogs
        # print(totals_by_cost_item)
        for keys, values in totals_by_cost_item.items():
            print (f"      {keys}{' '*(40 - len(keys))}      : ${' '*(12-len('%.2f' % values))}{values:.2f}") #--------cogs itmes
        # print total cogs amount
        total_cogs = 0
        for item in year_month_cogs_dict_list:
            total_cogs += float(item['expense_amount'])
        print(f"      {'-'*61}") #----------------------------------------------------------------------------------------divider
        print(f"      Total Cost of Goods Sold {' '*42} ${' '*(11-len('%.2f' % total_cogs))} {total_cogs:.2f}") # --------total cogs

        print(f"{'-'*76}{'-'*12}") # ------------------' '-------------------------------------------------------divider before gross profit
        gross_profit = total_sales-total_cogs
        print(f"Gross Profit/Loss{' '*57}${' '*(12-len('%.2f' % gross_profit))}{gross_profit:.2f}") #--------------------gross profit
        # all other expenses
        year_month_other_expense_dict_list = []
        for item in other_exp_dict_list:
            if (item["month_split"]+" "+item["year_split"]) == list_of_months_to_choose[int(selected_mm_yyyy)-1]:
                year_month_other_expense_dict_list.append(item)
        # print(year_month_cogs_dict_list)
        totals_by_other_expense_item =  {}
        for item in year_month_other_expense_dict_list:
            cost_item = item["title"]
            cost_item_amount = float(item["expense_amount"])
            if cost_item in totals_by_cost_item:
                totals_by_other_expense_item[cost_item] += cost_item_amount
            else:
                totals_by_other_expense_item[cost_item] = cost_item_amount
        #print(totals_by_cost_item)
        print("\n\nAll other expenses") #---------------------------------------------------------------------------all other expenses
        # print(totals_by_cost_item)
        for keys, values in totals_by_other_expense_item.items():
            print (f"      {keys}{' '*(40 - len(keys))}      : ${' '*(12-len('%.2f' % values))}{values:.2f}") #------other expese itmes
        total_other_expenses = 0
        for item in year_month_other_expense_dict_list:
            total_other_expenses += float(item["expense_amount"])
        print(f"{' '*6}{'-'*61}") #-------------------------------------------------------------------------------------divider
        print(f"{' '*6}Total All other expenses {' '*42} ${' '*(11-len('%.2f' % total_other_expenses))} {total_other_expenses:.2f}") #---total
        # deduct tax and display net income
        print(f"{'-'*76}{'-'*12}") # ----------------------------------------------------------------------------divider before p/l
        net_profit = gross_profit-total_other_expenses
        print(f"Income Before tax{' '*57}${' '*(12-len('%.2f' % net_profit))}{net_profit:.2f}") #------------------income before tax
        tax_amount = net_profit*10/100
        print(f"- Taxes (GST 10%){' '*57}${' '*(12-len('%.2f' % tax_amount))}{tax_amount:.2f}") #------------------tax
        print(f"{'-'*76}{'-'*12}")
        net_income = net_profit-tax_amount
        print(f"Net Income{' '*64}${' '*(12-len('%.2f' % net_income))}{net_income:.2f}") #-----------------------------net income
        print(f"{' '*75} {'='*12}\n") #----------------------------------------------------------------------------divider after p/l
# END - Monthly Profit and loss account Report fUNCTION

# START - Account Statistics FUNCTION
# gross profit margin calculation
def gp_calc(x,y): # used in montly account statistics and total account statistics
    z = lambda x,y: "%.2f" % ((x-y)/x*100)
    return z(x,y)

def account_stats(account_name):
    # income list with month and year
    income_list = []
    for row in full_list_with_month_year(account_name):
        income_list.append(row) if row["type"] == "Income" else None

    # print(income_list)
    # monthly
    list_of_available_months = []
    for row in income_list:
        if row["month_split"] + ' ' + row["year_split"] not in list_of_available_months:
            list_of_available_months.append(row["month_split"] + ' ' + row["year_split"])
    #print(full_list_with_month_year(account_name))
    #print(list_of_available_months) # list of months and years.
    total_income_alltime = 0
    total_expense_alltime = 0
    count_alltime = 0
    for row in full_list_with_month_year(account_name):
        total_income_alltime += float(row["income_amount"])
        total_expense_alltime += float(row["expense_amount"])
        count_alltime += 1 if row["type"] == "Income" else count_alltime ==count_alltime
    # print(total_income_alltime)
    # print(total_expense_alltime)
    # print(count_alltime)
    # display total statistics
    print(f"\nSummary Statistics\n{'-'*100}")
    print(f" Total to-date sales amount   : ${total_income_alltime:.2f}")
    print(f" Total no of sales/income transactions to-date : {count_alltime}")
    print(f" All time average transaction amount per sale : ${total_income_alltime/count_alltime:.2f}")
    print(f" Total to-date expense amount : ${total_expense_alltime:.2f}")
    #print(f" All time Gross profit margin  : {(total_income_alltime-total_expense_alltime)/total_income_alltime*100:.2f}%\n")
    print(f" All time Gross profit margin  : {gp_calc(total_income_alltime,total_expense_alltime)}%\n")
    # monthly statistics
    print(f"\nMonthly Statistics\n{'-'*100}")
    for month_and_year in list_of_available_months:
        total_income = 0
        total_expense = 0
        count = 0
        for row in full_list_with_month_year(account_name):
            if month_and_year == row["month_split"] + ' ' + row["year_split"]:
                total_income += float(row["income_amount"])
                total_expense += float(row["expense_amount"])
                count += 1 if row["type"] == "Income" else count == count
        # display monthly statistics
        print(month_and_year)
        print(f"{'-'*15}")
        print(f" Total monthly sales amount : ${total_income:.2f}")
        print(f" Total no of sales transaction during the month : {count}")
        print(f" average transaction amount per month in {month_and_year} : ${total_income/count:.2f}")
        print(f" Total expenses during the month : ${total_expense:.2f}")
        #print(f" Gross profit margin for {month_and_year} : {(total_income-total_expense)/total_income*100:.2f}%\n")
        print(f" Gross profit margin for {month_and_year} : {gp_calc(total_income,total_expense)}%\n")
        #print(f" Lambda {gp_calc(total_income,total_expense)}")
# END - Account Statistics FUNCTION

# START - Transaction by Customer or Vendor FUNCTION
def track_transactions(account_name):
    # customer list
    customer_list = []
    for row in full_list_with_month_year(account_name):
        if row['customer'].lower() not in customer_list:
            customer_list.append(row["customer"].lower()) if row["customer"] != '0' else None
    #print(customer_list)
    # vendor list
    vendor_list = []
    for row in full_list_with_month_year(account_name):
        if row['vendor'].lower() not in vendor_list:
            vendor_list.append(row["vendor"].lower()) if row["vendor"] != '0' else None
    # print(vendor_list)
    # Transactions by customers
    print(f"{'-'*100}\n{(f'Transacton by Customer for account {account_name}').center(100)}\n{'-'*100}")
    for customer in customer_list:
        transaction_list = []
        total_income = 0
        total_expense = 0
        count = 0
        for row in full_list_with_month_year(account_name):
            if customer == row["customer"].lower():
                transaction_list.append(row)
                total_income += float(row["income_amount"])
                total_expense += float(row["expense_amount"])
                count += 1 if row["type"] == "Income" else count == count
        print(f"\nCustomer Name: {customer.upper()}\n")     #----------------------------------------------------customer
        print(f"       Date{' '*10}Description{' '*33}Amount \n     {'-'*68}")
        for transaction in transaction_list:
            income_str = "%.2f" % float(transaction['income_amount'])
            print(f"      {transaction['transaction_date']}     {transaction['title']}"
            f"{' '*(50-(len(transaction['title'])+len(income_str)))}${float(transaction['income_amount']):.2f} ")
            #print(2*(len(transaction["title"])+len(income_str)))
        print(f" \n     * Total Sales to {customer}  : $ {total_income:.2f}")
        print(f"     * Average spent per transaction by {customer}  : $ {total_income/count:.2f}")
        # Transactions by vendors
    print(f"\n{'-'*100}\n{(f'Transacton by Vendor for account {account_name}').center(100)}\n{'-'*100}")------------------------------------------------------------------------check
    for vendor in vendor_list:
        transaction_list = []
        total_income = 0
        total_expense = 0
        count = 0
        for row in full_list_with_month_year(account_name):
            if vendor == row["vendor"].lower():
                transaction_list.append(row)
                total_income += float(row["income_amount"])
                total_expense += float(row["expense_amount"])
                count += 1 if row["type"] == "Expense" else count == count
        print(f"\nVendor Name: {vendor.upper()}\n")     #----------------------------------------------------vendor
        print(f"       Date{' '*10}Description{' '*33}Amount \n     {'-'*68}")
        for transaction in transaction_list:
            expense_str = "%.2f" % float(transaction["expense_amount"])
            print(f"     {transaction['transaction_date']}     {transaction['title']}"\
            f"{' '*(50-(len(transaction['title'])+len(expense_str)))}${float(transaction['expense_amount']):.2f} ")
            #print(2*(len(transaction["title"])+len(income_str)))
        print(f" \n    *Total Purcahses from {vendor}  : $ {total_expense:.2f}")
        #print(f" Average spent per transaction by {customer}  : $ {total_income/count:.2f}")
# END - Transaction by Customer or Vendor FUNCTION

# END ---------------------- Stretch Goals FUNCTIONS -------------------X

# BUDGET TRACKER ----------------------- --MAIN CODES------------------------------------------------------------- X

# default account - for stretch goal
account_list = ["Lemonade Stand"]
# assign default account to account_name to start with
account_name = account_list[0]
# Display title with default account at the start
print(f"{'=' * 100}\n\n{('BUDGET TRACKER').center(100)}\n\n{'=' * 100}\n\n")

# #### Technical Requirements
# - Load the previously created entries when the user initializes the application
with open("./budget_tracker.csv", "a+", newline='') as file:  # opening the text document in append and read mode
    print(f"\n Previous Transactions for account : {account_name} (default account)\n")
    view_all_previous(account_name)

    # 1.	When I start up the application, I am given the following options:
    # - a.	Add a new entry to the budget tracker
    # - b.	Display the total account balance
    # - c.	View all previous entries
# START - MAIN MENU CODE
input_main = ''
while input_main != '8':
    print(f"\n{'_' * 100}\n\nMAIN MENU - {account_name.upper()}\n{'_' * 100}\n")
    print(f"\n *** You are currently in {account_name.upper()}\n")
    print("1 - Add a new entry to the Budget tracker")
    print("2 - Display the total account balance")
    print("3 - View all previous entries")
    print("\n Stretch goals")
    print("----------------------")
    print("4 - Choose a different account or create a new account")
    print("5 - Monthly Profit and loss account Report")
    print("6 - High Level account Statistics")
    print("7 - Track and analyze transactions by specific customers or vendors")
    print("\n8 - Exit from Budget Tracker\n\n")
    print(f"{'-' * 100}")
    input_main = input(" *   Please enter your choice (1-8): ")
    print(f"{'-' * 100}")
    if input_main == '1': # Add new transaction
        print(f"{'_' * 100}\n\nMain Menu > Add A New Entry To The Budget Tracker - {account_name.upper()}\n{'_' * 100}\n")
        add_new_transaction_def(account_name)  # CALL THE FUNCTION TO ADD NEW TRANSACTION
    elif input_main == '2': # Display total balance
        print(f"{'_' * 100}\n\nMain Menu > Display The Total Account Balance - {account_name.upper()}\n{'_' * 100}\n")
        tot_bal_def(account_name)  # CALL THE FUNCTION TO DISPLAY TOTAL ACCOUNT BALANCE
    elif input_main == '3': # view history
        print(f"{'_' * 100}\n\nMain Menu > View All Previous Entries - {account_name.upper()}\n{'_' * 100}\n")
        print(f"\n Transaction history for account : {account_name}\n")
        view_all_previous(account_name)  # CALL THE FUNCTION TO VIEW ALL PREVIOUS ENTRIES
    # Stretch goal - manage multiple accounts
    elif input_main == '4': # Tested and working
        print(f"{'_' * 100}\n\nMain Menu > Choose A Different Account\n{'_' * 100}\n\n")
        # Display the list of available accounts to choose
        with open("./budget_tracker.csv", "r") as file:
            file.seek(0)
            reader = csv.DictReader(file)
            for row in reader:
                account_list.append(row["account"]) if row["account"] not in account_list else None
        num = 1 # number the available accounts
        for acc in account_list:
            print(f"{num}. {acc}")
            num += 1
        print(f"\n{num}. Create a new Account")
        # get the input from the user
        # print(account_list)
        while True: # syntax from Assignment cheat sheet
            try:
                account_select = input(f"\n{'-' * 100}\n *   Select or Create new account by entering a number (1-{num}): ")
                print(f"{'-' * 100}\n")
                if int(account_select) in range(1,num):
                    account_name = account_list[int(account_select)-1]
                    break
                elif int(account_select) == num:
                    new_account_name = input(f" * Enter new account name :")
                    account_name = new_account_name
                    print("\n* NOTE: YOUR NEW ACCOUNT WON'T SAVE UNTIL YOU ENTER ATLEAST 1 BUDGET ITEM. *\n")
                    print(f" Please add a transaction (budget item) to save '{account_name}'")
                    add_new_transaction_def(account_name) # -------------------------------------see if this code works
                    break
                else:
                    print(f" => Invalid answer! Enter only numbers between 1-{num}. ")
                    continue
            except ValueError as ve:
                # Customize the error message for non-numeric inputs
                if str(ve) == "invalid literal for int() with base 10: ''":
                    print("You did not enter a number. Please enter a valid positive number.")
                else:
                    # Print the specific error message for the ValueError raised
                    print(ve)
                    print("Let's try again...\n")
    # End code - Stretch goal - manage multiple accounts

    elif input_main == '5': # pnl
        print(f"{'_' * 100}\n\nMain Menu > Monthly Profit And Loss Report - {account_name.upper()}\n{'_' * 100}\n")
        monthly_pnl(account_name)
    elif input_main == '6': # stats
        print(f"{'_' * 100}\n\nMain Menu > High Level Account Statistics - {account_name.upper()}\n{'_' * 100}\n")
        account_stats(account_name)
    elif input_main == '7': # track and analyse
        print(f"{'_' * 100}\n\nMain Menu > Track and analyze transactions - {account_name.upper()}\n{'_' * 100}\n")
        track_transactions(account_name)
    elif input_main != '8':  # FOR ALL THE INPUTS THAT ARE NOT EQUAL 1-8
        print(" => Invalid choice! Try again.")
# END - MAIN MENU CODE ------------------------------------------------------------------------------------------------- x
# Display thank you message When user exit from the app.
print(f"\n{'#' * 100}\nThank you for using 21st Century Budget Tracker.\nSee you next time!\n\n")
file.close()
# x --------------------------------------------------END CODING --------------------------------------------------- x
