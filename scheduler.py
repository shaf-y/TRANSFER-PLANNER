from course_data import COURSES

# The theoretically optimal sequence for De Anza to UCB ChemE in 1 year.
# Balances weeder classes with lower-difficulty GEs and fits into unit limits.
OPTIMAL_TEMPLATE = {
    "Summer": ["MATH 1A", "EWRT 1A", "CIS 22A"],
    "Fall": ["MATH 1B", "CHEM 12A", "PHYS 4A", "EWRT 2"],
    "Winter": ["MATH 1C", "CHEM 12B", "PHYS 4B", "CIS 22B"],
    "Spring": ["MATH 1D", "CHEM 12C", "PHYS 4C", "COMM 1"]
}

MAX_UNITS = {
    "Summer": 15.0,
    "Fall": 21.5,
    "Winter": 21.5,
    "Spring": 21.5
}

def generate_plan():
    plan = []
    
    for term, course_ids in OPTIMAL_TEMPLATE.items():
        quarter_data = {
            "term": term,
            "max_units": MAX_UNITS[term],
            "courses": [],
            "total_units": 0.0,
            "difficulty_score": 0
        }
        
        for cid in course_ids:
            if cid in COURSES:
                cinfo = COURSES[cid]
                quarter_data["courses"].append({
                    "id": cid,
                    "name": cinfo["name"],
                    "units": cinfo["units"],
                    "difficulty": cinfo["difficulty"]
                })
                quarter_data["total_units"] += cinfo["units"]
                quarter_data["difficulty_score"] += cinfo["difficulty"]
                
        plan.append(quarter_data)
        
    return plan
