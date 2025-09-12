"""
Have a look at the script called 'human-guess-a-number.py' (in the same folder as this one).

Your task is to invert it: You should think of a number between 1 and 100, and the computer 
should be programmed to keep guessing at it until it finds the number you are thinking of.

At every step, add comments reflecting the logic of what the particular line of code is (supposed 
to be) doing. 
"""

def input_check(prompt):
    """Asks the user to check: correct (correct), too high (high), too low (low)."""
    feedback = input(prompt).lower()
    while feedback not in ('correct', 'high', 'low'): 
        print("Please type 'correct' for correct, 'high' for too high, or 'low' for too low.")
        feedback = input(prompt).lower()
    return feedback

print("Think of a number between 1 and 100, and I will try to guess it!")

low = 1      
high = 100   
guesses = 0  

while True:
    guess = (low + high) // 2  
    guesses += 1
    print(f"My guess is {guess}.")  

    feedback = input_check("Is it correct, too high, or too low? ")

    if feedback == 'correct':  
        print(f"I found your number in {guesses} guesses!")
        break
    elif feedback == 'high': 
        high = guess - 1  
    else:                
        low = guess + 1   