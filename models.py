# utils
from utils import get
from utils import post
from utils import auth

# typing
from typing import List

from itertools import groupby


class Dog(object):
    """
    Dog object that is composed of the id, name and breed of the dog

    To initialize:
    :param id: dog id
    :param name: dog name
    :param breed: dog breed id

    USAGE:
        >>> dog = Dog(id=1, name='Bobby', breed=1)
    """

    def __init__(self, id: int, name: str, breed: int):
        self.id = id
        self.name = name
        self.breed = breed


class Breed(object):
    """
    Breed object that is composed of the id and the name of the breed.

    To initialize:
    :param id: breed id
    :param name: breed name

    Also, breed has a list of dogs for development purposes
    :field dogs: breed dog list

    USAGE:
        >>> breed = Breed(id=1, name='Kiltro')
        >>> dog = Dog(id=1, name='Cachupin', breed=breed.id)
        >>> breed.add_dog(dog)
        >>> breed.dogs_count()
        1
    """

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.dogs: List[Dog] = []

    def add_dog(self, dog: Dog):
        self.dogs.append(dog)

    def dogs_count(self) -> int:
        return len(self.dogs)


class DogHouse(object):
    """
    Doghouse object that manipulates information on breeds and dogs.
    We expect you implement all the methods that are not implemented
    so that the flow works correctly


    DogHouse has a list of breeds and a list of dogs.
    :field breeds: breed list
    :field dogs: dog list

    USAGE:
        >>> dog_house = DogHouse()
        >>> dog_house.get_data(token='some_token')
        >>> total_dogs = dog_house.get_total_dogs()
        >>> common_breed = dog_house.get_common_breed()
        >>> common_dog_name = dog_house.get_common_dog_name()
        >>> total_breeds = dog_house.get_total_breeds()
        >>> data = {  # add some data
        ...     'total_dogs': total_dogs,
        ...     'total_breeds': total_breeds,
        ...     'common_breed': common_breed.name,
        ...     'common_dog_name': common_dog_name,
        ... }
        >>> token = 'some token'
        >>> dog_house.send_data(data=data, token=token)
    """

    def __init__(self):
        self.breeds: List[Breed] = []
        self.dogs: List[Dog] = []

    def get_data(self, token: str):
        """
        You must get breeds and dogs data from our API: http://dogs.magnet.cl

        We recommend using the Dog and Breed classes to store
        the information, also consider the dogs and breeds fields
        of the DogHouse class to perform data manipulation.
        """
        # Dogs
        flag_dogs_end = False
        dogs_next_page = 'http://dogs.magnet.cl/api/v1/dogs/'
        while not flag_dogs_end:
            dogs_response = get(dogs_next_page, token)
            dogs_next_page = dogs_response['next']
            flag_dogs_end = dogs_next_page == None
            for hash in dogs_response['results']:
                dog = Dog(hash['id'], hash['name'], hash['breed'])
                self.dogs.append(dog)
        # Breeds
        flag_breeds_end = False
        breeds_next_page = 'http://dogs.magnet.cl/api/v1/breeds/'
        while not flag_breeds_end:
            breeds_response = get(breeds_next_page, token)
            breeds_next_page = breeds_response['next']
            flag_breeds_end = breeds_next_page == None
            for hash in breeds_response['results']:
                breed = Breed(hash['id'], hash['name'])
                self.breeds.append(breed)

    def get_total_breeds(self) -> int:
        """
        Returns the amount of different breeds in the doghouse
        """
        return self.breeds.__len__()

    def get_total_dogs(self) -> int:
        """
        Returns the amount of dogs in the doghouse
        """
        return self.dogs.__len__()

    def get_common_breed(self) -> Breed:
        """
        Returns the most common breed in the doghouse
        """
        most_common_breed_id = None
        most_common_breed_quantity = 0
        sorted_breeds = sorted(self.dogs, key=lambda dog: dog.breed)
        for key, value in groupby(sorted_breeds, lambda item: item.breed):
            quantity = list(value).__len__()
            if quantity > most_common_breed_quantity:
                most_common_breed_id = key
                most_common_breed_quantity = quantity
        for breed in self.breeds:
            if(breed.id == most_common_breed_id):
                return breed

    def get_common_dog_name(self) -> str:
        """
        Returns the most common dog name in the doghouse
        """
        most_common_dog_name = None
        most_common_dog_name_quantity = 0
        sorted_dogs = sorted(self.dogs, key=lambda dog: dog.name)
        for key, value in groupby(sorted_dogs, lambda item: item.name):
            quantity = list(value).__len__()
            if quantity > most_common_dog_name_quantity:
                most_common_dog_name = key
                most_common_dog_name_quantity = quantity
        return most_common_dog_name

    def send_data(self, data: dict, token: str):
        """
        You must send the answers obtained from the implemented
        methods, the parameters are defined in the documentation.

        Important!! We don't tell you if the answer is correct
        """
        post('http://dogs.magnet.cl/api/v1/answer/', {
            'totalBreeds': data['total_breeds'],
            'totalDogs': data['total_dogs'],
            'commonBreed': data['common_breed'],
            'commonDogName': data['common_dog_name']
        }, token)
