# GitHub-Build-Trigger-Code-UOttaHack5

# Description: 

Trigger for building for a repository on a specific Git branch and environment

# GitHub Dispatch Action:  

This is a GitHub action that can be used to trigger a build for a repository on a specific branch and environment. The build can also include custom data that can be passed as an input argument to the action.

# Requirements: 

GitHub repository with the code for which the build needs to be triggered.
A GitHub access token with the appropriate permissions to trigger a dispatch event for the repository.
The environment variables GITHUB_REPO_NAME, GITHUB_USERNAME, GITHUB_BRANCH_NAME, and ENVIRONMENT_NAME must be set in the action's environment.

# Usage: 
The action can be triggered by adding it to a workflow in the .github/workflows directory in your repository. Here is an example of a workflow that triggers the build for a repository: 

# yaml code: 

name: Trigger Build

on:
  push:
    branches:
      - main

env:
  GITHUB_REPO_NAME: ${{ env.GITHUB_REPOSITORY }}
  GITHUB_USERNAME: ${{ env.GITHUB_ACTOR }}
  GITHUB_BRANCH_NAME: ${{ env.GITHUB_REF }}
  ENVIRONMENT_NAME: production
  SEND_EMAIL_NOTIFICATION: true
  EMAIL_TO: your-email@example.com

jobs:
  trigger_build:
    runs-on: ubuntu-latest

    steps:
    - name: Trigger Build
      uses: ./.github/actions/trigger_build
      env:
        INPUT_CUSTOM_DATA: '{"custom_field_1": "value_1", "custom_field_2": "value_2"}'

In the example above, the action is triggered when the main branch is pushed. The environment variables GITHUB_REPO_NAME, GITHUB_USERNAME, GITHUB_BRANCH_NAME, and ENVIRONMENT_NAME are set to the appropriate values. The INPUT_CUSTOM_DATA variable can be set to include any custom data that needs to be passed to the build. The SEND_EMAIL_NOTIFICATION variable can be set to true if an email notification needs to be sent when the build is triggered.

# Configuration: 

SMTP_SERVER_ADDRESS, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, and FROM_EMAIL_ADDRESS: These variables must be set if email notifications need to be sent. They correspond to the SMTP server address, port, username, password, and from email address, respectively.
YOUR_GITHUB_ACCESS_TOKEN: This variable must be set to your GitHub access token.

# Logging in the Application: 

The action logs information to a file in the /github/home/logs directory. The log file name is of the format github_dispatch_{UUID}.log, where {UUID} is a unique identifier generated for each run of the action. The log file contains information about the input arguments and any error messages that might occur during the execution of the action.


