# java2S3 Amazon S3 Bucket Enumeration Tool

## Introduction

This Python script automates the enumaration of S3 Buckets referenced in a subdomain's javascript files. This allows the bug bounty hunter to check for security misconfigurations and pentest Amazon S3 Buckets. 

## Features

- Fetches HTTP status codes for subdomains
- Retrieves JavaScript URLs associated with each subdomain
- Identifies Amazon S3 buckets in the content

## Getting Started

### Prerequisites

- Python 3.x
- Install required libraries:

  ```bash
  pip install requests


## Usage

1. **Download the script:**
   - Clone the repository or download the script (`js2s3.py`).

2. **Prepare an input file:**
   - Create a text file (`input.txt`) containing a list of subdomains (one per line).

3. **Run the script from the command line:**
   - Open a terminal or command prompt.
   - Navigate to the directory where the script is located.

     ```bash
     cd path/to/script
     ```

   - Execute the script by providing the input file, base domain, and output file as arguments:

     ```bash
     python js2s3.py input.txt example.com output.txt
     ```

     Replace `example.com` with your base domain.

4. **Review the results:**
   - Open the output file (`output.txt`) to review the results.
