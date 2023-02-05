##Introduction
This final project is a RSA encryption and decryption system that enable users to send their secret messages.


##Login
All the users have to register their own account in order to use this program.

After registeration,a pair of public key and secret key will be assigned to the user automatically.

The username, password, public key, secret key will store in a SQL file called database.db

##Encryption
The user need to pick their message receiver first.

Then, the user can type the messages in the message box below.

After that, each letter in the messages will be converted to ASCii code and encrypt it.

The RSA encryption method is using the sender secret key, receiver public key, a product of prime number to do the modulus calculation.

the encrypted ascii code will be store in a csv file called message.csv

##Decryption
The message receiver have to login with their own account.

After login, the receiver need to pick the correct sender of the secret message.

Then, click the "decrypt" button,the program will read the csv file, decrypt the message and display the decrypted messages in the message box.

The RSA decryption method is using the sender public key, receiver secret key,the same prime number in encryption part in order to do the modulus calculation.

The correct decrypted messages will be displayed only if you are the correct message receiver and you know the correct message sender.

