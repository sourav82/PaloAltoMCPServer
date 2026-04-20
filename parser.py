
def parse_traffic_logs(raw_logs):
    entries = raw_logs.get("entry", [])

    if isinstance(entries, dict):
        entries = [entries]

    parsed = []

    for e in entries:
        parsed.append({
            "src_ip": e.get("src"),
            "dst_ip": e.get("dst"),
            "src_port": e.get("sport"),
            "dst_port": e.get("dport"),
            "action": e.get("action"),
            "rule": e.get("rule"),
            "app": e.get("app"),
            "bytes": e.get("bytes"),
            "start_time": e.get("start")
        })

    return parsed
