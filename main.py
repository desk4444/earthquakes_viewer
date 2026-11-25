from earthquake_map.fetch import fetch_and_save_yesterday_earthquakes


def main():
    path = fetch_and_save_yesterday_earthquakes()
    print("Saved earthquake data to {0}".format(path))


if __name__ == "__main__":
    main()
