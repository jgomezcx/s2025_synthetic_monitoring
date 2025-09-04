**Ping Monitor Dashboard**
---
A lightweight Python-based **ping monitor** that exposes metrics to **Prometheus**, with dashboards in **Grafana**.  
Track **server uptime, latency, packet loss, and RTT trends** with simple YAML-based configuration.  

---
📌 Overview

This project is a coded lightweight Python-based ping monitor that exposes metrics to Prometheus, with dashboards in Grafana.
Track server uptime, latency, packet loss, and RTT trends with simple YAML-based configuration.

This project provides a network monitoring solution using Prometheus and Grafana. It allows you to monitor the availability and latency of servers through ICMP ping.

### The included Grafana dashboard displays:

#### - ✅ Server Status (Up/Down)
#### - 📈 Average RTT (Round Trip Time) trends
#### - 🔴 Min/Max RTT heatmap
#### - 🎛 Latest RTT values in gauges

This setup helps track the reliability and performance of external services or internal infrastructure.

## 🚀 Features  
- Ping multiple hosts/domains defined in a YAML file.  
- Configurable scrape interval and exporter port.  
- Exposes Prometheus metrics for:  
  - ✅ `ping_up` (server availability)  
  - 📦 `ping_packets_transmit`, `ping_packets_receive`  
  - 📉 `ping_packet_loss_ratio`  
  - ⏱ `ping_rtt_min_ms`, `ping_rtt_avg_ms`, `ping_rtt_max_ms`  
  - 📊 `ping_rtt_ms` (histogram for latency distribution)  
- Ready to visualize in **Grafana** dashboards.  


# 📂 Setup 
## 1. Prerequisites
 Make sure to download Grafana and Prometheus, along with the pingmonitor.py file in the repo
#### 1. https://prometheus.io/download/
- ```make sure to download the lastest "prometheus" LTS version since its usually the most stable```
#### 2. https://grafana.com/grafana/download
- ```for graphana, I downloaded the windows installer, and make it so i can run the app manually whenever I want through the command line (make sure you remember where the file is installed, you will need it to run the .exe file)```

#### 3. Python Pingmonitor.py (custom script) it will run in the background, pinging and storing all the information into the prometheus time series database automatically.
- Clone this repo (you only need the ping_monitor_exporter.py and domain.yaml files) 
```
git clone https://github.com/jgomezcx/s2025_synthetic_monitoring.git
```

```
# install the python file dependencies
pip install pingparsing prometheus-client pyyaml
```

```
# make sure to look inside the domain.yaml file to make the modifications such as which domains you want to ping, how long each interval ping should be, and change the port if you have something on port 8000 already. 
```

```
python ping-monitor-exporter.py -on windows
python3 ping-monitor-exporter.py -on mac
```


## 2. Run Prometheus 

**NOTE**: make sure you install prometheus via their website first

#### 1. Update the prometheus.yml file that comes inside the folder with the prometheus download.

```
scrape_configs:

    ## add this under the already existing code
  - job_name: "ping_monitor"
    static_configs:
      - targets: ["localhost:8000"]   # ping exporter endpoint
```
**make sure the targets matches what port you setup in the domain.yaml file**

#### 3. Run Prometheus
```
# running this in the command line will run prometheus
prometheus.exe
```
**you can verify prometheus is running by going to (http://localhost:9090/)**

## 3. Run Grafana

**NOTE:** make sure you install Graphana via their website first

#### 1. Start Grafana and connect it to Prometheus as a data source:

  - Navigate to Configuration → Data Sources

  - Add Prometheus (http://localhost:9090)

### 2. Import Dashboard

  - import the dashboard from the json file in the repo, or create your own new dashboard in Grafana

  refer to this documentation if you want to create a dashboard from scratch.
  - https://grafana.com/docs/grafana/latest/datasources/prometheus/

if you import dashboard using json
- Add panels using json provided

### 📊 Dashboard Panels

- Server Down Status

  - Uses ping_up metric
  - Displays servers as Running (1) or Down (0)

- Average RTT Ping (ms)
  - Line graph showing latency trends

- Heatmap displaying min/max values across time
  -  Ping RTT Min/Max (ms)

- Average RTT Gauges
  - Bar/Donut gauges for latest RTT values

## 🖼️ Example Dashboard


![image](https://i.imgur.com/SxXSnj5.png)



link https://imgur.com/a/R82dkkz.png

