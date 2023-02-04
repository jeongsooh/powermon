import mysql.connector
import time
import matplotlib.pyplot as plt

# Connect to the MySQL database
cnx = mysql.connector.connect(user='your_username',
                              password='your_password',
                              host='your_host',
                              database='your_db')
cursor = cnx.cursor()

# Initialize variables
data = []
start_time = time.time()

# Continuously read data from the socket
while True:
    # Read 20 integers from the socket
    values = socket.recv(20*4) # assuming integers are 4 bytes each
    data.extend(values)
    
    # If one second has passed
    if time.time() - start_time >= 1:
        # Calculate the average of the data
        avg = sum(data) / len(data)
        
        # Insert the average into the MySQL database
        cursor.execute("INSERT INTO data (value) VALUES (%s)", (avg,))
        cnx.commit()
        
        # Clear the data list and reset the start time
        data = []
        start_time = time.time()
        
        # Plot the data and show the graph
        plt.plot(data)
        plt.show()


"""
In this example, the DataView class inherits from Django's View class, and overrides the get() method to handle incoming GET requests. 
It opens a connection to the MySQL database and continuously reads data from the socket. When one second of data has been received, 
it calculates the average, inserts that average into the database, clear the data list and reset the start time. and prepare the data 
to send to the browser as json format and return it by JsonResponse.

You will have to create the url pattern in urls.py file to map the URL to this view and also you have to design a template to display 
the graph by using javascript library like chart.js or d3.js

It's important to note that this is just an example and is not guaranteed to work perfectly as is, you may need to adjust it 
to fit your specific requirements.
"""