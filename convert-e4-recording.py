import argparse
import os

VALID_TYPES = ["acc", "bvp", "temp", "eda", "tag"]


def convert_logs(log_dir, output_file, types):
    # Check if log directory exists
    if not os.path.exists(log_dir):
        print(f"Directory not found: {log_dir}")
        sys.exit(0)

    events = []
    for t in types:
        log_file = os.path.join(log_dir, f"{t.upper()}.csv")
        if not os.path.exists(log_file):
            print(f"File not found: {log_file}")
            continue

        output_type = t
        if t == "eda":
            output_type = "gsr"

        with open(log_file, "r") as f:
            lines = list(f)
            dt = float(lines[0].split(",")[0])
            sample_rate = float(lines[1].split(",")[0])
            index = 0
            for line in lines[2:]:
                line = line.strip()
                values = [float(x) for x in line.split(",")]
                events.append(
                    {
                        "dt": dt + index / sample_rate,
                        "device_uid": "E4",
                        "type": output_type,
                        "values": values,
                    }
                )
                index += 1

    # Sort the events by timestamp
    events = sorted(events, key=lambda x: x["dt"])

    start_time = events[0]["dt"]

    # Write the events to the output file
    with open(output_file, "w") as record_log_file:
        for event in events:
            dt = event["dt"] - start_time
            device_uid = event["device_uid"]
            event_type = event["type"]
            sample = event["values"]
            value_string = ",".join([f"{x:0.2f}" for x in sample])
            record_log_file.write(
                f"{dt:.02f},{device_uid},{event_type},{value_string}\n"
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert E4 Logs to replayable logs.")
    parser.add_argument(
        "e4_dir", type=str, help="E4 Capture directory (containing BVP.csv etc.)"
    )
    parser.add_argument("log_file", type=str, help="Output log file (e.g. my-log.txt)")
    parser.add_argument(
        "--type",
        type=str,
        help="Filters the event type, separated by commas (e.g. bvp, gsr)",
        default=None,
    )

    args = parser.parse_args()
    types = VALID_TYPES
    if args.type:
        types = args.type.split(",")
        types = [t.strip() for t in types]
        # Check if all types are valid
        for t in types:
            if t not in VALID_TYPES:
                print(f"Invalid event type: {t}")
                sys.exit(0)

    convert_logs(args.e4_dir, args.log_file, types)
