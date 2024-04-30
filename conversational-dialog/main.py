# main.py

import os
import random
import json
from interviewer import Interviewer
from summary import summarize_interview
from datetime import datetime

def list_available_jobs(jobs_folder):
    """List all job directories in the specified folder."""
    return [name for name in os.listdir(jobs_folder) if os.path.isdir(os.path.join(jobs_folder, name))]


def get_job_files(job_folder):
    persona_files = [f for f in os.listdir(job_folder) if f.endswith('.txt') and not f.endswith('~guidelines.txt')]
    criteria_files = [f for f in os.listdir(job_folder) if f.endswith('guidelines.txt')]
    return persona_files, criteria_files

def main():
    jobs_folder = "/Users/jibs/Documents/Projects /Idera and Interviews/interview-pilot-ai/persona-generation/personas/jobs"
    available_jobs = list_available_jobs(jobs_folder)
    if not available_jobs:
        print("No available jobs found in the directory.")
        return

    job_name = input(f"Enter the job you are interviewing for (available jobs: {', '.join(available_jobs)}): ")
    job_folder = os.path.join(jobs_folder, job_name)

    if not os.path.exists(job_folder):
        print(f"Job folder '{job_name}' does not exist.")
        return

    persona_files, criteria_files = get_job_files(job_folder)

    if not persona_files or not criteria_files:
        print(f"No persona or criteria files found for job '{job_name}'.")
        return

    persona_file = random.choice(persona_files)
    criteria_file = random.choice(criteria_files)

    with open(os.path.join(job_folder, persona_file), 'r') as file:
        persona = file.read()

    with open(os.path.join(job_folder, criteria_file), 'r') as file:
        criteria = file.read()

    interviewer = Interviewer(persona)
    interviewer.main()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    history_filename = f"{job_name}_{timestamp}_history.json"
    with open(history_filename, 'w') as file:
        json.dump(interviewer.history, file, indent=4)

    # New code to save the history as a text file
    history_text_filename = f"{job_name}_{timestamp}_history.txt"
    with open(history_text_filename, 'w') as file:
        for entry in interviewer.history:
            file.write(f"{entry['question']} - {entry['answer']}\n")

    summary = summarize_interview(interviewer.history, criteria)
    print(summary)

    # New code to save the summary as a text file
    summary_filename = f"{job_name}_{timestamp}_summary.txt"
    with open(summary_filename, 'w') as file:
        file.write(summary)

if __name__ == '__main__':
    main()
