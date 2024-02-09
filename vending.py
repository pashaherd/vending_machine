import re

def sortInputs(input,method):
    for i in range(len(input) - 1):
        if method == "Uni":
            code1 = ord(input[i])
            code2 = ord(input[i + 1])
            if code1 > code2:
                swap = input[i]
                input[i] = input[i + 1]
                input[i + 1] = swap

                i = 0 
        if method == "Col":
            if input[i]["position"] > input[i + 1]["position"]:
                swap = input[i]
                input[i] = input[i + 1]
                input[i + 1] = swap

                i = 0
    return input

class VendingMachine:
    def __init__(self,rows,columns, depth):
        self.rows = int(rows)
        self.columns = int(columns)
        self.depth = int(depth)
        self.wallet = 0
        machine = {}
        char_code = 65
        for i in range(self.rows):
            machine[f"{chr(char_code + i)}"] = []
        
        self.machine = machine
        
    
    def stock(self,rows,columns):
        machine = self.machine
        max_columns = self.columns
        max_depth = self.depth
        response = {}
        error = False

        for i in range(len(rows)):
            for j in range(len(columns[i])):
                find_match = None
                k = 0 
                while k < len(machine[rows[i]]):
                    if machine[rows[i]][k]["position"] == columns[i][j]["position"]:
                        find_match = machine[rows[i]][k]

                    k = k + 1
            
                if find_match:
                    total_stock = find_match["stock"] + columns[i][j]["stock"]
                    if total_stock > max_depth:
                        error = True
                        response["error"] = f"OverStock At {rows[i]}{j}"
                        response["location"] = f"{rows[i]}{j}"
                        continue
                    elif find_match["name"] != columns[i][j]["name"]:
                        error = True
                        response["error"] = f"{find_match['name']} currently occupies {rows[i]}{j}"
                        response["location"] = f"{rows[i]}{j}"
                        continue
                    else:
                        position = find_match["position"]            
                        machine[rows[i]][position]["stock"] = total_stock
                else:
                    
                    if columns[i][j]["position"] > max_columns:
                       error = True
                       response["error"] = f"Column Doesnt Exist {rows[i]}{columns[i][j]['position']}"
                       response["location"] = f"{rows[i]}{j}"
                       continue
                    elif columns[i][j]["stock"] > max_depth:
                        error = True
                        response["error"] = f"OverStock at {rows[i]}{columns[i][j]['position']}"
                        response["location"] = f"{rows[i]}{j}" 
                    else:
                       machine[rows[i]].append(columns[i][j])
        if error:
            return response
        return True
        
        
    def view(self):
        print(self.machine)
        print(f"Current Balance:{self.wallet}")
    def sort(self):
        machine = self.machine
        for _,columns in machine.items():
            length = len(columns)
            for i in range(length - 1):
                if columns[i]["position"] > columns[i + 1]["position"]:
                    swap = columns[i]
                    columns[i] = columns[i + 1]
                    columns[i + 1] = swap
                    i = 0 
        return 
    def buy(self,selection,payment,position):
        machine = self.machine
        row = selection[0]

        if machine[row][position]["stock"] <= 0:
            return None

        if machine[row][position]["price"] - payment > 0:
            return False 
        
        self.wallet = self.wallet + payment
        machine[row][position]["stock"] = machine[row][position]["stock"] - 1
         
        change = payment - machine[row][position]["price"]

        if machine[row][position]["stock"] <= 0:
            del machine[row][position] 
        return {"change":change} 
    

max_choices = 4
columns_regex = r"\w+\,\d+\,\d+\,\d+\.\d+"
rows_regex = r"[A-Z]+(\,+)?"
select_regex = r"[A-Z]\d" 
errors_index = 1
error_count = 0
def main():
    global errors_index
    global error_count

    print(f"Welcome To VendMart!\n"
          f"Where all your snacking dreams come true\n"
          f"leave at anytime with exit keyword")
    print(f"Create Your Vending Machine In 3 Easy Steps!")

    vending_machine = None
    while True:
        rows = input(f"How Many Rows? ")
        columns = input(f"How Many Columns? ")
        depth = input(f"How Many Slots Should Each Column Contain? ")
    
        if rows.isdigit() and columns.isdigit() and depth.isdigit():         
           vending_machine = VendingMachine(rows,columns,depth)
           break
        else:
           print(f"Invalid Entry, Please Try Again")
    while True:
        print(f"Navigation\n"
              f"1.Stock Machine\n"
              f"2.View Machine\n"
              f"3.Buy\n"
              f"4.Exit")
        option = input("Enter Choice ")
        
        if not option.isdigit():
           print(f"Invalid Entry")
           continue
        
        option = int(option)
        if option == 4:
            print("goodbye")
            break
        elif option > max_choices:
            print(f"Option Doesnt Exist")
        elif option == 1:
            stocked_columns = []
            row_input = input(f"List Rows Are You Stocking? ")

            if not re.match(rows_regex,row_input):
                if error_count < 3:
                    error_count = error_count + 1
                    print(f"Couldnt Process Columns Due to Invalid Entry\n"
                          f"Accepted Format: X,Y,Z")
                    continue
                else:
                    print("Aborted")
                    break
             
            
            stocked_rows = row_input.split(',')
            if len(stocked_rows) > vending_machine.rows:
                print(f"Too Many Rows, Max Rows:{vending_machine.rows}")
                continue
            column_input = None
            abort = False
            for i in range(len(stocked_rows)):
                if abort:
                    break
                stocked_columns.append([])
                while True:
                    column_input = input(f"Insert Column For Row {stocked_rows[i]}: ")
                    

                    if re.match(columns_regex, column_input):

                        process_column = column_input.split(",")
                        name = process_column[0]
                        position = int(process_column[1])
                        stock = int(process_column[2])
                        price = 0

                        if process_column[3]:
                            price = float(process_column[3])
                        
                        if stock > vending_machine.depth:
                            print(f"Overstock at {stocked_rows[i]}{position}")
                            continue
                        elif position > vending_machine.columns:
                            print(f"Position {stocked_rows[i]}{position} Doesnt Exist")
                            continue
                        elif len(stocked_columns[i]) >= vending_machine.columns:
                            print(f"Row Full")
                            break
                  
                        
                        stocked_columns[i].append({"name":name, "position":position, "stock":stock, "price":price})
                    
                        continue_additions = input("Finshed? Enter Yes or No ")  
                        if continue_additions == "Yes":
                            break 
                    else:
                        if error_count <= 3:
                            print(f"Couldnt Process Columns Due to Invalid Entry\n"
                                  f"Accepted Format: Name,Position,Stock,Price")
                            error_count = error_count + 1 
                        else:
                            print("Aborted")
                            abort = True
                            break 
            if not abort:
                result = vending_machine.stock(stocked_rows, stocked_columns)
                if result != True:
                    location = result["location"]
                    msg = result["error"]
                    print(f"unsuccessful stock at position {location}\n"
                          f"{msg}")

                    errors_index = errors_index + 1
                else:
                    vending_machine.sort()
        elif option == 2:
            vending_machine.view()
        elif option == 3:
            reject_count = 0
            while True:
                print(f"Purchase Available Goods Now! use \"exit\" to leave")
                vending_machine.view()

            
                selection = input(f"Enter Choice: ")

                if re.match(select_regex, selection):
                    exists = False
                    position = 0
                    number = int(selection[1])
                    char_code = ord(selection[0])

                    if char_code - 64 > vending_machine.rows:
                        print(f"{selection[0]} doesnt exist")
                        continue

                    row = vending_machine.machine[selection[0]]
                    for i in range(len(row)):
                        if row[i]["position"] == number:
                           position = i
                           exists = True
                    if exists:
                        item = vending_machine.machine[selection[0]][position]
                        item_price = item["price"]
                        print(f"Cost: {item_price}")
                        purchase = input("Accept[1] or Reject[0]: ")
                        purchase = int(purchase)

                        if purchase == 1:
                            payment = input("Pay Now: ")
                            payment = float(payment) 

                            sufficent_funds = vending_machine.buy(selection, payment, position)

                            if sufficent_funds:
                               print(f"Vend Successful:{item}\n"
                                     f"Change: {sufficent_funds['change']}")
                               break
                            elif sufficent_funds == None:
                                print(f"Sold Out")
                            else:
                               reject_count = reject_count + 1
                               print(f"Insufficient Funds")
                        else:
                            reject_count = reject_count + 1
                            print("Purchase Rejected")
                    else:
                        print(f"Position {number} in Row {selection[0]} doesnt exist")
                else:
                    if not selection == "exit":
                        print("Invalid Entry")
                
                if reject_count > 5 or selection == 'exit':
                    break
                   


main()

                
                