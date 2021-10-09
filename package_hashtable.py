import csv


# pull and convert package data from .csv into hash table for easier/faster reading and writing of data
class PackageHashTable:

    # create default hash map with default 40 empty entries
    # O(1)
    def __init__(self):
        self.size = 100
        self.map = [None] * self.size

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
                # python still thinks rows consist of None even though hash table would be populated at this point?
                # and we're specifically saying not to search rows with None value?
                if value_input in package[1]:
                    # add packages with matched values to list to display to user
                    result_list.append(package[1])
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

    # insert package into hash table
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


# gets package data from .csv and inserts into hash table
# O(N)
def retrieve_packages(package_file):
    package_hash_table = PackageHashTable()
    # use csv reader to get data
    with open(package_file) as file:
        reader = csv.reader(file)
        # skip first row
        next(reader, None)
        # insert each row into hashmap
        for row in reader:
            package_hash_table.insert_package(row[0], row)
    return package_hash_table


# Initialize hash table with package .csv
packages_hash = retrieve_packages("data/WGUPS Package File.csv")
