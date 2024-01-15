# java2s3.py
import requests
from urllib.parse import urljoin
import re

def get_html_content(url):
    try:
        response = requests.get(url, timeout=20, verify=True)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_js_urls(html_content, base_url):
    try:
        js_urls = re.findall(r"(?<=src=['\"])[a-zA-Z0-9_\.\-\:\/]+\.js", html_content.decode('utf-8', 'ignore'))
        return [urljoin(base_url, js_url) for js_url in js_urls]
    except Exception as e:
        print(f"Error extracting JavaScript URLs: {e}")
        return []

def extract_s3_buckets(content):
    try:
        regs3 = r"[\w\-\.]+\.s3\.?(?:[\w\-\.]+)?\.amazonaws\.com|(?<!\.)s3\.?(?:[\w\-\.]+)?\.amazonaws\.com\\?\/[\w\-\.]+"
        s3_buckets = re.findall(regs3, content.decode('utf-8', 'ignore'))
        return s3_buckets
    except Exception as e:
        print(f"Error extracting S3 Buckets: {e}")
        return []

def analyze_subdomain(subdomain, base_domain, output_file):
    with open(output_file, "a") as output:
        output.write(f"\nAnalyzing subdomain: {subdomain}\n")

        url_http = f"http://{subdomain}"
        url_https = f"https://{subdomain}"

        for url in [url_http, url_https]:
            try:
                subdomain_without_protocol = subdomain.replace("http://", "").replace("https://", "")
                full_url = url if base_domain in subdomain else f"{url}/{subdomain_without_protocol}"

                output.write(f"\nChecking - {full_url}\n")

                response = requests.get(full_url, timeout=20, verify=True)
                output.write(f"HTTP Status Code: {response.status_code}\n")

                html_content = response.content
                output.write(f"HTML Content: {html_content}\n")

                js_urls = extract_js_urls(html_content, full_url)
                output.write(f"JavaScript URLs: {js_urls}\n")

                s3_buckets = extract_s3_buckets(html_content)
                output.write(f"S3 Buckets: {s3_buckets}\n")

                if s3_buckets:
                    print(f"\nAlert: S3 Bucket(s) found for subdomain {subdomain}! {s3_buckets}\n")

            except requests.exceptions.RequestException as e:
                output.write(f"Error analyzing subdomain {subdomain}: {e}\n")
                continue

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("Usage: python java2s3.py input_file base_domain output_file")
        sys.exit(1)

    input_filename = sys.argv[1]
    base_domain = sys.argv[2]
    output_filename = sys.argv[3]

    with open(output_filename, "w") as output:
        output.write("Results:\n")

    with open(input_filename, "r") as domains_file:
        for domain in domains_file:
            analyze_subdomain(domain.strip(), base_domain, output_filename)

    print(f"Results written to {output_filename}")
