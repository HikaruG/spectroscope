# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: validator/node.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='validator/node.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x14validator/node.proto\".\n\rValidatorList\x12\x1d\n\tvalidator\x18\x01 \x03(\x0b\x32\n.Validator\"!\n\tValidator\x12\x14\n\x0cvalidatorKey\x18\x01 \x01(\tb\x06proto3'
)




_VALIDATORLIST = _descriptor.Descriptor(
  name='ValidatorList',
  full_name='ValidatorList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='validator', full_name='ValidatorList.validator', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=24,
  serialized_end=70,
)


_VALIDATOR = _descriptor.Descriptor(
  name='Validator',
  full_name='Validator',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='validatorKey', full_name='Validator.validatorKey', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=72,
  serialized_end=105,
)

_VALIDATORLIST.fields_by_name['validator'].message_type = _VALIDATOR
DESCRIPTOR.message_types_by_name['ValidatorList'] = _VALIDATORLIST
DESCRIPTOR.message_types_by_name['Validator'] = _VALIDATOR
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ValidatorList = _reflection.GeneratedProtocolMessageType('ValidatorList', (_message.Message,), {
  'DESCRIPTOR' : _VALIDATORLIST,
  '__module__' : 'validator.node_pb2'
  # @@protoc_insertion_point(class_scope:ValidatorList)
  })
_sym_db.RegisterMessage(ValidatorList)

Validator = _reflection.GeneratedProtocolMessageType('Validator', (_message.Message,), {
  'DESCRIPTOR' : _VALIDATOR,
  '__module__' : 'validator.node_pb2'
  # @@protoc_insertion_point(class_scope:Validator)
  })
_sym_db.RegisterMessage(Validator)


# @@protoc_insertion_point(module_scope)