
import os
import shutil
import time
import argparse
from datetime import datetime

def sync_folders(source, replica):
    changes = []

    if not os.path.exists(replica):
        os.makedirs(replica)

    for item in os.listdir(source):
        source_item = os.path.join(source, item)
        replica_item = os.path.join(replica, item)

        if os.path.isdir(source_item):
            changes.extend(sync_folders(source_item, replica_item))
        else:
            if not os.path.exists(replica_item) or os.path.getmtime(source_item) > os.path.getmtime(replica_item):
                shutil.copy2(source_item, replica_item)
                changes.append(f"Copying: {source_item} -> {replica_item}")

    for item in os.listdir(replica):
        replica_item = os.path.join(replica, item)
        source_item = os.path.join(source, item)

        if not os.path.exists(source_item):
            if os.path.isdir(replica_item):
                shutil.rmtree(replica_item)
            else:
                os.remove(replica_item)
            changes.append(f"Removing: {replica_item}")

    return changes

def main_loop(source_folder, replica_folder, interval, log_file):
    while True:
        changes = sync_folders(source_folder, replica_folder)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if changes:
            for change in changes:
                print(f"{timestamp} {change}")
                with open(log_file, "a") as log:
                    log.write(f"{timestamp} {change}\n")

        time.sleep(interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synchronize two folders at a specified interval and log changes.")
    parser.add_argument("source_folder", help="Path to the source folder")
    parser.add_argument("replica_folder", help="Path to the replica folder")
    parser.add_argument("interval_minutes", type=int, help="Synchronization interval in minutes")
    parser.add_argument("log_file", help="Path to the log file")

    args = parser.parse_args()

    main_loop(args.source_folder, args.replica_folder, args.interval_minutes * 60, args.log_file)