import sqlite3

database_path = "./search.db"

try:
    connection = sqlite3.connect(database_path)
except:
    print "Invalid database path."
    exit()


def print_header():
    print "\n********** Options **********"
    print "[1] Search by Word"
    print "[2] Search by URL"
    print "[3] Search by Frequency"
    print "[4] Exit the System"
    print "*****************************\n"


def search(search_attribute, search_term):
    search_condition_string = search_attribute + " = ?"
    if search_attribute == "url":
        search_condition_string = search_attribute + " LIKE ?"

    search_results = connection.execute(
        "SELECT * FROM data WHERE " + search_condition_string +
        " ORDER BY frequency DESC", (search_term,))

    return search_results


def print_search_results(search_results):
    print "\n========================= SEARCH ========================="
    search_results = search_results.fetchall()
    number_of_found_rows = len(search_results)
    if number_of_found_rows == 0:
        print "*** NO RESULTS FOUND ***"
    else:
        print "***** Search matched ", str(number_of_found_rows) \
            " results *****"

        print "  %-20s %-10s %s" % ("Word", "Frequency", "URL")

        row_counter = 0
        for row in search_results:
            word = row[0]
            url = row[1]
            frequency = row[2]

            print "  %-20s %-10s %s" % (word, str(frequency), url)
            row_counter += 1

            if (row_counter >= 100):
                print "Search stopped after 100 results."
                break

    print "==========================================================\n"


def get_search_term(search_attribute):
    while True:
        search_term = raw_input("Enter your search " + search_attribute + ": ")

        if (len(search_term.split()) == 1):
            return search_term.lower()
        else:
            print "Error: Only one search term is allowed."


def search_by_word():
    search_term = get_search_term("term")
    search_results = search("word", search_term)
    print_search_results(search_results)


def search_by_URL():
    search_term = get_search_term("URL")
    search_term = "%" + search_term + "%"
    search_results = search("url", search_term)
    print_search_results(search_results)


def search_by_frequency():
    search_term = get_search_term("frequency")
    search_results = search("frequency", search_term)
    print_search_results(search_results)

print "Welcome to the Database Search Engine"
while True:
    print_header()

    selection = raw_input("Enter your option: ")

    if (selection == "1"):
        search_by_word()
    elif (selection == "2"):
        search_by_URL()
    elif (selection == "3"):
        search_by_frequency()
    elif (selection == "4"):
        print "Goodbye!"
        exit()
    else:
        print "Invalid Option"
