from common_imports import *

def calculate_ai_score(trainset):
    """ Calculate an AI score for a trainset based on multiple factors.
    Returns: (score: int, reasons: list of str) """
    score = 100
    reasons = []
    # Fitness
    if not trainset['fitness']['overall_valid']:
        score -= 30
        reasons.append("Invalid fitness certificate")
    # Job cards (open maintenance issues reduce score)
    open_jobs = trainset['job_cards']['open']
    if open_jobs > 0:
        penalty = min(20, open_jobs * 5)
        score -= penalty
        reasons.append(f"{open_jobs} open job cards")
    # Mileage & wear
    wear_avg = sum(trainset['mileage']['component_wear'].values()) / 3
    if wear_avg > 70:
        score -= 20
        reasons.append("High component wear")
    # Cleaning
    if trainset['cleaning']['interior_status'] != "Clean" or trainset['cleaning']['exterior_status'] != "Clean":
        score -= 10
        reasons.append("Requires cleaning")
    # Operational reliability
    reliability = trainset['operational']['reliability_score']
    score += (reliability - 70) // 2  # add some positive impact
    reasons.append(f"Reliability score {reliability}")
    # Branding
    if trainset['branding']['exposure_deficit'] > 10:
        score -= 10
        reasons.append("Branding exposure deficit")
    # Clamp between 0–100
    score = max(0, min(100, score))
    return score, reasons
# Enhanced Data Generation & Simulation
# Enhanced Data Simulation