import csv


# pull and convert package data from .csv into hash table for easier/faster reading and writing of data
class PackageHashTable:

    # create default hash table with default 40 empty entries
    # O(1)
    def __init__(self):
        self.size = 40
        self.map = [None] * self.size  # maybe change to [] ?

    def __setitem__(self, key, value):
        self.map[key] = value

    def get_hash(self, key):
        key_hash = key % self.size
        print('...MADE KEY HASH...', key_hash)
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
                    result_list.append(package)
        if result_list:
            return result_list
        else:
            return None

    # return package with matching key/id
    # should we just use __getitem__ ?
    # O(1)
    def search_by_key(self, key_input):
        # convert id to hash
        key = self.get_hash(int(key_input))
        # gets entry that matches key
        if self.map[key] is not None:
            print('---PACKAGE---', )
            return self.map[key]
        return None

    # insert package into hash table
    # O(1)
    def insert_package(self, key, package):
        hash_key = self.get_hash(int(package[0]))
        values = [key, package]

        if self.map[hash_key] is None:
            self.map[hash_key] = list(values)
        else:
            # replaces values for existing packages
            if self.map[hash_key] is not None:
                # TODO: test if this works
                self.__setitem__(hash_key, values)
                return True
            # adds package if no empty slots or existing match
            self.map[hash_key].append(values)


# gets package data from .csv and inserts into hash table
# O(N)
def retrieve_packages(package_file):
    package_hash_table = PackageHashTable()
    # use csv reader to get data
    with open(package_file) as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            package_hash_table.insert_package(row[0], row)
    return package_hash_table


# def search_by_value(value_input):
#     # search every element with something like a .contains or .includes?
#     # or get field to search by and input and search that way?
#     # return list of results matched
#
#     # O(N^2) bleh
#     result_list = []
#     # does not work
#     # for row in packages.table:
#     #     if row.index(value_input):
#     #         result_list.append(row)
#     for row in packages.map:
#         value_input in row:
#         result_list.append(row)
#
#
# if result_list:
#     return result_list
# else:
#     return 'No packages found.'

# Initialize hash table with package .csv
packages = retrieve_packages("WGUPS Package File.csv")
