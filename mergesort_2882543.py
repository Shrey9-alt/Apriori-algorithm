import sys

def print_laidout(left, right, depth):
    if depth == 0:
        # Combine both lists with no spacing
        laidout = " ".join(map(str, left + right))
    elif depth == 1:
        # Add spacing between the left and right sides
        laidout = f"{' '.join(map(str, left))}{' ' * 5}{' '.join(map(str, right))}"
    elif depth == 2:
        # Split each side into halves and format with the required spacings
        left_part1 = " ".join(map(str, left[:len(left) // 2]))
        left_part2 = " ".join(map(str, left[len(left) // 2:]))
        right_part1 = " ".join(map(str, right[:len(right) // 2]))
        right_part2 = " ".join(map(str, right[len(right) // 2:]))

        left_spacing = " " * 5
        right_spacing = " " * 9

        laidout = f"{left_part1}{left_spacing}{left_part2}{right_spacing}{right_part1}{left_spacing}{right_part2}"

    elif depth == 3:  
        spacing = " " * 5
        sub_spacing = " " * 9
        laidout = (
            spacing.join(map(str, left)) + sub_spacing + spacing.join(map(str, right))
        )
    if depth == 4:  
    
       merged_left = [sorted(duo) for duo in zip(left[::2], left[1::2])]
       merged_right = [sorted(duo) for duo in zip(right[::2], right[1::2])]

       left_part = " ".join(" ".join(map(str, duo)) for duo in merged_left[:1])  # First left duo
       left_part += " " * 5 + " ".join(" ".join(map(str, duo)) for duo in merged_left[1:])  # Second left duo
    
       right_part = " ".join(" ".join(map(str, duo)) for duo in merged_right[:1])  # First right duo
       right_part += " " * 5 + " ".join(" ".join(map(str, duo)) for duo in merged_right[1:])  # Second right duo

       laidout = left_part + " " * 9 + right_part

    elif depth == 5: 
        left_sorted = sorted(left)
        right_sorted = sorted(right)

        laidout = " ".join(map(str, left_sorted)) + " " * 5 + " ".join(map(str, right_sorted))

    print(laidout)
    print() 

if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        print("Command line usage: python3 mergesort_2882543.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

try:
    # Read numbers from the file
    with open(filename, 'r') as file:
        numbers = list(map(int, file.readline().strip().split()))

    # Split the list into left and right halves
    midpoint = len(numbers) // 2
    left, right = numbers[:midpoint], numbers[midpoint:]

    # Print the laid-out representation for each step
    for step in range(6):
        print_laidout(left, right, step)

    # Print the sorted numbers
    print(" ".join(map(str, sorted(numbers))))

except FileNotFoundError:
    # Handle missing file error
    print(f"Error: Could not open file '{filename}'. Please check if it exists.")
    sys.exit(1)
