from earthquake_map.fetch import fetch_and_save_yesterday_earthquakes
from earthquake_map.map_builder import build_and_save_map_from_data, build_index
from earthquake_map.config import MAP_DIR


def main():
    data_path = fetch_and_save_yesterday_earthquakes()
    print("Saved earthquake data to {0}".format(data_path))
    map_path = build_and_save_map_from_data(data_path)
    print("Saved map to {0}".format(map_path))
    build_index(MAP_DIR)
    print("Index built !")


if __name__ == "__main__":
    main()
