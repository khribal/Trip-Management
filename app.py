from flask import Flask, render_template, url_for, request, redirect
import csv 
from datetime import datetime
from operator import itemgetter

app = Flask(__name__)

#globals 
TRIPS_PATH = app.root_path + '/trips.csv'
MEMBERS_PATH = app.root_path + '/members.csv'
TRIPS_KEYS = ['name','level','start_date','location','length','leader','cost','description']
MEMBERS_KEYS = ['name','dob','email','address','phone']

# read dictionaries with trip info into one list
def get_trips():
    with open(TRIPS_PATH, 'r') as csvfile:
        data = csv.DictReader(csvfile)
        trips = list(data)
        return trips


# read dictionaries with member info into one list
def get_members():
    with open(MEMBERS_PATH, 'r') as csvfile:
        data = csv.DictReader(csvfile)
        members = list(data)
        return members


def set_trips(trip_dict):
    with open('trips.csv', 'w', newline='') as csvfile:
        csv_writer = csv.DictWriter(csvfile,fieldnames=TRIPS_KEYS)
        csv_writer.writeheader()
        for row in trip_dict:
            csv_writer.writerow(row)

def set_members(member_dict):
    with open('members.csv', 'w', newline='') as csvfile:
        csv_writer = csv.DictWriter(csvfile,fieldnames=MEMBERS_KEYS)
        csv_writer.writeheader()
        for row in member_dict:
            csv_writer.writerow(row)

@app.route('/')
def index():
    return render_template('index.html')


# rewrite member date as a datetime, then sort by member['dob'], render template using sorted
# list of dictionaries
@app.route('/members')
def members():
    members = get_members()
    for member in members:
        member['dob'] = datetime.strptime(member['dob'], '%Y-%m-%d').date()
    member_sorted = sorted(members, key=itemgetter('dob'))
    return render_template('members.html', members=member_sorted)

# rewrite trip date as a datetime, then sort by trip['start_date'], render template using sorted
# list of dictionaries
@app.route('/trips')
def trips():
    trips = get_trips()
    for trip in trips:
        trip['start_date'] = datetime.strptime(trip['start_date'], '%Y-%m-%d').date()
    trips_sorted = sorted(trips, key=itemgetter('start_date'))
    return render_template('trips.html', trips=trips_sorted)


# @app.route('/members/<member_id>')
# def member(member_id=None):
#         members = get_members()
#         if member_id:
#              return render_template('member.html', member=members[int(member_id)])
#         else:
#             return render_template('members.html', m_list=members)

#set trip_id to none, render template and change trip index to an int
#renders template for trip dictionary according to index

@app.route('/trip/<trip_id>')
def trip(trip_id=None):
    trips=get_trips()
    if trip_id:
        return render_template('trip.html', trip=trips[int(trip_id)], trip_id=trip_id)
    else:
        return render_template('trips.html')
    


# @app.route('/trips/add')
# def trip_form():
#     return render_template('trip_form.html')

@app.route('/trips/<trip_id>/edit')
def edit(trip_id=None):
    trips=get_trips()
    if trip_id:
        return render_template('trip_form.html', trip=trips[int(trip_id)])
    else:
        return render_template('trips_form.html', trip=trips[int(trip_id)], trip_id=trip_id)
    

@app.route('/trips/add', methods=['GET', 'POST'])
def add_trip():
    if request.method == 'POST':
        
        name = request.form['name']
        level = request.form['level']
        start_date = request.form['start_date']
        location = request.form['location']
        length = request.form['length']
        leader = request.form['leader']
        cost = request.form['cost']
        description = request.form['description']

        
        trips_dict = {"name": name, "level": level, "start_date": start_date, "location": location, "length": length, "leader": leader, "cost": cost, "description": description}
        trips = get_trips()
        trips.append(trips_dict)
        set_trips(trips)

        return redirect(url_for('trips'))
    else: 
        return render_template('trip_form.html')
    



@app.route('/member/add', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        
        name = request.form['name']
        dob = request.form['dob']
        email = request.form['email']
        address = request.form['address']
        phone = request.form['phone']
        
        members_dict = {"name": name, "dob": dob, "email": email, "address": address, "phone": phone}
        members = get_members()
        members.append(members_dict)
        set_members(members)

        return redirect(url_for('members'))
    else: 
        return render_template('member_form.html')
    

