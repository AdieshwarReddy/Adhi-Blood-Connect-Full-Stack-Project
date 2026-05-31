from typing import List, Set

# Full blood group compatibility matrix
# Key: Patient blood group
# Value: Set of compatible donor blood groups
COMPATIBILITY_MAP = {
    "O-": {"O-"},
    "O+": {"O-", "O+"},
    "A-": {"O-", "A-"},
    "A+": {"O-", "O+", "A-", "A+"},
    "B-": {"O-", "B-"},
    "B+": {"O-", "O+", "B-", "B+"},
    "AB-": {"O-", "A-", "B-", "AB-"},
    "AB+": {"O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"} # Universal Recipient
}

def is_compatible(donor_group: str, patient_group: str) -> bool:
    """
    Checks if a donor's blood type is compatible with a patient's blood type.
    """
    donor = donor_group.upper().strip()
    patient = patient_group.upper().strip()
    
    if patient not in COMPATIBILITY_MAP:
        return False
        
    return donor in COMPATIBILITY_MAP[patient]

def get_compatible_donors(patient_group: str) -> List[str]:
    """
    Retrieves all compatible donor blood types for a given patient blood type.
    """
    patient = patient_group.upper().strip()
    if patient not in COMPATIBILITY_MAP:
        return []
    return list(COMPATIBILITY_MAP[patient])
