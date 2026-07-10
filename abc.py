import csv
import io

def parse_user_data(csv_string, group_name):
    """
    Parses a CSV string with user data in the specified format and
    returns a list of dictionaries, where each dictionary represents a user.

    Args:
        csv_string (str): A string containing the CSV data.
        group_name (str): The name of the group to associate with the users.

    Returns:
        list: A list of dictionaries, where each dictionary has the keys
              'Name', 'email', and 'group'.  Returns an empty list if no
              user data is found.
    """
    user_data = []
    lines = csv_string.strip().splitlines()  # Split into lines and remove leading/trailing whitespace
    i = 0
    while i < len(lines):
        # Check if the line is empty or contains only whitespace
        if not lines[i].strip():
            i += 1
            continue

        # Extract data, handling potential issues with spacing
        try:
            name = lines[i+1].strip()
            email = lines[i+3].strip()
            user_data.append({
                'Name': name,
                'email': email,
                'group': group_name
            })
            i += 6  # Move to the next user entry
        except IndexError:
            # Handle the case where a user entry is incomplete.
            # Log the error and skip to the next expected entry.
            print(f"Incomplete user entry at line {i}. Skipping.")
            break

    return user_data

def format_user_data_for_csv(user_data):
    """
    Formats user data into a CSV string with the specified header.

    Args:
        user_data (list): A list of dictionaries, where each dictionary has the keys
                          'Name', 'email', and 'group'.

    Returns:
        str: A CSV string with the formatted user data, or an empty string
             if the input list is empty.
    """
    if not user_data:
        return ""

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=['Name', 'email', 'group'])
    writer.writeheader()
    writer.writerows(user_data)
    return output.getvalue()

def main(csv_string, group_name):
    """
    Parses user data from a CSV string and prints the formatted CSV output.

    Args:
        csv_string (str): A string containing the CSV data.
        group_name (str): The name of the group.
    """
    user_data = parse_user_data(csv_string, group_name)
    if user_data:
        formatted_csv = format_user_data_for_csv(user_data)
        print(formatted_csv)
    else:
        print("No user data found to process.")

if __name__ == "__main__":
    csv_string = """
AB
John Smith
User
john.smith@abc.com
Member
526d4d55-b3f8-48b8-a5b8-15f4b5c7af07


AP
Graham Brady
User
graham.brady@abc.com
Member
970fe1a0-cf9c-476a-bf11-2fc5ec40c78e


AP
Will Young
User
will.young@abc.com
Member
abd18536-8b3d-42ac-afdc-ca24c4526e05
"""
    group_name = "abc group"  # Example group name
    main(csv_string, group_name)
