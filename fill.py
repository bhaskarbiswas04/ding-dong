import os
import random
from datetime import datetime, timedelta

# --- CONFIGURATION ---
# Phase 1: Last 2 Years up until 4 months ago (Months 5 to 24)
P1_DENSITY = 0.20          # 20% chance of committing on any given day (sporadic)
P1_MIN_COMMITS = 1
P1_MAX_COMMITS = 2

# Phase 2: The most recent 4 months (Months 1 to 4)
P2_DENSITY = 0.70          # 70% chance of committing on any given day (moderate/consistent)
P2_MIN_COMMITS = 1
P2_MAX_COMMITS = 4
# ---------------------

def run_git_command(command):
    os.system(command)

def main():
    if not os.path.exists(".git"):
        run_git_command("git init")
        print("Initialized empty Git repository locally.")

    filename = "activity.txt"
    end_date = datetime.now()
    
    # Calculate timeline boundaries
    start_date = end_date - timedelta(days=2 * 365)        # 2 years ago
    phase_boundary = end_date - timedelta(days=4 * 30)     # 4 months ago

    print(f"Generating historic timeline...")
    print(f"Phase 1 (Sporadic): {start_date.strftime('%Y-%m-%d')} to {phase_boundary.strftime('%Y-%m-%d')}")
    print(f"Phase 2 (Moderate): {phase_boundary.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}\n")

    current_date = start_date
    total_commits = 0

    while current_date <= end_date:
        # Determine which phase rules apply to the current date
        if current_date < phase_boundary:
            density = P1_DENSITY
            min_commits = P1_MIN_COMMITS
            max_commits = P1_MAX_COMMITS
        else:
            density = P2_DENSITY
            min_commits = P2_MIN_COMMITS
            max_commits = P2_MAX_COMMITS

        # Evaluate if this day gets activity
        if random.random() < density:
            # Optional: Make it look like a regular job by skipping 80% of weekends
            if current_date.weekday() >= 5 and random.random() < 0.80:
                current_date += timedelta(days=1)
                continue

            commits_today = random.randint(min_commits, max_commits)
            
            for i in range(commits_today):
                # Add random hour/minute so commits don't all look like they happened at midnight
                hour = random.randint(9, 18)  # 9 AM to 6 PM
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                commit_time = current_date.replace(hour=hour, minute=minute, second=second)
                
                git_date = commit_time.strftime("%Y-%m-%d %H:%M:%S")
                
                with open(filename, "a") as f:
                    f.write(f"Contribution update on {git_date}\n")
                
                run_git_command(f'git add {filename}')
                
                # Set environment variables for precise timestamping
                os.environ["GIT_AUTHOR_DATE"] = git_date
                os.environ["GIT_COMMITTER_DATE"] = git_date
                
                # Commit with a varied generic message
                msg = random.choice(["Fix typos", "Refactor module", "Update documentation", "Clean up codebase", "Patch minor bugs"])
                run_git_command(f'git commit -m "{msg}" --date="{git_date}"')
                total_commits += 1

        current_date += timedelta(days=1)

    print(f"\nSuccessfully generated {total_commits} natural commits locally!")
    print("Now push your changes using: git push -u origin main")

if __name__ == "__main__":
    main()
