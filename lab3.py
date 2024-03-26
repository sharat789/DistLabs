def read_input_file(input_file):
    calls = []
    with open(input_file, 'r') as file:
        for line in file:
            parts = line.strip().split()
            phone1, phone2, duration = parts[:3]
            calls.append((phone1, int(duration)))
            calls.append((phone2, int(duration)))
    return calls

def calculate_summary(calls):
    summary = {}
    for phone, duration in calls:
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

    summary = calculate_summary(calls)

    write_output_file(summary, output_file)

if __name__ == "__main__":
    main()
