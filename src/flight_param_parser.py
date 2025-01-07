# Define file paths
input_file_path = './evo_fligh_params.txt'      # Replace with your input file path
output_file_path = './parsed_params.txt'   # Replace with your desired output file path

# Function to parse PX4 parameters
def parse_px4_params(input_file, output_file):
    # Open and read the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Parse each line to desired format
    parsed_lines = []

    for line in lines:
        # Skip comment lines or empty lines
        if line.startswith("#") or not line.strip():
            continue

        # Split each line into its components
        parts = line.split()
        
        # Extract the name and value
        param_name = parts[2]   # Name of the parameter
        param_value = parts[3]  # Value of the parameter
        
        # Format to the desired output
        parsed_line = f"param set {param_name} {param_value}"
        parsed_lines.append(parsed_line)

    # Save the parsed output to a new file
    with open(output_file, 'w') as file:
        for parsed_line in parsed_lines:
            file.write(parsed_line + '\n')

    print(f"Parsed parameters saved to {output_file}")

# Call the function with specified input and output paths
parse_px4_params(input_file_path, output_file_path)
