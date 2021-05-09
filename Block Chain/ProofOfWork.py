import hashlib 

input_str = "pocas.kr"
counter = 0 
difficulty = 1 
for difficulty in range(1, 8):
    while hashlib.sha256(f"{input_str}{counter}".encode()).hexdigest()[:difficulty] != "0"*difficulty:
        counter+=1
    print(f"difficulty: {difficulty}, counter: {counter}")
    print(hashlib.sha256(f"{input_str}{counter}".encode()).hexdigest())
    print("="*20)