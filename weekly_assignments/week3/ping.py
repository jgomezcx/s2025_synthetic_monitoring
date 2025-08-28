from pingparsing import PingParsing, PingTransmitter

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
    
# Example output:
"""PING google.com (216.58.196.238) 56(84) bytes of data.
64 bytes from lhr25s30-in-f14.1e100.net (216.58.196.238): icmp_seq=1 ttl=54 time=37.341 ms
64 bytes from lhr25s30-in-f14.1e100.net (216.58.196.238): icmp_seq=2 ttl=54 time=45.678 ms
--- google.com ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 37.341/41.509/45.678/4.168 ms
"""

# Example: Executing ping and parsing the result
# ping_transmitter = PingTransmitter()
# ping_transmitter.destination = "google.com"
# ping_transmitter.count = 1
# result = ping_transmitter.ping()
# print(result._asdict())

if __name__ == "__main__":
    ## assuming user input would be here ##
    # destination = input("Enter the destination to ping: ")
    # count = int(input("Enter the number of ping requests to send: "))
    
    destination = "google.com"
    count = 4
    ping_result = execute_ping(destination, count)
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
        Received = {packet_receive},
        Loss Rate = {packet_loss_rate:.2f}%
        RTT(ms): 
        \tMin = {rtt_min},
        \tAvg = {rtt_avg},
        \tMax = {rtt_max}
        """
    else:
        output = "No valid ping result available."
    
    print(output)
