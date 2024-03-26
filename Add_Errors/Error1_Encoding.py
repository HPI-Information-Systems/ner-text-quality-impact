
# Path to the text file
input_file_path = 'filepath/filename_org.txt'
# Path to save new file
output_file_path = 'filepath/filename_modifies.txt' 

# Steps to produce encoding errors in the text file
# 1. Read file with 'latin-1' encoding
# 2. Write the file with 'utf-8' encoding

try:
    with open(input_file_path, encoding='latin-1') as input_file:
        sample_text_default = input_file.read()
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(sample_text_default)

except FileNotFoundError:
    print(f'Error: The input file "{input_file_path}" does not exist.')

except Exception as e:
    print(f'An error occurred: {str(e)}')
