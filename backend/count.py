# write python program to count the total number of vowels, consonants and blanks in a given string

def count_chars(text):
    vowels = set("aeiouAEIOU")
    vowel_count = 0
    consonant_count = 0
    blank_count = 0

    for ch in text:
        if ch.isspace():
            blank_count += 1
        elif ch.isalpha():
            if ch in vowels:
                vowel_count += 1
            else:
                consonant_count += 1

    return vowel_count, consonant_count, blank_count


if __name__ == "__main__":
    text = input("Enter a string: ")
    vowels, consonants, blanks = count_chars(text)
    print(f"Vowels: {vowels}")
    print(f"Consonants: {consonants}")
    print(f"Blanks: {blanks}")
    


