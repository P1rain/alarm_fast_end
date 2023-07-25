import json

from DB.class_book import Book
from DB.class_manager_info import Manager
from DB.class_rental import Rental
from DB.class_reservation import Reservation
from DB.class_user import User


class ObjEncoder(json.JSONEncoder):
    _instance = None

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()

    def toJSON_as_binary(self, obj):
        if isinstance(obj, list):
            temp_list = list()
            for o in obj:
                str_obj = self.toJSON_an_object(o)
                temp_list.append(str_obj)
            list_json = json.dumps(temp_list, default=lambda o: o.__dict__)
            return list_json
        return self.toJSON_an_object_with_encode(obj)

    def toJSON_an_object_with_encode(self, obj):
        json_string = self.toJSON_an_object(obj)
        # return json_string.encode('utf-8')
        return json_string

    def toJSON_an_object(self, obj):
        print(obj.__dict__)
        string_converted_obj = json.dumps(obj, default=lambda o: o.__dict__)
        json_string = self.encode(string_converted_obj)
        return json_string


class ObjDecoder(json.JSONDecoder):
    _instance = None

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()

    def binary_to_obj(self, binary_str):
        if isinstance(binary_str, bytes):  # binary -> utf-8
            binary_str = binary_str.decode('utf-8')
        json_string = json.loads(binary_str)  # utf-8 -> json
        if isinstance(json_string, list):
            result_obj = self.list_mapper(json_string)
        else:
            result_obj = self.object_mapper(json_string)
        if result_obj is not None:
            return result_obj
        return json_string

        # json_to_object = json.loads(json_string)  # json -> dict(default)

    def object_mapper(self, dict_obj):
        if isinstance(dict_obj, str):
            dict_obj = json.loads(dict_obj)
        if isinstance(dict_obj, str):
            dict_obj = json.loads(dict_obj)
        assert isinstance(dict_obj, dict)
        if "book_writer" in dict_obj.keys():
            return Book(**dict_obj)
        elif "book_rental_date" in dict_obj.keys():
            return Rental(**dict_obj)
        elif "return_completed_date" in dict_obj.keys():
            return Reservation(**dict_obj)
        elif "user_name" in dict_obj.keys():
            return User(**dict_obj)
        elif "mng_id" in dict_obj.keys():
            return Manager(**dict_obj)

    def list_mapper(self, list_obj):
        assert isinstance(list_obj, list)
        result_list = list()
        for o in list_obj:
            converted_o = self.object_mapper(o)
            result_list.append(converted_o)
        return result_list


if __name__ == '__main__':
    msg_1 = Book('집으로 가는길', 'kdt23000001', '박선생', "소미", '2023.07')
    msg_2 = User('집으로 가는길', 'kdt23000001', '박선생', "소미", '2023.07')

    msg_list = [msg_1, msg_2]
    # print(id(msg_1))
    # print(id(msg_2))

    # print(msg_list)

    encoder = ObjEncoder()
    decoder = ObjDecoder()

    # list_obj_ = [msg_1, msg_2, msg_3, msg_4]
    # bytes_list_obj = encoder.toJSON_as_binary(msg_list)
    # result_list = decoder.binary_to_obj(bytes_list_obj)

    result = encoder.toJSON_as_binary(msg_1)
    result2 = encoder.toJSON_as_binary(msg_2)
    print(result)
    print(result2)

    result_obj = decoder.binary_to_obj(result)
    result_obj2 = decoder.binary_to_obj(result2)
    print(result_obj)
    print(result_obj2)
