from django.test import TestCase
from queue import Queue

# Create your tests here.

data = ['2023-01-18 15:58:51.325644', 'gre000004', 3, 912, 99, 212]
print(data[0], data[1],data[2],data[3],data[4],data[5])

temp_queue = Queue()

temp_queue.put(data)

recv_data = temp_queue.get()
print(recv_data)

ok_date=str(recv_data[0][:22])
print(ok_date)

st=list(str("abcde"))
print(st)
sensor_val=str(''.join(st[:]))
print(sensor_val)

test = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(sum(test)/len(test))