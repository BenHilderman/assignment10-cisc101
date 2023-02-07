"""
This program displays Tim Hortons orders and has actions the user can do revolving the orders
Author:  Benjamin Hilderman
Student Number: 20374738
Date:  Nov 28, 2022
"""

import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def readWords(urlLink):
    """
    This function reads the data from the link provided and returns a dictionary organized by each order and its contents
    Parameters: urlLink - string
    Return Value: dictionary
    """
    try:
        itemsList = []
        response = urllib.request.urlopen(urlLink)
        data = response.readline().decode('utf-8')
        # removing last character of first line
        data = str(data)[:-1]
    except:
        # if url gets an error
        print("The URL is invalid")
        return []
    
    while len(data) != 0:
        # adding each line to list
        itemsList += [data]
        data = response.readline().decode('utf-8')
        # removing last character of each line
        data = str(data)[:-1]

    # initializing dictionary
    ordersDictionary = {}
    counter = -1

    # turning list into organized dictionary
    for orders in itemsList:
        counter += 1
        # split values and getting first value which is the order id
        ordersSplit = orders.split()
        itemId = ordersSplit[0]

        # finding the last value because they vary per order (due to the number of items ordered)
        max = 0
        for j in range(len(ordersSplit)):
            if j > max:
                max = j

        # the last value of the order is the price of the item
        itemPrice = ordersSplit[max]
        item = ''

        # getting the strings inbetween the order number and price which is the items ordered
        for itemsOrdered in range(1, max):
            item = item + ' ' + ordersSplit[itemsOrdered]
        item = item[1:]

        # creating organized dictionary with values found: order number, item(s), and order price 
        ordersDictionary[itemId] = {'item': item, 'price': itemPrice}
    return ordersDictionary

def displayOrders(ordersDictionary):
    """
    This function uses the orders dictionary to print each order line by line
    Parameters: ordersDictionary - dictionary
    Return Value: none
    """
    # looping each order and printing them line by line
    for id in ordersDictionary:
        print("Order " + str(id) + ": " + ordersDictionary[str(id)]['item'] + " $" + ordersDictionary[str(id)]['price'])

def orderSearch(ordersDictionary, id):
    """
    This function looks for the order that corresponds with the id, and if found, prints its items and price
    Parameters: ordersDictionary - dictionary, id - string
    Return Value: none
    """
    # using for loop to see if id inputted is found in dictionary of orders
    orderInput = "Invalid"
    for i in ordersDictionary:
        if id == i:
            orderInput = "Valid"

    # if the order is found, print its values
    if orderInput == "Valid":
        print("Order " + str(id) + ": " + ordersDictionary[str(id)]['item'] + " $" + ordersDictionary[str(id)]['price'])
    
    # if order is not found print "Order ID is not found"
    else: print("Order ID is not found")

def changeOrder(ordersDictionary, id):
    """
    This function finds the order corresponding to the id parameter, asks the user what the new values of the order should be, and updates the order with the values inputted
    Parameters: ordersDictionary - dictionary, id - string
    Return Value: dictionary
    """
    # using for loop to see if id inputted is found in dictionary of orders
    orderInput = "Invalid"
    for i in ordersDictionary:
        if id == i:
            orderInput = "Valid"

    # if order is found
    if orderInput == "Valid":
        # print current items in order
        print("The current item(s) for order " + str(id) + " is/are: " + ordersDictionary[str(id)]['item'])
        # ask user what they want the updates items to be
        ordersDictionary[str(id)]['item'] = input("Input the the updated food items for order " + str(id) + ": ")
        # return updated dictionary of orders
        return ordersDictionary

    # if order is not found print "Order ID is not found"
    else:
        print("Order ID is not found")
        return ordersDictionary

def donutSearch(ordersDictionary):
    """
    This function finds the orders that contain a donut, and prints them
    Parameters: ordersDictionary - dictionary
    Return Value: none
    """
    # looping dictionary to search each line
    for key, value in ordersDictionary.items():
        # split values in order
        splitValues = value['item'].split()
        # checks if order contains the value "Donut"
        for i in splitValues:
            if i == "Donut" or i == "donut":
                print("Order " + str(key) + " contains a donut(s)")

def removeOrder(ordersDictionary, id):
    """
    This function finds the order corresponding to the id parameter, and removes it from the dictionary
    Parameters: ordersDictionary - dictionary, id - string
    Return Value: dictionary
    """
    # using for loop to see if id inputted is found in dictionary of orders
    orderInput = "Invalid"
    for i in ordersDictionary:
        if id == i:
            orderInput = "Valid"

    # if order is found delete it        
    if orderInput == "Valid":
        del ordersDictionary[str(id)]
        return ordersDictionary

    # if order is not found print "Order ID is not found"
    else:
        print("Order ID is not found")
        return ordersDictionary

def withOutDonut(ordersDictionary):
    """
    This function searches all of the orders, and counts up the total cost of the orders without donuts
    Parameters: ordersDictionary - dictionary
    Return Value: float
    """
    total = 0
    # looping dictionary to search each line
    for key, value in ordersDictionary.items():

        # split values in order
        splitValues = value['item'].split()

        # checks if order contains the value "donut" or "Donut"
        donut = "no"
        for i in splitValues:
            if i == "Donut" or i == "donut":
                donut = "yes"

        # add price to total if order doesnt contain the value "donut" or "Donut"
        if donut == "no":
            total += float(ordersDictionary[key]['price'])

    # round total cost to 2 decimals
    total = round(total, 2)
    return total

def main():
    """
    This function displays the menu, which gives the user options of which function they can run. Ends when user inputs "6"
    Parameters: none
    Return Value: none
    """
    # get values (orders) from link
    ordersDictionary = readWords('https://research.cs.queensu.ca/home/cords2/timHortons.txt')
    # call display orders function
    displayOrders(ordersDictionary)

    menuLoop = 'loop'
    # menu continues to loop when menuLoop == "loop"
    while menuLoop == 'loop':
        userChoice = input('Input the corresponding number to the task you want to run:\n(1) Search for an order\n(2) Change order\n(3) Search for orders with donut(s)\n(4) Remove order\n(5) Total cost of orders without donuts\n(6) Exit menu\n')
        
        # user inputs 1
        if userChoice == '1':
            # displays the current order numbers for the user to choose from
            orderIDs = ''
            for i in ordersDictionary:
                orderIDs += ", " + i
            orderIDs = orderIDs[2:]
            # user inputs what order ID they want to seach
            userOrderIdChoice = input("Input the order ID you want to search: " + orderIDs + "\n")
            # call order search function with user input and dictionary of orders
            orderSearch(ordersDictionary, userOrderIdChoice)
        
        # user inputs 2
        elif userChoice == '2':
            # displays the current order numbers for the user to choose from
            orderIDs = ''
            for i in ordersDictionary:
                orderIDs += ", " + i
            orderIDs = orderIDs[2:]
            # user inputs what order ID they want to change
            userOrderIdChoice = input("Input the order ID you want to change: " + orderIDs + "\n")
            # call change order function with user input and dictionary of orders
            ordersDictionary = (changeOrder(ordersDictionary, userOrderIdChoice))
            # call display orders function
            displayOrders(ordersDictionary)
        
        # user inputs 3
        elif userChoice == '3':
            # call donutSearch function with dictionary of orders
            donutSearch(ordersDictionary)
        
        # user inputs 4
        elif userChoice == '4':
            # displays the current order numbers for the user to choose from
            orderIDs = ''
            for i in ordersDictionary:
                orderIDs += ", " + i
            orderIDs = orderIDs[2:]
            # asks user which order they want to remove, user inputs a value
            userOrderIdChoice = input("Input the order ID you want to remove: " + orderIDs + "\n")
            # call removeOrder function with user choice and dictionary of orders
            ordersDictionary = removeOrder(ordersDictionary, userOrderIdChoice)
            # call display orders function
            displayOrders(ordersDictionary)

        # user inputs 5
        elif userChoice == '5':
            # call withOutDonut function with dictionary of orders as the parameter, and print the value in a string
            print("The total price of all orders that do not contain donuts is: $" + str(withOutDonut(ordersDictionary)))
        
        # user inputs 6
        elif userChoice == '6':
            menuLoop = "Exit"
        
        # user inputs a value that isn't 1-6
        else:
            print("You entered an invalid value...")
main()