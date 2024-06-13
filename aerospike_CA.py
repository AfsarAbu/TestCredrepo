def check_security_ldap_stanza(config_file_path):
    """
    Check if the configuration file has a security stanza with an ldap sub-stanza.
    """
    try:
        with open(config_file_path, 'r') as file:
            config_content = file.read()
        
        # Check for the security stanza
        if 'security {' in config_content:
            print("Security stanza found.")
            
            # Check for the ldap sub-stanza
            if 'ldap {' in config_content:
                print("LDAP sub-stanza found inside the security stanza.")
            else:
                print("LDAP sub-stanza NOT found inside the security stanza.")
        else:
            print("Security stanza NOT found.")
            
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
        
        # Check for the xdr stanza
        if 'xdr {' in config_content:
            print("XDR stanza found.")
        else:
            print("XDR stanza NOT found.")
            
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
        
        # Check for encryption settings in the storage-engine stanza
        if 'storage-engine ' in config_content and 'data-encryption' in config_content:
            print("Encryption at rest is configured.")
        else:
            print("Encryption at rest is NOT configured.")
            
    except FileNotFoundError:
        print(f"Configuration file not found: {config_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def check_key_dat_encryption(key_dat_file_path):
    """
    Check if the key.dat file is encrypted.
    """
    try:
        with open(key_dat_file_path, 'rb') as file:
            file_header = file.read(16)  # Read the first 16 bytes to check for encryption header
        
        # Assuming encrypted files have a specific header, e.g., 'ENCRYPTED_HEADER'
        encrypted_header = b'ENCRYPTED_HEADER'
        
        if file_header.startswith(encrypted_header):
            print("The key.dat file is encrypted.")
        else:
            print("The key.dat file is NOT encrypted.")
            
    except FileNotFoundError:
        print(f"Key.dat file not found: {key_dat_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Get the path to the Aerospike configuration file from the user
config_file_path = input("Enter the path to the Aerospike configuration file: ")

# Run the checks on the configuration file
check_security_ldap_stanza(config_file_path)
check_xdr_stanza(config_file_path)
check_encryption_at_rest(config_file_path)

# Get the path to the key.dat file from the user
key_dat_file_path = input("Enter the path to the key.dat file: ")

# Run the check on the key.dat file
check_key_dat_encryption(key_dat_file_path)
