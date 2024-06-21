import pymqi

def check_mq_attributes(qmgr_name, queue_name, channel, host, port, user, password):
    # Connection parameters
    conn_info = f"{host}({port})"
    
    # Create a queue manager connection
    qmgr = pymqi.QueueManager(None)
    
    try:
        # Connect to the queue manager
        qmgr.connectTCPClient(qmgr_name, pymqi.CD(), conn_info, channel, user, password)
        
        # Create a PCF object
        pcf = pymqi.PCFExecute(qmgr)

        # Check Queue Manager attributes
        qmgr_response = pcf.MQCMD_INQUIRE_Q_MGR({
            pymqi.CMQC.MQCA_Q_MGR_NAME: qmgr_name
        })

        perfmev = qmgr_response[0].get(pymqi.CMQCFC.MQIACF_PERMIT_EVENTS)
        print(f"PERFMEV (Queue Manager Performance Events): {perfmev}")

        # Check Queue attributes
        queue_response = pcf.MQCMD_INQUIRE_Q({
            pymqi.CMQC.MQCA_Q_NAME: queue_name
        })

        qdphiev = queue_response[0].get(pymqi.CMQC.MQIA_Q_DEPTH_HIGH_EVENT)
        print(f"QDPHIEV (Queue Depth High Event): {qdphiev}")
        
    except pymqi.MQMIError as e:
        print(f"MQ Error: {e}")
    finally:
        # Disconnect from the queue manager
        qmgr.disconnect()

# Get configuration parameters from user input
qmgr_name = input("Enter the Queue Manager name: ")
queue_name = input("Enter the Queue name: ")
channel = input("Enter the Channel name: ")
host = input("Enter the Host: ")
port = input("Enter the Port: ")
user = input("Enter the User: ")
password = input("Enter the Password: ")

check_mq_attributes(qmgr_name, queue_name, channel, host, port, user, password)
