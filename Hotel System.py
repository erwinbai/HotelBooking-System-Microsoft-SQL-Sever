import pyodbc

#connection = pyodbc.connect('driver={SQL Server}; Server=cypress.csil.sfu.ca;Trusted_Connection=yes;')
connection = pyodbc.connect('driver={SQL Server};Server=cypress.csil.sfu.ca;uid=s_ebai;pwd=feLMmEnNfGJF6MN2')

cursor = connection.cursor()

## q3
##def writecom():

    #guest_name = input("please input your name:")
    #command1 = ("SELECT * FROM Reviews r WHERE r.guest_name = ?")
    #cursor.execute(command1, guest_name)
    #List = []
    #results = cursor.fetchone()
    #while results:
            #List.append(results)
    #print (List)

    #index = int(input("select which one u want to comment:"))
    #com = input("enter your comment:")


    #command2 = ("UPDATE Reviews SET r.comments = ? WHERE r.index = ?")
    #cursor.execute(command2, com, index)
    


print('Welcome to Airbnb, how may I help you?')

ans=True
while ans:
    print ("""      1.Search Listings
      2.Book Listing
      3.Write Review
      4.Exit/Quit""")
    ans=input("What would you like to do? ")
    #Question 1 Book Listing
    #===========================================================================================================
    #User Interface
    if ans== "1":
        print("Please enter in the following ")

        minimum = input("minimum price: ")

        maximum = input("maximum price: ")

        bedroom = input("number of bedrooms: ")

        print("In the form of year-month-date")
        start = input("start date: ")
        #start = '2016-03-07'
        #end = '2016-03-20'
        end = input("end date: ")
    #============================================================================================================
    #Selecting and creating a 2D array with the selected column
        SQLcommand = ("""SELECT A.id, A.name, A.description, A.number_of_bedrooms,sum(price) as price 
                         FROM (Select DISTINCT L.id,L.name, L.description, L.number_of_bedrooms,c.price, C.date
                               From Listings L, Calendar C
                               Where L.id = C.listing_id
                               and C.available = 1
                               and C.price >= ?
                               and C.price <= ?
                               and L.number_of_bedrooms = ?
                               and C.date >= ?
                               and C.date <= ?) A
                       GROUP BY A.id,A.name,A.description,A.number_of_bedrooms
                       HAVING count(id) > datediff(day,?,?)
                      """)
        cursor.execute(SQLcommand, minimum,maximum,bedroom,start,end,start,end)
        #cursor.execute(SQLcommand, 90,95,1,'2016-03-07','2017-12-30','2016-03-07','2017-12-30')
    
    
        List = []      
        results = cursor.fetchone()
        i = 0
        while results:
            List.append(results)
            print("Index: ", i)
            i = i+1
            print("Listing id:" + str(results[0]))
            print("Name:" + str(results[1]))
            print("Description:" + str(results[2])[:25])
            print("Number_of_bedrooms:" + str(results[3]))
            print("Price:" + str(results[4]))
            print("\n")
            results = cursor.fetchone()

        if not List:
            print("No record found, please try again with different entry")

            
    #Question 2
    #===============================================================================================================
    elif ans=="2":
        print("\nPlease choose a listing from the filtered list")
        print("\n")
        index = int(input("Please chose an avaliable list to book, enter the INDEX number: "))

        cursor.execute("SELECT COUNT (*) FROM Bookings")
        rowcount = cursor.fetchone()[0]
        
        name = input("Please enter your name: ")        
        numberg = int(input("Please input number of guest: "))
        
        SQLcommand2 = ("INSERT INTO Bookings (id, listing_id, guest_name, stay_from, stay_to, number_of_guests) VALUES (?,?,?,?,?,?)")  
        cursor.execute(SQLcommand2, rowcount + 1, List[index][0], name, start, end, numberg)
        cursor.commit()
        print("Booking completed")
    #Question 
    #=============================================================================================================== 
    elif ans=="3":
        print("\nWrite Review")
         
        name = str(input("What is your name:"))
        command1 = ("SELECT * FROM Bookings b WHERE b.guest_name = ?")
        cursor.execute(command1, name)
        List = []
        results = cursor.fetchone()
        while results:
            List.append(results)
            print("Index: " + str(results[0]))
            print("Listing id: " + str(results[1]))
            print("Guest name: " + str(results[2]))
            print("Stay from: " + str(results[3]))
            print("stay to: " + str(results[4]))
            print("Number of guest: " + str(results[5]))
            print("\n")
            results = cursor.fetchone()

        if not list:
            print("You haven't book any room yet!Cannot write review")
        else:
            index=int(input("Enter the index of the booked list you want to review: "))
            comment = input("Enter your comment")
            cursor.execute("SELECT COUNT (*) FROM Reviews")
            rowcount = cursor.fetchone()[0]
            SQLcommand3 = ("INSERT INTO Reviews (id, listing_id, comments, guest_name) VALUES (?,?,?,?)")
            cursor.execute(SQLcommand3, rowcount + 1, List[index-1][1], comment, name)
            cursor.commit()
            print("writing completed")
  
    elif ans=="4":
        print("\n Thank you for using Airbnb !")
        ans = None
    else:
         print("\nNot Valid Choice Try again")



connection.close()
