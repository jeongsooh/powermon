# Tuple print

# result = [('power', 100)]

# print(result[0][1])
# print(result[0].get_field())

# a = 12.2345
# print('data = {:.2f}'.format(a))
sensor_id ="GRE000202"
m_fields = ["power", "voltage", "powerfactor"]
m_phase = [0, 1, 2]
for phase_id in m_phase:
  for m_field in m_fields:
    # query = 'from(bucket:"powermon")\
    # |> range(start: -15m)\
    # |> filter(fn:(r) => r._measurement == "power_data")\
    # |> filter(fn:(r) => r.sensor_id == "GRE000202")\
    # |> filter(fn:(r) => r.phase_id == "0")\
    # |> filter(fn:(r) => r._field == "' + m_field + '")'

    # print(query)


    query = 'from(bucket:"powermon")\
    |> range(start: -15m)\
    |> filter(fn:(r) => r._measurement == "power_data")\
    |> filter(fn:(r) => r.sensor_id == "' + sensor_id + '")\
    |> filter(fn:(r) => r.phase_id == "' + str(phase_id) + '")\
    |> filter(fn:(r) => r._field == "' + m_field + '")'

    print(query)