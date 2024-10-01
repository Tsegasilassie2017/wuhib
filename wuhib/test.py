
GUIDELINES_FILE_PATH = 'C:/Users/hp/Desktop/wuhib/guidelines/tsega new 2017 BSC.docx'

try:
    with open(GUIDELINES_FILE_PATH, 'rb') as file:
        print("File opened successfully.")
except FileNotFoundError:
    print("File not found.")
except Exception as e:
    print(f"Error opening file: {e}")