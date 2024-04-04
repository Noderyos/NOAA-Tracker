import random
import requests

months = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def retrieve_satelite(sat_id: int, all_passes: bool, is_utc: bool, std_time: bool, gmt_hours: int, lat: float,
                      lon: float):
    lines = requests.get(f"https://www.n2yo.com/passes/print.php" +
                         f"?s={sat_id}" +
                         f"&a={int(all_passes)}" +
                         f"&b={int(is_utc)}" +
                         f"&c={int(std_time)}" +
                         f"&d={gmt_hours}" +
                         f"&e={lat}" +
                         f"&f={lon}" +
                         f"&r={random.random()}").text.split("\n")

    passes = []
    data = []

    sat_start = 0
    sat_max = 0
    sat_end = 0
    mg = 0

    fields = ["range", "satla", "satlo", "elevation", "azimuth", "utc", "eclipsed", "sunElevation", "mag"]

    def parse_pos(l):
        idx = l.index("SatellitePosition")
        data = [a.strip(" '") for a in l[idx + 18:-2].strip("')").split(",")]
        assert len(data) == 9
        data = list(map(float, data))

        data[5] = int(data[5])
        data[6] = bool(data[6])
        return dict(zip(fields, data))

    for line in lines:
        if line.startswith("spStart = "): sat_start = parse_pos(line)
        if line.startswith("spMax = "): sat_max = parse_pos(line)
        if line.startswith("spEnd = "): sat_end = parse_pos(line)
        if line.startswith("mg="): mg = line.split("'")[1]
        if line.startswith("data.push"):
            data.append(parse_pos(line))

        if line.startswith("passes["):
            passes.append({
                "start": sat_start,
                "max": sat_max,
                "end": sat_end,
                "mag": mg,
                "data": data
            })
            data = []
    return passes

