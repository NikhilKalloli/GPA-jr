import re
import json

text = """
CS31, CS, Linear Algebra and Laplace  Transforms  Mathematics  BSC  2 1 0 3 4 
2 CS32  Digital Design and Computer Organization  CSE IPCC  3 0 1 4 5 
3 CS33  Data Structures  CSE PCC  3 0 0 3 3 
4 CS34  Object Oriented Programming  CSE PCC  3 0 0 3 3 
5 CS35  Discrete Mathematical Structures  CSE PCC  2 1 0 3 4 
6 CSL36  Data Structures Laboratory  CSE PCC  0 0 1 1 2 
7 CSL37  Object Oriented Programming Laboratory  CSE PCC  0 0 1 1 2 
8 UHV38  Universal Human Values  CSE UHV  2 0 0, 9
CS41, CS, Numerical Techniques and Probability  Models  Mathematics  BSC  2 1 0 3 4 
2 CS42  Microcontrollers and IoT  CSE IPCC  3 0 1 4 5 
3 CS43  Design and Analysis of Algorithms  CSE PCC  3 0 0 3 3 
4 CS44  Data Communication and Networking  CSE PCC  3 0 0 3 3 
5 CS45  Finite Automata and Formal Languages  CSE PCC  2 1 0 3 4 
6 CSL46  Design and Analysis of Algorithms Laboratory  CSE PCC  0 0 1 1 2 
7 CSL47  Data Communication and Networking Laboratory  CSE PCC  0 0 1 1 2 
8 CSL48  Data visualization with python Lab  CSE PCC  0 0 1, 9

"""

pattern = r"(CS\d{2})\w*,\s*(\w+),\s*([\w\s,]+)\s+\w+\s+\w+\s+(\d+)\s+(\d+)\s+(\d+)\s*(?:\d+)?"

subject_info = []

# Split text into lines
lines = text.strip().split('\n')

# Process each line individually
for line in lines:
    # Perform regex matching on the current line
    match = re.match(pattern, line)
    if match:
        subject_code, leading_letters, subject_name, credit1, credit2, credit3 = match.groups()
        total_credits = int(credit1) + int(credit2) + int(credit3)
        subject_info.append({
            "subject_code": subject_code,
            "leading_letters": leading_letters,
            "subject_name": subject_name.strip(),
            "total_credits": total_credits
        })

# Save subject information to JSON file
with open("sub_info.json", "w") as file:
    json.dump(subject_info, file, indent=4)

print("Subject information has been saved to sub_info.json")
