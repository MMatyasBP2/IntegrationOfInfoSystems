# Integration Of Information Systems
Integration of Information Systems subject semester task.
The task is implemented and ran under Docker enviroment.

It is about creating a fictional prepaid mobile top-up application that will be a tcp based socket server on a specific port to receive client requests. The clients are atm machines that work according to the following protocol: 
1) the client sends a test message with the phone number to be recharged,
2) if the number is rechargeable, it sends an OK otherwise it aborts the transaction with an ERROR message. In case of an OK message, a transaction ID is received which identifies the process in the next step 3
3) the client initiates the actual top-up with the transaction ID received earlier, but the phone number and top-up amount must be resent.

The possible top-up amounts are 3000,5000,10000,15000 
A query client is also created that lists the previous transactions for a given phone number. Use a database to store transactions in the server application.

Main.py is working the way, that 3 clients that use a predefined set of phone numbers and randomly trigger test and upload transactions.
