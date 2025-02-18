"""
This python script is to test the for/if, all and any.
"""
import time

with open('cities_file.txt', 'r', encoding="utf-8") as f:
    cities = [line.strip() for line in f]
print(f"{len(cities) = }")


def for_if_cities_capitalized() -> bool:
    """

    :return:         True or False.
    """
    for city in cities:
        # if city != city.capitalize():
        if city[0].islower():
            print(f"{city = }")
            return False
    return True


def all_cities_capitalized() -> bool:
    """

    :return:         True or False.
    """
    # return all(city == city.capitalize() for city in cities)
    return all(city[0].islower() for city in cities)


def any_cities_capitalized() -> bool:
    """

    :return:         True or False.
    """
    # return all(city == city.capitalize() for city in cities)
    return any(city[0].islower() for city in cities)


def main() -> None:
    """

    :return:         None.
    """
    # CPU Execution Time
    # get the start time
    st = time.process_time()
    print(f"{for_if_cities_capitalized() = }")
    # get the end time
    end = time.process_time()
    # get execution time
    print('CPU Execution time for/if:', end - st, 'seconds')

    # get the start time
    st = time.process_time()
    print(f"{all_cities_capitalized() = }")
    # get the end time
    end = time.process_time()
    # get execution time
    print('CPU Execution time all:', end - st, 'seconds')

    # get the start time
    st = time.process_time()
    print(f"{any_cities_capitalized() = }")
    # get the end time
    end = time.process_time()
    # get execution time
    print('CPU Execution time any:', end - st, 'seconds')


if __name__ == "__main__":
    main()
