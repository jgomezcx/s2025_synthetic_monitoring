from pingparsing import PingParsing, PingTransmitter
import yaml
import time

def execute_ping(destination, count=4):
    try:
        ping_parser = PingParsing()
        ping_transmitter = PingTransmitter()
        ping_transmitter.destination = destination
        ping_transmitter.count = count
        results = ping_transmitter.ping()
        parse_results = ping_parser.parse(results)
        # print(parse_results.as_dict()   )
        return parse_results.as_dict()

    except Exception as e:
        print(f"An error occurred while executing ping:\n {e}")
        return None

if __name__ == "__main__":
    ## assuming user input would be here ##
    # destination = input("Enter the destination to ping: ")
    # count = int(input("Enter the number of ping requests to send: "))
    sleep_time = 5  # seconds  (time to wait between ping sets)

    file_name = 'domain.yaml'
    dict_data = {}
    # dict_data = {'domains': [google.com, example.com, github.com]}

    try:
        with open(file_name, 'r') as file:
            data = yaml.safe_load(file)
            dict_data = data['domains']
    except Exception as error:
        print("Error reading YAML file\n:", error)

    print(dict_data)

    ping_counted = 1
    # while True:
    while ping_counted <= 2: #only run once
        print("==============================================================")
        print(f"{ping_counted} set of pings")
        for domain in dict_data:
            print(f"Pinging {domain}...")
            ping_result = execute_ping(domain, count=2)
            if ping_result:
                # Extract key metrics
                packet_transmit = ping_result['packet_transmit']
                packet_receive = ping_result['packet_receive']
                packet_loss_rate = ping_result['packet_loss_rate']
                rtt_min = ping_result['rtt_min']
                rtt_avg = ping_result['rtt_avg']
                rtt_max = ping_result['rtt_max']

                output = f"""
    Ping Metrics for Destination: {ping_result['destination']}
    --------------------------------------
    Packets: Transmitted = {packet_transmit},
    Received = {packet_receive}, Loss Rate = {packet_loss_rate:.2f}%
    RTT(ms):  Min = {rtt_min}, Avg = {rtt_avg}, Max = {rtt_max}
    """
                print(output)
            else:
                print(f"Failed to ping {domain}.")
        
        ping_counted += 1
        print(f"sleeping..... for {sleep_time} seconds")
        time.sleep(sleep_time)  # Wait for 5 seconds before the next set of pings

        