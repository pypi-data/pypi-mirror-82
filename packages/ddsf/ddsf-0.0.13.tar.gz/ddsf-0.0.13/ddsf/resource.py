import json
import requests
import pymssql

class Resource():
    """
    base object for all Resources

    Attributes:
        session(requests.Session): requests session
        data(dict): all userData is stored inside this dict
        url: dsf base url
        db: db connection used by username()
    """
    def __len__(self):
        """
        returns length of data dict
        """
        return len(self.data)

    def __setattr__(self, name, value):
        """
        set value inside data dict

        Example:
           instead of changing data like this::

               person.data['FirstName'] = "Tadao"

           use this notation::

               person.FirstName = "Tadao"

        """
        self.data[name] = value

    def __getattr__(self, item):
        """
        tries to return members of the data dict

        Example:
           instead of accessing the data like ::

               user.data['UserAccount']

           use this notation::

               user.UserAccount

        """
        try:
            return self.data[item]
        except:
            pass
        return self.data[item[0].upper() + item[1:]]

    def __str__(self):
        """
        is called when you print the object

        Returns:
            str: prettyprinted data dict
        """
        return self.pretty()

    def serialize(self, obj):
        """
        this method is used by json.dumps() to serialize
        """
        return obj.data

    def pretty(self, sort=False):
        """
        pretty print data dict

        Returns:
            str: prettyprinted data dict
        """
        return json.dumps(self.data, indent=4, sort_keys=sort, default=self.serialize)

    # http methods
    def post(self):
        """
        post data to dsf-entity. You can create a new object and then call its `post()` method to create it in dsf.

        Returns:
            requests.Response : request object

        Example:
            This Example creates a new CommunicationNumber and creates it in dsf::

                data = {"Actor": user.ActorId,
                        "CommunicationType": 7,
                        "CommunicationNumberValue": ldapData['mail']}
                mail = CommunicationNumber(self.dsf.url, self.dsf.session, data)
                mail.post()
        """
        return self.session.post(self.url, json=self.data)

    def delete(self):
        """
        delete object from entity
        """
        return self.session.delete(f"{self.url[:-1]}{self.data[self.primaryKey]})")

    def patch(self):
        """
        patch object

        Example::

            person = dsf.person(123)
            person.FirstName = "Klaus"
            person.patch()
        """
        tempData = self.data.copy()
        data = self.session.patch(self.url[:-1] + f"{self.data[self.primaryKey]})", json=tempData)
        if data.status_code == 200:
            self.data = data.json()["value"][0]
        return data


class AcademicTitle(Resource):
    def __init__(self, url, session):
        object.__setattr__(self, "session", session)
        object.__setattr__(self, "data", {})
        object.__setattr__(self, "url", url + "AcademicTitle()")
        object.__setattr__(self, "filter", "?$filter=UserName eq '%d'")

    def get(self, id=None):
        object.__setattr__(self, "id", id)
        if id:
            data = self.session.get(self.url + self.filter % id)
            if data.status_code == 200:
                object.__setattr__(self, "data", data.json()["value"][0])
        else:
            data = self.session.get(self.url)
            if data.status_code == 200:
                object.__setattr__(self, "data", data.json()["value"])


class OrgUnit(Resource):
    def __init__(self, url, session, data={}, db=None):
        object.__setattr__(self, "session", session)
        object.__setattr__(self, "data", data)
        object.__setattr__(self, "db", db)
        object.__setattr__(self, "primaryKey", "OrgUnitId")
        object.__setattr__(self, "url", url + "OrgUnit()")

    def get(self, id):
        data = self.session.get(self.url + f"?$filter=OrgUnitId eq {id}")
        if data.status_code == 200:
            object.__setattr__(self, "data", data.json()["value"][0])


class OrgUnitType(Resource):
    def __init__(self, url, session, data={}, db=None):
        object.__setattr__(self, "session", session)
        object.__setattr__(self, "data", data)
        object.__setattr__(self, "db", db)
        object.__setattr__(self, "url", url + "OrgUnitType()")

    def get(self, id):
        data = self.session.get(self.url + f"?$filter=OrgUnitTypeId eq {id}")
        if data.status_code == 200:
            object.__setattr__(self, "data", data.json()["value"][0])


class Person(Resource):
    def __init__(self, url, session, data={}, db=None):
        object.__setattr__(self, "session", session)
        object.__setattr__(self, "data", data)
        object.__setattr__(self, "db", db)
        object.__setattr__(self, "primaryKey", "ActorId")
        object.__setattr__(self, "url", url + "Person()")


class Room(Resource):
    def __init__(self, url, session, data={}, db=None):
        object.__setattr__(self, "session", session)
        object.__setattr__(self, "data", data)
        object.__setattr__(self, "db", db)
        object.__setattr__(self, "primaryKey", "RoomId")
        object.__setattr__(self, "url", url + "Room()")

    def type(self):
        if type(self.data['RoomType']) is RoomType:
            return self.data['RoomType']
        url = self.url[:-2] + f"Type()?$filter=RoomTypeId eq {self.data['RoomType']}"
        data = self.session.get(url)
        return RoomType(url, self.session, data.json()['value'][0])


class RoomType(Resource):
    def __init__(self, url, session, data={}, db=None):
        object.__setattr__(self, "session", session)
        object.__setattr__(self, "data", data)
        object.__setattr__(self, "db", db)
        object.__setattr__(self, "url", url + "RoomType()")

    def get(self):
        data = self.session.get(self.url)
        if data.status_code == 200:
            object.__setattr__(self, "data", data.json()["value"][0])


class User(Resource):
    """
    represents User() entity

    """
    def __init__(self, url, session, data={}, db=None):
        object.__setattr__(self, "session", session)
        object.__setattr__(self, "data", data)
        object.__setattr__(self, "db", db)
        object.__setattr__(self, "primaryKey", "UserAccountId")
        object.__setattr__(self, "url", url + "UserAccount()")
        object.__setattr__(self, "base", url)

    def username(self, username):
        """
        change username of the User via database

        Attributes:
            username(str): new username for the user
        """
        if not self.db:
            raise Exception("connection to db is not made")
        # ensure username matches CN requirements
        self.UserName = username.upper()
        # check if username is already used
        cursor = self.db.cursor(as_dict=True)
        cursor.execute(f"SELECT COUNT(*) as count FROM campus.ACCO007 WHERE account_user = '{self.UserName}'")
        result = cursor.fetchone()
        if result["count"] != 0:
            raise Exception("username already used")

        cursor.execute(f"""UPDATE campus.ACCO007
                           SET account_user='{self.UserName}'
                           WHERE intnoobject={self.ActorId}""")

    def uniMail(self):
        """
        get uniMail of the User

        Returns:
            CommunicationNumber: uniMail
        """
        url = self.base + f"CommunicationNumber()?$filter=Actor eq {self.ActorId} and CommunicationType eq 7"
        data = self.session.get(url).json()["value"]
        if not data:
            return None
        return CommunicationNumber(self.base, self.session, data[0])

    def privateMail(self):
        """
        get privateMail of the User

        Returns:
            CommunicationNumber: privateMail
        """
        url = self.base + f"CommunicationNumber()?$filter=Actor eq {self.ActorId} and CommunicationType eq 3"
        data = self.session.get(url).json()["value"]
        if not data:
            return None
        return CommunicationNumber(self.base, self.session, data[0])

    def student(self):
        url = self.base + f"Student()?$filter=PersonId eq {self.ActorId}"
        data = self.session.get(url).json()["value"]
        if not data:
            return None
        print(data[0])
        #return CommunicationNumber(self.base, self.session, data[0])

    def actorTypes(self):
        """
        get all ActorTypes of a user

        Returns:
            list[ActorToActorType]: a list of Users ActorTypes

        """
        url = self.base + f"ActorToActorType()?$filter=Actor eq {self.ActorId}"
        data = self.session.get(url).json()["value"]
        if not data:
            return None
        returnData = []
        for entry in data:
            returnData.append(ActorToActorType(self.base, self.session, entry))
        return returnData

    def addActorType(self, actorTypeId):
        url = self.base + f"ActorToActorType()?$filter=Actor eq {self.ActorId} and ActorType eq {actorTypeId}"
        data = self.session.get(url).json()["value"]
        if len(data) != 0:
            print("user already has AT")
            return None
        data =  {"Actor": self.ActorId,
                 "ActorType": actorTypeId,
                 "Active": True}
        at = ActorToActorType(self.base, self.session, data)
        print(data)
        print(at.post())

    def removeActorType(self, actorTypeId):
        url = self.base + f"ActorToActorType()?$filter=Actor eq {self.ActorId} and ActorType eq {actorTypeId}"
        data = self.session.get(url).json()["value"]
        if len(data) == 0:
            print("user does not have AT")
            return None
        at = ActorToActorType(self.base, self.session, data[0])
        at.delete()

class CommunicationNumber(Resource):
    def __init__(self, url, session, data={}, db=None):
        object.__setattr__(self, "session", session)
        object.__setattr__(self, "data", data)
        object.__setattr__(self, "db", db)
        object.__setattr__(self, "url", url + "CommunicationNumber()")
        object.__setattr__(self, "filter", "?$filter=UserName eq '%s'")

    def patch(self):
        """
        patch CommunicationNumber. This method is overloaded because 3 ids are neccessary to patch an element
        """
        return self.session.patch(f"{self.url[:-1]}Actor={self.Actor}, CommunicationType={self.CommunicationType}L,Address=0L)", json=self.data)

    def delete(self):
        """
        delete CommunicationNumber. This method is overloaded because 3 ids are neccessary to patch an element
        """
        return self.session.delete(f"{self.url[:-1]}Actor={self.Actor}, CommunicationType={self.CommunicationType}L,Address=0L)")

class Student(Resource):
    def __init__(self, url, session, data={}, db=None):
        object.__setattr__(self, "session", session)
        object.__setattr__(self, "data", data)
        object.__setattr__(self, "db", db)
        object.__setattr__(self, "primaryKey", "UserAccountId")
        object.__setattr__(self, "url", url + "Student()")
        object.__setattr__(self, "base", url)
        object.__setattr__(self, "filter", "?$filter=UserName eq '%s'")

    def userAccount(self):
        url = self.base + f"UserAccount()?$filter=ActorId eq {self.PersonId}"
        data = self.session.get(url).json()["value"]
        if not data:
            return None
        return User(self.base, self.session, data[0], db=self.db)

class ActorToActorType(Resource):
    def __init__(self, url, session, data={}, db=None):
        object.__setattr__(self, "session", session)
        object.__setattr__(self, "data", data)
        object.__setattr__(self, "db", db)
        object.__setattr__(self, "url", url + "ActorToActorType()")
        object.__setattr__(self, "base", url)
        object.__setattr__(self, "filter", "?$filter=UserName eq '%s'")

    def delete(self):
        """
        delete ActorToActorType. This method is overloaded because 2 ids are neccessary to delete an element
        """
        return self.session.delete(f"{self.url[:-1]}Actor={self.Actor}, ActorType={self.ActorType})")
