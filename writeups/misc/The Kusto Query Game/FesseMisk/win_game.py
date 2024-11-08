import random

def load_event_ids_from_file(file_path):
    # Read the text file and load event IDs
    with open(file_path, 'r') as file:
        # Convert lines to a list of integers
        event_ids = [int(line.strip().strip(',')) for line in file if line.strip()]
    return event_ids

def generate_kql_query(event_ids, num_ids):
    # Ensure the number of IDs doesn't exceed available IDs
    num_ids = min(num_ids, len(event_ids))
    selected_ids = random.sample(event_ids, num_ids)  # Randomly select the specified number of IDs

    # Generate the KQL query with the selected Event IDs
    kql_query = f"StormEvents\n | where EventId in ({', '.join(map(str, selected_ids))})"
    return kql_query

# Example usage
file_path = "event_ids.txt"  # Path to the text file containing Event IDs
num_ids = int(input("Enter the number of Event IDs to use: "))

event_ids = load_event_ids_from_file(file_path)
kql_query = generate_kql_query(event_ids, num_ids)
print("Generated KQL Query:")
print(kql_query)
