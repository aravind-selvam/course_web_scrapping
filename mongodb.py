import pymongo


class mongodbconnection:
    ### This class shall be used for mongoDB operation ###
    def __init__(self, username, password):
        try:
            self.username = username
            self.password = password
            self.url = f"mongodb+srv://{self.username}:{self.password}@cluster0.wgmux.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        except Exception as e:
            raise e

    def getMongoClient(self):
        """
        It creates a MongoClient object.
        
        Returns:
          A MongoClient object
        """
        try:
            client = pymongo.MongoClient(self.url)
            return client
        except Exception as e:
            raise e

    def getDatabase(self, dbName):
        """
        It returns a database object.
        
        Args:
          dbName: The name of the database you want to connect to.
        
        Returns:
          A database object
        """
        try:
            client = self.getMongoClient()
            database = client[dbName]
            return database
        except Exception as e:
            raise e

    def getCollection(self, dbName, collectionName):
        """
        It gets the collection from the database.
        
        Args:
          dbName: The name of the database you want to connect to.
          collectionName: The name of the collection you want to get.
        
        Returns:
          A collection object
        """
        try:
            database = self.getDatabase(dbName)
            collection = database[collectionName]
            return collection
        except Exception as e:
            raise e

    def isDatabasePresent(self, dbName):
        """
        It checks if the database is present in the MongoDB server.
        
        Args:
          dbName: The name of the database you want to check for.
        
        Returns:
          A boolean value.
        """
        try:
            client = self.getMongoClient()
            if dbName in client.list_database_names():
                return True
            else:
                return False
        except Exception as e:
            raise e

    def isCollectionPresent(self, dbName, collectionName):
        """
        If the database exists, check if the collection exists. If it does, return True. If it doesn't,
        return False.
        
        Args:
          dbName: The name of the database.
          collectionName: The name of the collection you want to check for.
        
        Returns:
          A boolean value
        """
        try:
            if self.isDatabasePresent(dbName):
                database = self.getDatabase(dbName)
                if collectionName in database.list_collection_names():
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            raise e
