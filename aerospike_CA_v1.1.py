import os
import subprocess

def check_security_ldap_stanza(config_file_path):
    """
    Check if the configuration file has a security stanza with an ldap sub-stanza.
    """
    try:
        with open(config_file_path, 'r') as file:
            config_content = file.read()
        
        if 'security {' in config_content:
            print("Security stanza found.")
            if 'ldap {' in config_content:
                print("LDAP is configured. - AD2 - PASS")
            else:
                print("LDAP is not configured. - AD2 - FAIL")
        else:
            print("Security stanza NOT found. - AD2 - FAIL")
            
    except FileNotFoundError:
        print(f"Configuration file not found: {config_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def check_xdr_stanza(config_file_path):
    """
    Check if the configuration file has an xdr stanza.
    """
    try:
        with open(config_file_path, 'r') as file:
            config_content = file.read()
        
        if 'xdr {' in config_content:
            print("XDR is configured. - AD2 - PASS")
        else:
            print("XDR is not configured. - AD2 - FAIL")
            
    except FileNotFoundError:
        print(f"Configuration file not found: {config_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def check_encryption_at_rest(config_file_path):
    """
    Check if the configuration file has encryption at rest configured.
    """
    try:
        with open(config_file_path, 'r') as file:
            config_content = file.read()
        
        if 'storage-engine device {' in config_content:
            print("Encryption at rest is configured. - AD3 - PASS")
        else:
            print("Encryption at rest is NOT configured. - AD3 - FAIL")
            
    except FileNotFoundError:
        print(f"Configuration file not found: {config_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def check_key_dat_encryption(config_file_path):
    """
    Check if 'encryption aes-' is present inside 'storage-engine device { }' stanza.
    """
    try:
        with open(config_file_path, 'r') as file:
            config_content = file.read()
        
        # Split the config content by 'storage-engine device { }' to check each occurrence
        storage_engine_blocks = config_content.split('storage-engine device {')
        
        found_encryption = False
        
        # Iterate over each block to check for 'encryption aes-' inside 'storage-engine device { }'
        for block in storage_engine_blocks[1:]:  # Start from index 1 to skip content before first occurrence
            if 'encryption aes-' in block:
                found_encryption = True
                break
        
        if found_encryption:
            print("Encryption aes- found inside storage-engine device { } stanza. - AD4 - PASS")
        else:
            print("Encryption aes- NOT found inside storage-engine device { } stanza. - AD4 - FAIL")
            
    except FileNotFoundError:
        print(f"Configuration file not found: {config_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def check_tls_configuration(config_file_path):
    """
    Check if the configuration file has the tls sub-stanza immediately after the service stanza
    and if it is enabled.
    """
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
            print("Service stanza found.")
            if tls_stanza:
                print("TLS sub-stanza found after service stanza. - AD9 - PASS")
                if tls_enabled:
                    print("TLS is enabled. - AD9 - PASS")
                else:
                    print("TLS is NOT enabled. - AD9 - FAIL")
            else:
                print("TLS sub-stanza NOT found after service stanza. - AD9 - FAIL")
        else:
            print("Service stanza NOT found. - AD9 - FAIL")
            
    except FileNotFoundError:
        print(f"Configuration file not found: {config_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def check_backup_in_crontab():
    """
    Check if backup scripts (as_incremental_backup.sh and as_full_backup.sh) are configured in crontab.
    """
    try:
        # Get the crontab entries using subprocess
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True, check=True)
        crontab_content = result.stdout
        
        # Check if as_incremental_backup.sh is configured in crontab
        if 'as_incremental_backup.sh' in crontab_content:
            print("Incremental backup script (as_incremental_backup.sh) is configured in crontab. - AD16 - PASS")
        else:
            print("Incremental backup script (as_incremental_backup.sh) is NOT configured in crontab. - AD16 - FAIL")
        
        # Check if as_full_backup.sh is configured in crontab
        if 'as_full_backup.sh' in crontab_content:
            print("Full backup script (as_full_backup.sh) is configured in crontab. - AD16 - PASS")
        else:
            print("Full backup script (as_full_backup.sh) is NOT configured in crontab. - AD16 - FAIL")
        
    except subprocess.CalledProcessError as e:
        print("Error retrieving crontab entries.")
    except FileNotFoundError:
        print("Error: crontab command not found. Ensure cron is installed and in the system PATH.")
    except Exception as e:
        print(f"An error occurred while checking crontab entries: {e}")

def check_log_files_presence():
    """
    Check if log files are present in the specified paths.
    """
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
                print(f"Log files found in {path}:")
				print("AD16 - PASS")
                for log_file in log_files:
                    print(f"- {log_file}")
            else:
                print(f"No log files found in {path}.")
				print("AD16 - FAIL")
        else:
            print(f"Path does not exist: {path}")

    if not log_files_found:
        print("No log files found in any of the specified paths.")



def check_file_log_sink(config_file_path):
    """
    Check if the configuration file has a logging stanza with a file log sink.
    """
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
            print("Logging stanza found.")
            if file_log_sink:
                print("File log sink found in logging stanza. - AD17 - PASS")
            else:
                print("File log sink NOT found in logging stanza. - AD17 - FAIL")
        else:
            print("Logging stanza NOT found. - AD17 - FAIL")
            
    except FileNotFoundError:
        print(f"Configuration file not found: {config_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def check_aerospike_version(user_version):
    """
    Check the installed Aerospike DB version against accepted versions including user-supplied version.
    
    Parameters:
    - user_version (str): User-supplied version to be included in the accepted versions list.
    """
    try:
        # Get the installed version of Aerospike DB
        result = subprocess.run(['aerospike', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            installed_version = result.stdout.strip()
            print(f"Installed Aerospike version: {installed_version}")

            # Define initial accepted versions
            accepted_versions = ['7.1.0', '7.0.0']
            
            # Add user-supplied version to accepted versions
            accepted_versions.append(user_version)

            # Check if installed version matches any accepted version
            if installed_version in accepted_versions:
                print(f"Aerospike version {installed_version} is installed and accepted. - AD15 - PASS")
            else:
                print(f"Aerospike version {installed_version} is installed but not accepted. - AD15 - FAIL")
        else:
            print("Error retrieving Aerospike version.")
    except FileNotFoundError:
        print("Aerospike command not found. Ensure Aerospike is installed and in the system PATH. - AD17 - FAIL")
    except Exception as e:
        print(f"An error occurred while checking Aerospike version: {e}")

if __name__ == "__main__":
    user_version = input("Enter the Aerospike DB version as per your bank policy: ")
    check_aerospike_version(user_version)
# Get the path to the Aerospike configuration file from the user
    config_file_path = input("Enter the path to the Aerospike configuration file: ")

# Run the checks on the configuration file
    check_security_ldap_stanza(config_file_path)
    check_xdr_stanza(config_file_path)
    check_encryption_at_rest(config_file_path)
    check_tls_configuration(config_file_path)
    check_file_log_sink(config_file_path)
    check_backup_in_crontab()
    check_key_dat_encryption(config_file_path)
    check_log_files_presence()
