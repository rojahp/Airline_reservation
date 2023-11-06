#!/usr/bin/python3
import argparse
import json
import os
import sys
import logging

#defining globals
NUM_ROW_SEATS = 8
NUM_ROWS = 20
START_INDEX = 0
ROW_INDEX = 'A'
SEATS_FILE = 'airline_reservation.json'
logging.basicConfig(filename='airline.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)


#Create custom argument parser to avoid printing errors on stdout
class MyArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(MyArgumentParser, self).__init__(*args, **kwargs)

    def error(self, message):
        logging.error(message)
        print('FAIL')
        sys.exit(1)


def load_seats():
    """Returns seats information fetched from SEATS_FILE
    """
    with open(SEATS_FILE, 'r') as f:
        return json.load(f)


def store_seats(data):
    """Stores seats information into SEATS_FILE

    Args:
        data (dict): Dictionary object containing seats information
    """
    with open(SEATS_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def check_base_cases(row, seat_num, num_seats):
    """Return 0 or 1 after checking if the input provided for booking/canceling a seat is valid.

    Args:
        row (int): This is the row number to be assigned a seat to. Row is originally a character, but is converted to an integer based on it's ascii value.
        seat_num (int): The value of seat number between 0 and 7 to be booked or cancelled.
        num_seats (int): The number of consecutive seats to be booked or cancelled.
    """
    if (row < START_INDEX or row >= NUM_ROWS) or (seat_num <0 or seat_num >=NUM_ROW_SEATS) or (num_seats<1 or (seat_num + num_seats -1)>=NUM_ROW_SEATS):
        print('FAIL')
        return 1
    return 0


def book_seat(current_seats, row, seat_num, num_seats):
    """Book the required seats if possible

    Args:
        current_seats (dict): Information on current seats in dictionary format.
        row (int): This is the row number to be assigned a seat to. Row is originally a character, but is converted to an integer based on it's ascii value.
        seat_num (int): The value of seat number between 0 and 7 to be booked or cancelled.
        num_seats (int): The number of consecutive seats to be booked or cancelled.
    """
    #check base cases
    ret = check_base_cases(row, seat_num, num_seats)
    if ret==1:
        return
    
    all_seats = current_seats[str(row)][seat_num:seat_num+num_seats]
    #check if the seats are available
    if set(all_seats)!= set([0]):
        print('FAIL')
        return

    #now set the seats as occupied
    current_seats[str(row)][seat_num:seat_num+num_seats] = [1] * num_seats
    store_seats(current_seats)

    print('SUCCESS')


def cancel_seat(current_seats, row, seat_num, num_seats):
    """Cancel required seats if possible

    Args:
        current_seats (dict): Information on current seats in dictionary format.
        row (int): This is the row number to be assigned a seat to. Row is originally a character, but is converted to an integer based on it's ascii value.
        seat_num (int): The value of seat number between 0 and 7 to be booked or cancelled.
        num_seats (int): The number of consecutive seats to be booked or cancelled.
    """
    ret = check_base_cases(row, seat_num, num_seats)
    if ret==1:
        return

    all_seats = current_seats[str(row)][seat_num:seat_num+num_seats]
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
    parser = MyArgumentParser()
    parser.add_argument('ACTION', choices=['BOOK', 'CANCEL'], action='store', help="Specify what action needs to be taken w.r.t. airline seat booking.")
    parser.add_argument('STARTING_SEAT_NUMBER', type=str, action='store', help="Mention the row at which to book the seat")
    parser.add_argument('NUM_OF_SEATS', type=int, action='store', help="Specify the number of consecutive seats to be booked.")

    #read the arguments
    args = parser.parse_args()

    #if not already done, create initial layout for json file where seats assigned data is stored
    try:
        if not os.path.isfile(SEATS_FILE):
            dump = {}
            for i in range(20):
                dump[i] = [0]*8

            store_seats(dump)
    except Exception as e:
        logging.error(f"Exception occurred while trying to check for or initialize airline storage file: {e}")
        print('FAIL')
        sys.exit(1)

    
    #call the required function based on the argument
    try:
        current_seats = load_seats()
        if len(args.STARTING_SEAT_NUMBER)!=2:
            print('FAIL')
            sys.exit()
        row = ord(args.STARTING_SEAT_NUMBER[0])-ord(ROW_INDEX)
        seat_num = int(args.STARTING_SEAT_NUMBER[1:])
        num_seats = int(args.NUM_OF_SEATS)
    except Exception as e:
        logging.error(f"Error occurred while reading arguments: {e}")
        print('FAIL')
        sys.exit(1)
            
    try:
        if args.ACTION=='BOOK':
            book_seat(current_seats, row, seat_num, num_seats)
        elif args.ACTION=='CANCEL':
            cancel_seat(current_seats, row, seat_num, num_seats)
    except Exception as e:
        logging.error(f"Error occuerred while doing action {args.ACTION}: {e}")
        print('FAIL')
        sys.exit(1)

    
