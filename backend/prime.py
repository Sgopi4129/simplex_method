#write a program to check whether a number is prime or not
import random
import threading

def get_input():
    global start, end
    start = input("Enter starting number:\t")
    end = input("Enter ending value:\t")
    return start, end
def prime(n):
    try:
        n = int(n)
    except (TypeError, ValueError):
        return False

    if n <= 1:
        
        return False

    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

    


if __name__ == "__main__":
    # start an input thread and allow 5 seconds for the user to respond
    thread = threading.Thread(target=get_input)
    # make the input thread a daemon so the program can exit if it times out
    thread.daemon = True
    thread.start()
    thread.join(5)
    if thread.is_alive():
        st = random.randint(1, 1000)
        en=random.randint(1,1000)
        print("\nTime is up!")
        print("Starting and ending numbers are:", st, en)
    else:
        try:
            st = int(start)
            en = int(end)
            print("Starting and ending values:", st, en)
        except (NameError, ValueError):
            print("Please enter a valid integer.")
            raise SystemExit(1)
    # if start and end are reversed, swap them
    if st > en:
        
        st, en = en, st
        print("Exchanging values",st,en)

    for i in range(st, en + 1):
        if prime(i):
            print(i, end=" ")
        else:
            pass
    print()
   