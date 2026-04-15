COURSES = {
    "MATH 1A": {"name": "Calculus I", "units": 5.0, "difficulty": 8, "prereqs": []},
    "MATH 1B": {"name": "Calculus II", "units": 5.0, "difficulty": 8, "prereqs": ["MATH 1A"]},
    "MATH 1C": {"name": "Calculus III", "units": 5.0, "difficulty": 8, "prereqs": ["MATH 1B"]},
    "MATH 1D": {"name": "Calculus IV", "units": 5.0, "difficulty": 8, "prereqs": ["MATH 1C"]},
    "PHYS 4A": {"name": "Physics for Scientists and Engineers", "units": 6.0, "difficulty": 9, "prereqs": ["MATH 1A"]},
    "PHYS 4B": {"name": "Physics for Scientists and Engineers", "units": 6.0, "difficulty": 9, "prereqs": ["PHYS 4A", "MATH 1B"]},
    "PHYS 4C": {"name": "Physics for Scientists and Engineers", "units": 6.0, "difficulty": 9, "prereqs": ["PHYS 4B", "MATH 1C"]},
    "CHEM 12A": {"name": "Organic Chemistry", "units": 5.0, "difficulty": 10, "prereqs": []},
    "CHEM 12B": {"name": "Organic Chemistry", "units": 5.0, "difficulty": 10, "prereqs": ["CHEM 12A"]},
    "CHEM 12C": {"name": "Organic Chemistry", "units": 5.0, "difficulty": 10, "prereqs": ["CHEM 12B"]},
    "EWRT 1A": {"name": "Composition and Reading", "units": 5.0, "difficulty": 4, "prereqs": []},
    "EWRT 2": {"name": "Critical Reading, Writing and Thinking", "units": 5.0, "difficulty": 5, "prereqs": ["EWRT 1A"]},
    "COMM 1": {"name": "Public Speaking", "units": 5.0, "difficulty": 3, "prereqs": []},
    "CIS 22A": {"name": "Beginning Programming Methodologies", "units": 4.5, "difficulty": 5, "prereqs": []},
    "CIS 22B": {"name": "Intermediate Programming Methodologies", "units": 4.5, "difficulty": 6, "prereqs": ["CIS 22A"]},
    "CIS 22C": {"name": "Data Abstraction and Structures", "units": 4.5, "difficulty": 7, "prereqs": ["CIS 22B"]},
}

TARGET_COURSES = [
    # Sequences
    "MATH 1A", "MATH 1B", "MATH 1C", "MATH 1D",
    "PHYS 4A", "PHYS 4B", "PHYS 4C",
    "CHEM 12A", "CHEM 12B", "CHEM 12C",
    # Golden Four
    "EWRT 1A", "EWRT 2", "COMM 1",
    # CS Additions (Low priority, to fill empty spots)
    "CIS 22A", "CIS 22B", "CIS 22C"
]
