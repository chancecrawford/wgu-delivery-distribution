# Chance Crawford --- Student ID:

import csv


# pull and convert package data from .csv into hash map for easier/faster reading and writing of data
class PackageHashMap:

    # create default hash map with default 40 empty entries
    # O(N) since python still iterates over each element in creation
    def __init__(self):
        self.size = 100
        self.map = [None] * self.size

    # create hash from package id
    # O(1)
    def get_hash(self, key):
        key_hash = key % self.size
        return key_hash

    # return list of results by value
    # O(N^2)
    def search_by_value(self, value_input):
        # have to iterate through rows, then iterate through values in each row
        result_list = []
        for package in self.map:
            # pass over null entries
            if package is not None:
                # check if any element in list contains substring
                if any(value_input in string for string in package[1]):
                    # add packages with matched values to list to display to user
                    result_list.append(package[1])
        # make sure list isn't empty
        if result_list:
            return result_list
        else:
            return None

    # return package with matching key
    # O(1)
    def search_by_key(self, key_input):
        # convert id to hash
        key_hash = self.get_hash(int(key_input))
        # gets entry that matches key
        if self.map[key_hash][0] == key_input:
            return self.map[key_hash][1]
        return None

    # insert package into hash map
    # O(1)
    def insert_package(self, key, package):
        hash_key = self.get_hash(int(package[0]))
        values = [key, package]
        # if row empty, insert values
        if self.map[hash_key] is None:
            self.map[hash_key] = list(values)
        else:
            # replaces values for existing packages
            for entry in self.map[hash_key]:
                if entry[0] == key:
                    entry[1] = values
            # adds package if no empty slots or existing match
            self.map[hash_key].append(values)


# https://docs.python.org/3/library/csv.html
# gets package data from .csv and inserts into hash map
# O(N)
def retrieve_packages(package_file):
    package_hash_map = PackageHashMap()
    # use csv reader to get data
    with open(package_file) as file:
        reader = csv.reader(file)
        # skip first row
        next(reader, None)
        # insert each row into hashmap
        for row in reader:
            package_hash_map.insert_package(row[0], row)
    return package_hash_map


# Initialize hash map with package .csv
packages_hash = retrieve_packages("data/WGUPS Package File.csv")
