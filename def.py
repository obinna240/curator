import csv

def parse_user_csv2(input_file, output_file, group_name):
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip() != '']

    output_data = []
    entry_size = 6

    for i in range(0, len(lines), entry_size):
        chunk = lines[i:i + entry_size]
        if len(chunk) >= 4:
            name = chunk[1]
            email = chunk[3]
            output_data.append([name, email, group_name])

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Email', 'Group'])
        writer.writerows(output_data)

    print(f"Processed {len(output_data)} users into {output_file}")

def parse_user_csv(input_file, output_file, group_name):
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if not is_ignorable_line(line)]

    output_data = []
    entry_size = 6

    for i in range(0, len(lines), entry_size):
        chunk = lines[i:i + entry_size]
        if len(chunk) >= 4:
            name = chunk[1]
            email = chunk[3]
            output_data.append([name, email, group_name])

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Email', 'Group'])
        writer.writerows(output_data)

    print(f"Processed {len(output_data)} users into {output_file}")

UUID_PATTERN = re.compile(r'^[a-f0-9]{8}-[a-f0-9]{4}-[1-5][a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$', re.I)

def is_ignorable_line(line: str) -> bool:
    line = line.strip()
    return (
            not line or  # Empty/whitespace
            line in ("User", "Member") or
            len(line) == 2 or
            UUID_PATTERN.match(line)
    )

# Clean and filter the lines
lines = [line.strip() for line in lines if not is_ignorable_line(line)]
# Example usage:
parse_user_csv('input.csv', 'output.csv', 'abc group')
