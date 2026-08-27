def string(items: str):
    vowels = ""
    consonants = ""
    digits = ""
    vowel_set = "aeiouAEIOU"
    
    for ch in items:
        if ch.isalpha():
            if ch in vowel_set:
                vowels += ch
            else:
                consonants += ch
        elif ch.isdigit():
            digits += ch
    
    return {
        "Vowels": vowels,
        "Consonants": consonants,
        "Digits": digits
    }




def main():
    items = input("Enter a string:\t")
    result = string(items)
    print(f"Vowels: {result['Vowels']}")
    print(f"Consonants: {result['Consonants']}")
    print(f"Digits: {result['Digits']}")

if __name__ == "__main__":
    main()