from yelpQuery import YelpQuery

def testQuery():
    yelpQuery = YelpQuery()
    yelpQuery.connect()
    response = yelpQuery.search(term='ice cream', location = "San Luis Obispo", limit = 3)
    print(response)

def main():
    testQuery()

main()
