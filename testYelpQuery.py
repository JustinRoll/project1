from yelpQuery import YelpQuery

def testQuery():
    yelpQuery = YelpQuery()
    yelpQuery.connect()
    response = yelpQuery.search(term='Jaffa Cafe', location = "San Luis Obispo", limit = 3)
    print(response["businesses"][0]["rating"])
    print(response["businesses"][0]["name"])
    print(response["businesses"][0]) 
    print(yelpQuery.getFeatures("Jaffa Cafe", "San Luis Obispo"))
def main():
    testQuery()

main()
