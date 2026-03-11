import socket
import time
from datetime import datetime
from pyais import decode

# Configuration
HOST = "153.44.253.27"
PORT = 5631
OUTPUT_RAW = "../data/raw/ais_raw_{}.txt".format(datetime.now().strftime("%Y%m%d_%H%M"))
OUTPUT_CSV = "../data/processed/ais_decoded_{}.csv".format(datetime.now().strftime("%Y%m%d_%H%M"))
CAPTURE_HOURS = 24  # how long to capture

# Setup output files
raw_file = open(OUTPUT_RAW, "w")
csv_file = open(OUTPUT_CSV, "w")
csv_file.write("timestamp,raw,msg_type,mmsi,lat,lon,sog,cog,heading,rot,nav_status,ship_type\n")

print(f"Saving raw NMEA to: {OUTPUT_RAW}")
print(f"Saving decoded CSV to: {OUTPUT_CSV}")

# Connect
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
sock.settimeout(30)

print(f"Connected to {HOST}:{PORT}")
print(f"Capturing for {CAPTURE_HOURS} hours. Started at {datetime.now().strftime('%H:%M:%S')}\n")

start_time = time.time()
end_time = start_time + (CAPTURE_HOURS * 3600)
msg_count = 0
decode_errors = 0

try:
    while time.time() < end_time:
        try:
            data = sock.recv(4096)
            if not data:
                print("Connection lost, reconnecting...")
                sock.close()
                time.sleep(5)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((HOST, PORT))
                sock.settimeout(30)
                continue

            for line in data.split(b"\n"):
                line = line.strip()
                if not line:
                    continue

                try:
                    nmea_str = line.decode("utf-8", errors="ignore")
                except:
                    continue

                # Save raw line
                timestamp = datetime.now().isoformat()
                raw_file.write(f"{timestamp},{nmea_str}\n")

                # Try to decode
                try:
                    decoded = decode(nmea_str)
                    d = decoded.asdict()

                    row = "{},{},{},{},{},{},{},{},{},{},{},{}".format(
                        timestamp,
                        nmea_str.replace(",", ";"),  # escape commas in raw msg
                        d.get("msg_type", ""),
                        d.get("mmsi", ""),
                        d.get("lat", ""),
                        d.get("lon", ""),
                        d.get("speed", ""),
                        d.get("course", ""),
                        d.get("heading", ""),
                        d.get("turn", ""),
                        d.get("status", ""),
                        d.get("ship_type", ""),
                    )
                    csv_file.write(row + "\n")
                    msg_count += 1

                except Exception:
                    decode_errors += 1

                # Flush every 100 messages so data is saved even if script crashes
                if msg_count % 100 == 0:
                    raw_file.flush()
                    csv_file.flush()

                # Print progress every 1000 messages
                if msg_count % 1000 == 0 and msg_count > 0:
                    elapsed = (time.time() - start_time) / 3600
                    print(f"  {msg_count} messages decoded | {decode_errors} errors | {elapsed:.1f}h elapsed")

        except socket.timeout:
            continue

except KeyboardInterrupt:
    print("\nCapture stopped manually.")

finally:
    raw_file.close()
    csv_file.close()
    sock.close()
    elapsed = (time.time() - start_time) / 3600
    print(f"\nDone. {msg_count} messages decoded, {decode_errors} errors, {elapsed:.1f} hours captured.")
    print(f"Raw data: {OUTPUT_RAW}")
    print(f"Decoded data: {OUTPUT_CSV}")