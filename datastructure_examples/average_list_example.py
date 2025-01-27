all_numbers = []
one_input = ''
while True:
    one_input = input('Enter a number, type "done" when you are done.: ')
    if one_input == 'done':
        break
    try:
       number = int(one_input)
    except ValueError:
        print(f'Invalid input {one_input}')
        continue
    all_numbers.append(number)
    print(f"all numbers: {all_numbers}")

average = sum(all_numbers) / len(all_numbers)
print(f'Average: {average}')
