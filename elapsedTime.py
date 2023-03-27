from datetime import datetime, timedelta

def calculate_time_spent(Dict):
    arrivalDeparture = {}
    for name, data in Dict.items():
        time_spent = timedelta()
        for i in range(len(data)):
            location = tuple(data[i][1:3])
            time = datetime.strptime(data[i][3], '%I:%M %p')
            date = datetime.strptime(data[i][4], '%Y-%m-%d')
            battery = data[i][5]
            if i == 0:
                arrival_time = time
                last_location = location
            if i == len(data)-1:
                departure_time = time + timedelta(minutes=10)
                total_time_spent = time_spent + (departure_time - arrival_time)
                arrivalDeparture[name] = (name, last_location[0], last_location[1], arrival_time.strftime('%H:%M:%S'), departure_time.strftime('%H:%M:%S'), str(total_time_spent))
            elif location != last_location:
                departure_time = time
                total_time_spent = time_spent + (departure_time - arrival_time)
                arrivalDeparture[name] = (name, last_location[0], last_location[1], arrival_time.strftime('%H:%M:%S'), departure_time.strftime('%H:%M:%S'), str(total_time_spent))
                time_spent = timedelta()
                arrival_time = time
                last_location = location
            else:
                time_spent += time - datetime.combine(date, datetime.min.time())
            if i == len(data)-1 and name not in arrivalDeparture:
                departure_time = time + timedelta(minutes=10)
                total_time_spent = time_spent + (departure_time - arrival_time)
                arrivalDeparture[name] = (name, last_location[0], last_location[1], arrival_time.strftime('%H:%M:%S'), departure_time.strftime('%H:%M:%S'), str(total_time_spent))
    return arrivalDeparture