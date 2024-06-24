import os
import subprocess

results = []

def add_result(id, compliance, reason=""):
    results.append({"id": id, "compliance": compliance, "reason": reason})

def check_security_ldap_stanza(config_file_path):
    try:
        with open(config_file_path, 'r') as file:
            config_content = file.read()

        if 'security {' in config_content:
            if 'ldap {' in config_content:
                add_result("AD02", "PASS")
            else:
                add_result("AD02", "FAIL", "LDAP is not configured.")
        else:
            add_result("AD02", "FAIL", "Security stanza NOT found.")

    except FileNotFoundError:
        add_result("AD02", "FAIL", f"Configuration file not found: {config_file_path}")
    except Exception as e:
        add_result("AD02", "FAIL", f"An error occurred: {e}")

def check_xdr_stanza(config_file_path):
    try:
        with open(config_file_path, 'r') as file:
            config_content = file.read()

        if 'xdr {' in config_content:
            add_result("AD06", "PASS")
        else:
            add_result("AD06", "FAIL", "XDR is not configured.")

    except FileNotFoundError:
        add_result("AD06", "FAIL", f"Configuration file not found: {config_file_path}")
    except Exception as e:
        add_result("AD06", "FAIL", f"An error occurred: {e}")

def check_encryption_at_rest(config_file_path):
    try:
        with open(config_file_path, 'r') as file:
            config_content = file.read()

        if 'storage-engine device {' in config_content:
            add_result("AD03", "PASS")
        else:
            add_result("AD03", "FAIL", "Encryption at rest is NOT configured.")

    except FileNotFoundError:
        add_result("AD03", "FAIL", f"Configuration file not found: {config_file_path}")
    except Exception as e:
        add_result("AD03", "FAIL", f"An error occurred: {e}")

def check_key_dat_encryption(config_file_path):
    try:
        with open(config_file_path, 'r') as file:
            config_content = file.read()

        storage_engine_blocks = config_content.split('storage-engine device {')

        found_encryption = False

        for block in storage_engine_blocks[1:]:
            if 'encryption aes-' in block:
                found_encryption = True
                break

        if found_encryption:
            add_result("AD04", "PASS")
        else:
            add_result("AD04", "FAIL", "Encryption aes- NOT found inside storage-engine device { } stanza.")

    except FileNotFoundError:
        add_result("AD04", "FAIL", f"Configuration file not found: {config_file_path}")
    except Exception as e:
        add_result("AD04", "FAIL", f"An error occurred: {e}")

def check_tls_configuration(config_file_path):
    try:
        with open(config_file_path, 'r') as file:
            lines = file.readlines()

        service_stanza = False
        tls_stanza = False
        tls_enabled = False

        for i, line in enumerate(lines):
            if 'service {' in line:
                service_stanza = True
                if i + 1 < len(lines) and 'tls {' in lines[i + 1]:
                    tls_stanza = True
                    for j in range(i + 1, len(lines)):
                        if 'enabled true' in lines[j]:
                            tls_enabled = True
                            break
                break

        if service_stanza:
            if tls_stanza:
                if tls_enabled:
                    add_result("AD09", "PASS")
                else:
                    add_result("AD09", "FAIL", "TLS is NOT enabled.")
            else:
                add_result("AD09", "FAIL", "TLS sub-stanza NOT found after service stanza.")
        else:
            add_result("AD09", "FAIL", "Service stanza NOT found.")

    except FileNotFoundError:
        add_result("AD09", "FAIL", f"Configuration file not found: {config_file_path}")
    except Exception as e:
        add_result("AD09", "FAIL", f"An error occurred: {e}")

def check_backup_in_crontab():
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True, check=True)
        crontab_content = result.stdout

        if 'as_incremental_backup.sh' in crontab_content and 'as_full_backup.sh' in crontab_content:
            add_result("AD16", "PASS")
        else:
            add_result("AD16", "FAIL", "Backup scripts are NOT configured in crontab.")

    except subprocess.CalledProcessError:
        add_result("AD16", "FAIL", "Error retrieving crontab entries.")
    except FileNotFoundError:
        add_result("AD16", "FAIL", "Error: crontab command not found. Ensure cron is installed and in the system PATH.")
    except Exception as e:
        add_result("AD16", "FAIL", f"An error occurred while checking crontab entries: {e}")

def check_log_files_presence():
    paths = [
        "/data/aerospike/log/audit/",
        "/data/log/aerospike/audit/",
        "/data/aerospike/audit/"
    ]

    log_files_found = False

    for path in paths:
        if os.path.exists(path):
            log_files = os.listdir(path)
            if log_files:
                log_files_found = True
                break

    if log_files_found:
        add_result("AD16", "PASS")
    else:
        add_result("AD16", "FAIL", "No log files found in any of the specified paths.")

def check_file_log_sink(config_file_path):
    try:
        with open(config_file_path, 'r') as file:
            lines = file.readlines()

        logging_stanza = False
        file_log_sink = False

        for i, line in enumerate(lines):
            if 'logging {' in line:
                logging_stanza = True
                for j in range(i + 1, len(lines)):
                    if '}' in lines[j]:
                        break
                    if 'file' in lines[j]:
                        file_log_sink = True
                        break
                break

        if logging_stanza:
            if file_log_sink:
                add_result("AD17", "PASS")
            else:
                add_result("AD17", "FAIL", "File log sink NOT found in logging stanza.")
        else:
            add_result("AD17", "FAIL", "Logging stanza NOT found.")

    except FileNotFoundError:
        add_result("AD17", "FAIL", f"Configuration file not found: {config_file_path}")
    except Exception as e:
        add_result("AD17", "FAIL", f"An error occurred: {e}")

def check_aerospike_version(user_version):
    try:
        result = subprocess.run(['aerospike', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            installed_version = result.stdout.strip()

            accepted_versions = ['7.1.0', '7.0.0']
            accepted_versions.append(user_version)

            if installed_version in accepted_versions:
                add_result("AD15", "PASS")
            else:
                add_result("AD15", "FAIL", f"Aerospike version {installed_version} is installed but not accepted.")
        else:
            add_result("AD15", "FAIL", "Error retrieving Aerospike version.")
    except FileNotFoundError:
        add_result("AD15", "FAIL", "Aerospike command not found. Ensure Aerospike is installed and in the system PATH.")
    except Exception as e:
        add_result("AD15", "FAIL", f"An error occurred while checking Aerospike version: {e}")

def generate_html_report():
    total_pass = sum(1 for result in results if result["compliance"] == "PASS")
    total_fail = sum(1 for result in results if result["compliance"] == "FAIL")

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Compliance Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                width: 80%;
                margin: 0 auto;
                padding: 20px;
                background-color: #fff;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                margin-top: 30px;
            }}
            .header {{
                text-align: center;
                padding: 10px 0;
                border-bottom: 2px solid #333;
            }}
            .summary {{
                display: flex;
                justify-content: space-around;
                margin: 20px 0;
            }}
            .summary div {{
                padding: 20px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f9f9f9;
                text-align: center;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            table, th, td {{
                border: 1px solid #ddd;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            .fail-reason {{
                color: red;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Compliance Report</h1>
            </div>
            <div class="summary">
                <div>
                    <h2>Total PASS</h2>
                    <p>{total_pass}</p>
                </div>
                <div>
                    <h2>Total FAIL</h2>
                    <p>{total_fail}</p>
                </div>
            </div>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Compliance Result</th>
                    <th>Reason</th>
                </tr>
                {''.join([f'<tr><td>{result["id"]}</td><td>{result["compliance"]}</td><td class="fail-reason">{result["reason"]}</td></tr>' for result in results])}
            </table>
        </div>
    </body>
    </html>
    """

    with open("compliance_report.html", "w") as file:
        file.write(html_content)

if __name__ == "__main__":
    user_version = input("Enter the Aerospike DB version as per your bank policy: ")
    check_aerospike_version(user_version)

    config_file_path = input("Enter the path to the Aerospike configuration file: ")

    check_security_ldap_stanza(config_file_path)
    check_xdr_stanza(config_file_path)
    check_encryption_at_rest(config_file_path)
    check_tls_configuration(config_file_path)
    check_file_log_sink(config_file_path)
    check_backup_in_crontab()
    check_key_dat_encryption(config_file_path)
    check_log_files_presence()

    generate_html_report()
    print("Compliance report generated: compliance_report.html")
