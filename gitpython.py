import os
import requests
import logging
import json
import uuid
import smtplib
from email.mime.text import MIMEText

def trigger_build(repo_name, username, ref, environment, custom_data=None):
    url = f"https://api.github.com/repos/{username}/{repo_name}/dispatches"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "token YOUR_GITHUB_ACCESS_TOKEN"
    }
    payload = {
        "event_type": "build",
        "client_payload": {
            "ref": ref,
            "environment": environment
        }
    }

    if custom_data:
        payload["client_payload"].update(custom_data)

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 204:
        return True
    else:
        return False

def validate_input_params(repo_name, username, ref, environment):
    if not repo_name:
        raise Exception("Error: Required environment variable GITHUB_REPO_NAME is missing.")
    if not username:
        raise Exception("Error: Required environment variable GITHUB_USERNAME is missing.")
    if not ref:
        raise Exception("Error: Required environment variable GITHUB_BRANCH_NAME is missing.")
    if not environment:
        raise Exception("Error: Required environment variable ENVIRONMENT_NAME is missing.")

def setup_logger(log_file):
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def send_email_notification(to_email, subject, message):
    smtp_server = "SMTP_SERVER_ADDRESS"
    smtp_port = 587
    smtp_username = "SMTP_USERNAME"
    smtp_password = "SMTP_PASSWORD"

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = "FROM_EMAIL_ADDRESS"

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        logging.error(f"Failed to send mail: {e}")

def main(args):
    logging.info("Starting GitHub Dispatch action")
    logging.info(f"Input arguments: {args}")

    repo_name = os.getenv("GITHUB_REPO_NAME")
    username = os.getenv("GITHUB_USERNAME")
    ref = os.getenv("GITHUB_BRANCH_NAME")
    environment = os.getenv("ENVIRONMENT_NAME")
    is_send_email = os.getenv("SEND_EMAIL_NOTIFICATION")

    validate_input_params(repo_name, username, ref, environment)

    log_file = f"/github/home/logs/github_dispatch_{uuid.uuid4()}.log"
    setup_logger(log_file)

    logging.info(f"Triggering build for {username}/{repo_name}/{ref}/{environment}")
    trigger_build(repo_name, username, ref, environment, args)

    if is_send_email == "true":
        subject = f"GitHub Action: Build triggered for {username}/{repo_name}/{ref}/{environment}"
        message = f"GitHub Action: Build triggered for {username}/{repo_name}/{ref}/{environment}"
        send_email_notification(os.getenv("EMAIL_TO"), subject, message)

if __name__ == "__main__":
    main(json.loads(os.getenv("INPUT_CUSTOM_DATA")))