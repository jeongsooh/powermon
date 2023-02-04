from django.db import connection
from django.views import View
import time
import json

class DataView(View):
    def get(self, request):
        # Connect to the MySQL database
        cursor = connection.cursor()

        # Initialize variables
        data = []
        start_time = time.time()
        current_time = time.gmtime()
        current_minutes = current_time.tm_min

        # Continuously read data from the socket
        while True:
            # Read 20 integers from the socket
            values = socket.recv(20*4) # assuming integers are 4 bytes each
            data.extend(values)

            # If 15 minutes has passed
            current_time = time.gmtime()
            if current_time.tm_min - current_minutes >= 15:
                # Calculate the average of the data
                avg = sum(data) / len(data)

                # Insert the average into the MySQL database
                cursor.execute("INSERT INTO data (value,time) VALUES (%s,%s)", (avg,current_time))
                connection.commit()

                # Clear the data list and reset the start time and current_minutes
                data = []
                start_time = time.time()
                current_minutes = current_time.tm_min
                
                # Prepare data to send to the browser
                json_data = json.dumps(data)
                
                # Return the data
                return JsonResponse(json_data, safe=False)

"""
In this example, it uses gmtime() to get the current time in UTC format, and compares the current minute 
with the current_minutes variable. If 15 minutes have passed, it calculates the average, inserts that average into the database, 
clear the data list, reset the start time and current_minutes, and prepare the data to send to the browser.

It's also important to note that the above code will only return the data once every 15 minutes, you could add some logic 
to return the data every 15 minutes or use some other ways like set a timer to return the data.
"""
