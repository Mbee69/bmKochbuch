import uuid
import base64

import pickle
import os.path

import json


class Kochbuch:
    def __init__(self,name):
        self.name = name
        self.speisen = []
        self.kochbuch_guid = str(uuid.uuid4())

        self.load()

    def add_speise(self,Speise):
        self.speisen.append(Speise)

    def get_name(self):
        return self.name

    def get_guid(self):
        return self.kochbuch_guid
    
    def get_speisen(self):
        return self.speisen

    def del_speise(self,speise_guid):
        print(len(self.speisen))
        for speise in self.speisen:
            print(speise_guid)
            print(speise.get_guid())
            if speise.get_guid() == speise_guid:
                print("Del Found!!")
                self.speisen.remove(speise)
        print(len(self.speisen))

    def get_speise(self,speise_guid):
        for speise in self.speisen:
            if speise.get_guid() == speise_guid:
                print("get_speise: " + speise_guid)
                return speise     

    def save(self):
        print("save kochbuch")
        pickle.dump(self,open("./." + self.name + ".dat","wb"))

    def load(self):
        if os.path.isfile("./." + self.name + ".dat"):
            #self = pickle.load(open("./" + self.name + ".dat","rb"))
            kDatei = open("./." + self.name + ".dat", "rb")
            k = pickle.load(kDatei)
            kDatei.close()
            self.name = k.name
            self.kochbuch_guid = k.kochbuch_guid
            self.speisen = k.speisen
        else:
            print("New Kochbuch!!")
        return

class Speise:
    def __init__(self, name):
        self.name = name
        self.speise_guid = str(uuid.uuid4().hex)
        self.zutaten = []
        return

    def add_zutat(self,SpeiseZutat):
        self.zutaten.append(SpeiseZutat)

    def del_zutat(self,zutat_guid):
        for zutat in self.zutaten:
            if zutat.get_guid() == zutat_guid:
                self.zutaten.remove(zutat)

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def get_guid(self):
        return self.speise_guid

    def get_zutaten(self):
        return self.zutaten

    def get_zutat(self,zutat_guid):
        for zutat in self.zutaten:
            if zutat.get_guid() == zutat_guid:
                print("Del Found!!")
                return zutat     
class Zutat:
    def __init__(self, name, einheit, preis, menge, mindest):
        self.zutatguid = str(uuid.uuid4().hex)
        self.name = name
        self.einheit = einheit
        self.preis = preis
        self.mindest = mindest
        self.menge = menge
 
    def set_name(self,name):
        self.name = name

    def set_einheit(self,einheit):
        self.einheit = einheit

    def set_preis(self,preis):
        self.preis = preis
    
    def set_mindest(self,mindest):
        self.mindest = mindest
    
    def set_menge(self,menge):
        self.menge = menge
    
    def get_guid(self):
        return self.zutatguid

    def get_name(self):
        return self.name

    def get_einheit(self):
        return self.einheit

    def get_preis(self):
        return self.preis 

    def get_mindest(self):
        return self.mindest 

    def get_menge(self):
        return self.menge 
    
# class SpeiseZutat(Zutat):
#     def __init__(self,  name, einheit, preis, menge):
#         super().__init__( name, einheit, preis)
#         self.menge = menge

#         #self.load()
    
#     def set_menge(menge):
#         self.menge = menge

#     def get_menge():
#         return self.menge

class Lager:
    def __init__(self, name):
        self.name = name
        self.zutaten = []
        self.lager_guid = str(uuid.uuid4())

        self.load()

    def add_zutat(self, zutat):
        self.zutaten.append(zutat)
    
    def get_zutaten(self):
        return self.zutaten

    def get_zutat(self,zutat_guid):
        for zutat in self.zutaten:
            if zutat.get_guid() == zutat_guid:
                return zutat

    def del_zutat(self,zutat_guid):
        for zutat in self.zutaten:
            if zutat.get_guid() == zutat_guid:
                print("Del Found!!")
                self.zutaten.remove(zutat)

    def save(self):
        print("save lager")
        pickle.dump(self,open("./." + self.name + ".dat","wb"))

    def load(self):
        if os.path.isfile("./." + self.name + ".dat"):
            #self = pickle.load(open("./" + self.name + ".dat","rb"))
            kDatei = open("./." + self.name + ".dat", "rb")
            k = pickle.load(kDatei)
            kDatei.close()
            self.name = k.name
            self.lager_guid = k.lager_guid
            self.zutaten = k.zutaten
        else:
            print("New Lager!!")
        return


    
