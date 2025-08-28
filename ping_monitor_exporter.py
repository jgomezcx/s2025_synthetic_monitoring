
# ping_monitor_exporter.py
from pingparsing import PingParsing, PingTransmitter
from prometheus_client import start_http_server, Gauge, Histogram
import yaml
import time

# ---- Prometheus metric definitions ----
# "Latest" values (easy to read on the Prom UI)
PING_UP = Gauge("ping_up", "1 if ping received >=1, else 0", ["destination"])
PING_PACKET_LOSS_RATIO = Gauge("ping_packet_loss_ratio", "Loss ratio 0..1 for last run", ["destination"])
PING_TX = Gauge("ping_packets_transmit", "Packets transmitted (last run)", ["destination"])
PING_RX = Gauge("ping_packets_receive", "Packets received (last run)", ["destination"])
PING_RTT_MIN = Gauge("ping_rtt_min_ms", "Min RTT in ms (last run)", ["destination"])
PING_RTT_AVG = Gauge("ping_rtt_avg_ms", "Avg RTT in ms (last run)", ["destination"])
PING_RTT_MAX = Gauge("ping_rtt_max_ms", "Max RTT in ms (last run)", ["destination"])
PING_LAST_SCRAPE_TS = Gauge("ping_last_scrape_timestamp_seconds", "Unix time of last scrape", ["destination"])

# Optional: histogram for RTT so you can compute percentiles in PromQL
PING_RTT_HIST = Histogram(
    "ping_rtt_ms",
    "RTT distribution in ms",
    ["destination"],
    buckets=[1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
)

def execute_ping(destination: str, count: int = 4):
    parser = PingParsing()
    tx = PingTransmitter()
    tx.destination = destination
    tx.count = count
    result_text = tx.ping()
    return parser.parse(result_text).as_dict()

def normalize_loss_rate(raw):
    """
    pingparsing.packet_loss_rate is usually a percentage (e.g., 0.0, 25.0, 100.0).
    Convert to 0..1. If it's already 0..1, this keeps it correct.
    """
    if raw is None:
        return None
    return raw / 100.0 if raw > 1 else raw

def load_domains(path="domain.yaml"):
    try:
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        # expects:  domains: [ "google.com", "github.com" ]
        return data.get("domains", [])
    except FileNotFoundError:
        print(f"Warning: {path} not found.")
        raise Exception("Domain configuration file not found or loading error.")

def load_config(path="domain.yaml"):
    try:
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        # should return the time interval and port number from config
        # Grab values safely
        time_interval = data.get("time_interval", 5)  # default 5
        port_number = data.get("port_number", 8000)  # default 8000

        return time_interval, port_number
    except FileNotFoundError:
        print(f"Warning: {path} not found.")
        raise Exception("Configuration file not found or loading error.")

def scrape_once(destinations, ping_count=2):
    for dest in destinations:
        try:
            r = execute_ping(dest, count=ping_count)
        except Exception as e:
            # mark DOWN on exception
            PING_UP.labels(dest).set(1 if loss_ratio == 0.0 and rx > 0 else 0)
            continue

        # Update metrics
        tx = r.get("packet_transmit") or 0
        rx = r.get("packet_receive") or 0
        loss_ratio = normalize_loss_rate(r.get("packet_loss_rate") or 0.0)
        rtt_min = r.get("rtt_min")
        rtt_avg = r.get("rtt_avg")
        rtt_max = r.get("rtt_max")

        PING_TX.labels(dest).set(tx)
        PING_RX.labels(dest).set(rx)
        PING_UP.labels(dest).set(1 if rx > 0 else 0)
        PING_PACKET_LOSS_RATIO.labels(dest).set(loss_ratio if loss_ratio is not None else float("nan"))
        if rtt_min is not None: PING_RTT_MIN.labels(dest).set(rtt_min)
        if rtt_avg is not None:
            PING_RTT_AVG.labels(dest).set(rtt_avg)
            # Observe avg into histogram (simple, but useful for trends/percentiles)
            PING_RTT_HIST.labels(dest).observe(rtt_avg)
        if rtt_max is not None: PING_RTT_MAX.labels(dest).set(rtt_max)
        PING_LAST_SCRAPE_TS.labels(dest).set(time.time())

def main():
    # Config
    scrape_interval_seconds, metrics_port = load_config("domain.yaml")

    destinations = load_domains("domain.yaml")
    if not destinations:
        raise SystemExit("No domains found in domain.yaml (expected key: domains)")

    print("---------------------------------------------------------------------------------------------------")
    print(f"Starting exporter on :{metrics_port}, pinging: {destinations}, interval: {scrape_interval_seconds} seconds")
    print("===================================================================================================")


    start_http_server(metrics_port)

    # Main loop
    while True:
        print(f"[{time.strftime('%X')}] Scraping destinations...")
        scrape_once(destinations, ping_count=2)
        time.sleep(scrape_interval_seconds)

if __name__ == "__main__":
    main()
