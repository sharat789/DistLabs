from functools import reduce

def read_input_file(input_file):
    calls = []
    with open(input_file, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 4:
                phone1, phone2, duration, _ = parts[:4]
                calls.append((phone1, int(duration)))
                calls.append((phone2, int(duration)))
            else:
                print("Invalid input line:", line.strip())
    return calls

def reduce_operation(summary, call):
    phone, duration = call
    if phone in summary:
        summary[phone] += duration
    else:
        summary[phone] = duration
    return summary

def write_output_file(summary, output_file):
    with open(output_file, 'w') as file:
        for phone, duration in summary.items():
            file.write(f"{phone} {duration}\n")

def main():
    input_file = "calls.txt"  
    output_file = "summary.txt"  

    calls = read_input_file(input_file)

    summary = reduce(reduce_operation, calls, {})

    write_output_file(summary, output_file)

    print("Summary has been written to", output_file)

if __name__ == "__main__":
    main()
