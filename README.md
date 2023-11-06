# Airline_reservation
An airline company needs you to implement a system to help book seats on flights. This airline company has only one kind of plane with 20 rows, each row with a seat arrangement like so where ‘x’ represents a seat:
| xx _ xxxx _ xx |
Seats are identified using a letter to indicate the row and a number to represent the position in the row. The first row is identified as ‘A’ and the first seat in row A is ‘0’ and is thereby identified as ‘A0’. Payment information is handled by another team and system, so we only need to focus on the reservation of the seats themselves.

## Requirements
1. The state of reserved seats should be maintained in a file
2. A given seat cannot be reserved by more than one person
3. Once a person has a seat reservation they cannot be moved
4. If a customer cancels their reservation, the seat is available for reserving again
5. If a customer wants to reserve multiple seats together in the same row, we should be able to accommodate that or tell the customer it’s not possible
6. Must be able to run in a Linux environment
7. Input must be accepted from CLI arguments specifically
8. Input will be in the format of [Action] [Starting Seat] [Number of consecutive seats]
9. Output must go to STDOUT
10. Output must only be in the format of “SUCCESS” or “FAIL”
11. Any expected/unexpected errors should not go to STDOUT
12. This should not be an interactive terminal. It must be a command-line driven input.

## Usage
Run the app the following way:
    `./Solution.py BOOK|CANCEL ROW_NUM_SEAT_NUM NUM_OF_SEATS`
Examples:
    `./Solution.py BOOK A1 4`
    `./Solution.py CANCEL A2 1`

If you want to run pre-defined test-cases, do the following:
    sh tests.sh