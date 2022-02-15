import signal

class TimeoutException(Exception):   # Custom exception class
    pass

def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException
    
# Change the behavior of SIGALRM
signal.signal(signal.SIGALRM, timeout_handler)

def run():
    pass

def main():
    signal.alarm(60) # alarm if the following execution exceeds 60 seconds (actually will raise for every 60 seconds, thus a reset is required)
    try:
        run()
    except TimeoutException:
        # do something if timeout
        exit()
    else:
        # Reset the alarm
        signal.alarm(0)
