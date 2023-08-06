from confluent_kafka.schema_registry.avro import *
from confluent_kafka.schema_registry.json_schema import JSONSerializer, JSONDeserializer
from confluent_kafka.serialization import *

class Serializer(object):

    def get_avro_serializer(self, schema_str, schema_registry_client, to_dict=None, conf=None):
        return AvroSerializer(schema_str, schema_registry_client, to_dict, conf)

    def get_double_serializer(self):
        return DoubleSerializer()

    def get_integer_serializer(self):
        return IntegerSerializer()

    def get_json_serializer(self, schema_str, schema_registry_client, to_dict=None, conf=None):
        return JSONSerializer(schema_str, schema_registry_client, to_dict, conf)

    def get_protobuf_serializer(self, msg_type, schema_registry_client, conf=None):
        return ProtobufSerializer(msg_type, schema_registry_client, conf)

    def get_string_serializer(self, codec='utf_8'):
        return StringSerializer(codec)


class Deserializer(object):

    def get_avro_deserializer(self, schema_str, schema_registry_client, from_dict=None):
        return AvroDeserializer(schema_str, schema_registry_client, from_dict)

    def get_double_deserializer(self):
        return DoubleDeserializer()

    def get_integer_deserializer(self):
        return IntegerDeserializer()

    def get_json_deserializer(self, schema_str, from_dict=None):
        return JSONDeserializer(schema_str, from_dict)

    def get_protobuf_deserializer(self, message_type):
        return ProtobufDeserializer(message_type)

    def get_string_deserializer(self, codec='utf_8'):
        return StringDeserializer(codec)
