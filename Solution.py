import argparse
import json
import os

#defining globals
NUM_ROW_SEATS = 8
NUM_ROWS = 20
START_INDEX = 0
ROW_INDEX = 'A'
SEATS_FILE = '/Users/rojah/airline_reservation.json'



def load_seats():
    with open(SEATS_FILE, 'r') as f:
        return json.load(f)

def store_seats(data):
    with open(SEATS_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def check_base_cases(row, seat_num, num_seats):
    if (row < START_INDEX or row >= NUM_ROWS) or (seat_num <0 or seat_num >=NUM_ROW_SEATS) or (num_seats<1 or (seat_num + num_seats -1)>=NUM_ROW_SEATS):
        print('failing base case')
        print('FAIL')
        return 1
    return 0

def book_seat(current_seats, row, seat_num, num_seats):
    #check base cases
    ret = check_base_cases(row, seat_num, num_seats)
    if ret==1:
        return
    

    all_seats = current_seats[str(row)][seat_num:seat_num+num_seats]
    print(all_seats)
    #check if the seats are available
    if set(all_seats)!= set([0]):
        print('FAIL')
        return

    #now set the seats as occupied
    current_seats[str(row)][seat_num:seat_num+num_seats] = [1] * num_seats
    store_seats(current_seats)

    print('SUCCESS')

def cancel_seat(current_seats, row, seat_num, num_seats):
    ret = check_base_cases(row, seat_num, num_seats)
    if ret==1:
        return

    all_seats = current_seats[str(row)][seat_num:seat_num+num_seats]
    print(all_seats)
    #check if seats are already booked
    if set(all_seats)!= set([1]):
        print('FAIL')
        return
    
    #now set the seats as empty
    current_seats[str(row)][seat_num:seat_num+num_seats] = [0] * num_seats
    store_seats(current_seats)

    print('SUCCESS')


if __name__=='__main__':
    #create argument parser
    parser = argparse.ArgumentParser(description="Options to reserve seats.")
    parser.add_argument('ACTION', choices=['BOOK', 'CANCEL'], action='store', help="Specify what action needs to be taken w.r.t. airline seat booking.")
    parser.add_argument('STARTING_SEAT_NUMBER', type=str, action='store', help="Mention the row at which to book the seat")
    parser.add_argument('NUM_OF_SEATS', type=int, action='store', help="Specify the number of consecutive seats to be booked.")

    #read the arguments
    args = parser.parse_args()
    #print(args.ACTION)

    #if not already done, create initial layout for json file where seats assigned data is stored
    if not os.path.isfile(SEATS_FILE):
        dump = {}
        for i in range(20):
            dump[i] = [0]*8

        store_seats(dump)

    
    #call the required function based on the argument
    current_seats = load_seats()
    row = ord(args.STARTING_SEAT_NUMBER[0])-ord(ROW_INDEX)
    seat_num = int(args.STARTING_SEAT_NUMBER[1:])
    num_seats = int(args.NUM_OF_SEATS)
    
    print(f"row: {row}, seat_num: {seat_num}, num seats: {num_seats}")
    
    if args.ACTION=='BOOK':
        book_seat(current_seats, row, seat_num, num_seats)
    elif args.ACTION=='CANCEL':
        cancel_seat(current_seats, row, seat_num, num_seats)

    
