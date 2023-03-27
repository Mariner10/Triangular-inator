from datetime import datetime

def create_location_dictionary(Dict,accuracy):
    locations = {}
    for name, value in Dict.items():
        for item in value:
            #The accuracy variable determines whether to assess the data as accruately as the coordinate decimals go.
            
            #The key is as follows:
            #The units digit (one decimal degree) gives a position up to 111 kilometers (60 nautical miles, about 69 miles). It can tell us roughly what large state or country we are in.

            #The first decimal place is worth up to 11.1 km: it can distinguish the position of one large city from a neighboring large city.

            #The third decimal place is worth up to 110 m: it can identify a large agricultural field or institutional campus.

            #The fourth decimal place is worth up to 11 m: it can identify a parcel of land. It is comparable to the typical accuracy of an uncorrected GPS unit with no interference.

            #The fifth decimal place is worth up to 1.1 m: it distinguish trees from each other. Accuracy to this level with commercial GPS units can only be achieved with differential correction.

            #The sixth decimal place is worth up to 0.11 m: you can use this for laying out structures in detail, for designing landscapes, building roads.
            
            lat = round(float(item[1]), accuracy)
            long = round(float(item[2]), accuracy)
            coord_str = f"{lat}, {long}"
            day = datetime.strptime(item[4], "%Y-%m-%d").strftime("%A")
            fixTime = str(item[3])
            doubleTime = fixTime.split(" ")
            strTime = doubleTime[0]
            time = datetime.strptime(strTime, "%H:%M").strftime("%H:%M")
            if coord_str in locations:
                locations[coord_str]['count'] += 1
                locations[coord_str]['days_visited'].append((day, time, name))
            else:
                locations[coord_str] = {'count': 1, 'days_visited': [(day, time, name)]}

    return locations



def clean_location_dictionary(locations,visit_count):
    # Remove locations that are visited less than 10 times
    locations = {k:v for k,v in locations.items() if v['count'] >= visit_count}

    persons = {}
    for coord_str, data in locations.items():
        prev_dt = None
        for i, visit_data in enumerate(data['days_visited']):
            day, time, name = visit_data
            if name in persons:
                if prev_dt is not None:
                    # Calculate elapsed time since last visit, ignoring gaps longer than 30 minutes
                    curr_dt = datetime.strptime(f"{day} {time}", "%A %H:%M")
                    if (curr_dt - prev_dt).total_seconds() // 60 > 30:
                        prev_dt = None
                    else:
                        elapsed_time = int((curr_dt - prev_dt).total_seconds() // 60)
                        persons[name].append({'coordinates': coord_str, 'day': day, 'time': time, 'elapsed_time': elapsed_time})
                else:
                    persons[name].append({'coordinates': coord_str, 'day': day, 'time': time, 'elapsed_time': 0})
                prev_dt = datetime.strptime(f"{day} {time}", "%A %H:%M")
            else:
                persons[name] = [{'coordinates': coord_str, 'day': day, 'time': time, 'elapsed_time': 0}]
                prev_dt = datetime.strptime(f"{day} {time}", "%A %H:%M")
    return persons