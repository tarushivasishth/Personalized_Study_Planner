import pandas as pd
import numpy as np
import random

def generate_dataset(n_samples=500, random_state=42):
    random.seed(random_state)

    subjects_list = ["CS", "Maths", "Physics", "Chemistry", "Biology", "History", "Geography", "English"]
    difficulty_levels = ["Easy", "Medium", "Hard"]

    data = {}
    SUBJECTS = []
    DEADLINES = []
    DIFFICULTIES = []
    SCORES = []
    TIME = []

    for i in range(n_samples):
        subject = random.choice(subjects_list)
        deadline = random.randint(1, 14)
        difficulty = random.choice(difficulty_levels)
        previous_score = random.randint(0, 100)

        # Harder difficulty + low previous_score -> More time required
        base_time = {
           "Easy": random.randint(3, 6),
           "Medium": random.randint(6, 9),
           "Hard": random.randint(9, 12)
        }[difficulty]

        # adjust time based on score as well
        time_adjusted = base_time
        if previous_score < 40:
            time_adjusted *= 2.0   # much higher boost
        elif previous_score < 70:
            time_adjusted *= 1.5
        elif previous_score < 90:
            time_adjusted *= 1.0
        else:
            time_adjusted *= 0.6



        # adjust time based on deadline
        if deadline <= 3:
            time_adjusted += 1

        predicted_time = max(1, int(time_adjusted))

        SUBJECTS.append(subject)
        DEADLINES.append(deadline)
        DIFFICULTIES.append(difficulty)
        SCORES.append(previous_score)
        TIME.append(predicted_time)

    data["subject"] = SUBJECTS
    data["deadline"] = DEADLINES
    data["difficulty"] = DIFFICULTIES
    data["previous_score"] = SCORES
    data["time"] = TIME

    df = pd.DataFrame(data)
    df.to_csv("study_time_data.csv", index=False)

generate_dataset(1000)




        


