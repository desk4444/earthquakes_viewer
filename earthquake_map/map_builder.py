import json
from pathlib import Path
import folium
from earthquake_map.config import MAP_DIR


def build_and_save_map_from_data(data_path):
    file_path = Path(data_path)
    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    world_map = folium.Map(location=[0, 0], zoom_start=1, tiles="Esri WorldImagery")

    for feature in data["features"]:
        coords = feature["geometry"]["coordinates"]
        lon, lat = coords[0], coords[1]
        depth = coords[2] if len(coords) > 2 else "Unknown"
        props = feature["properties"]
        mag = props.get("mag") or 0
        place = props.get("place", "Unknown")
        popup_html = f"""
        <b>{place}</b><br>
        Magnitude: {mag}<br>
        Depth: {depth} km<br>
        <a href="{props.get("url", "#")}" target="_blank">USGS event page</a>
        """
        folium.CircleMarker(
                location=[lat, lon],
                radius=max(mag, 0.5) * 2,
                color="red",
                fill=True,
                fill_opacity=0.6,
                popup=folium.Popup(popup_html, max_width=300)
            ).add_to(world_map)
    day = Path(data_path).stem
    map_path = "{0}/{1}.html".format(MAP_DIR, day)
    Path(map_path).parent.mkdir(parents=True, exist_ok=True)
    world_map.save(map_path)
    return map_path


def build_index(map_dir):
    days = sorted((p.stem for p in Path(map_dir).glob("*.html") if p.stem != "index"), reverse=True)
    links = "\n".join(f'<li><a href="{day}.html">{day}</a></li>' for day in days)
    html = f"<html><body><h1>Earthquake maps</h1><ul>\n{links}\n</ul></body></html>"
    (Path(map_dir) / "index.html").write_text(html, encoding="utf-8")
