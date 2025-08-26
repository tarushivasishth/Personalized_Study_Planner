import heapq

class Task:
    def __init__(self, subject, deadline, difficulty, predicted_time, previous_score=None):
        self.subject = subject
        self.deadline = deadline
        self.difficulty = difficulty 
        self.predicted_time = predicted_time 
        self.previous_score = previous_score

    def __lt__(self, other):
        # Priority order:
        # 1. Earlier deadline first
        # 2. If same deadline → weaker score first
        # 3. If same score → higher difficulty first
        if self.deadline == other.deadline:
            if (self.previous_score is not None) and (other.previous_score is not None):
                if self.previous_score != other.previous_score:
                    return self.previous_score < other.previous_score  
            return self.difficulty > other.difficulty
        return self.deadline < other.deadline


def round_half(x):
    """Round to nearest 0.5 hours (at least 0.5 if > 0)."""
    if x <= 0:
        return 0
    return max(0.5, round(x * 2) / 2)


def schedule_tasks(tasks, hours_per_day=8):
    heap = []
    for t in tasks:
        heapq.heappush(heap, t)

    schedule = {}
    day = 1

    while heap:
        remaining = hours_per_day
        today_tasks = []

        while heap and remaining > 0:
            task = heapq.heappop(heap)

            # Remaining possible study capacity for this task
            max_capacity = max(1, task.deadline) * hours_per_day  # avoid zero-div errors

            if task.predicted_time > max_capacity:
                # Overload → spread evenly across remaining days
                hrs_per_day = task.predicted_time / max(1, task.deadline)
                hrs = round_half(min(20, hrs_per_day))
            else:
                # Normal → allocate within today’s remaining hours
                hrs = round_half(min(task.predicted_time, remaining))

            # Safety: skip zero-hour allocations
            if hrs <= 0:
                continue

            today_tasks.append((task.subject, hrs))
            task.predicted_time -= hrs
            remaining -= hrs
            task.deadline -= 1  # one day consumed

            # Push back if unfinished and still has deadline left
            if task.predicted_time > 0 and task.deadline > 0:
                heapq.heappush(heap, task)

        if today_tasks:  # Only store non-empty days
            schedule[f"Day {day}"] = today_tasks
            day += 1
        else:
            break  # nothing scheduled, stop infinite loop

    return schedule


# Example test
tasks = [
    Task("Math", 2, 5, 12, previous_score=35),   # overload
    Task("Physics", 1, 4, 5, previous_score=85),
    Task("Chemistry", 3, 3, 2),
    Task("CS", 2, 2, 10, previous_score=95),     # tight but normal
]

plan = schedule_tasks(tasks, hours_per_day=6)
for day, t in plan.items():
    print(day, ":", t)