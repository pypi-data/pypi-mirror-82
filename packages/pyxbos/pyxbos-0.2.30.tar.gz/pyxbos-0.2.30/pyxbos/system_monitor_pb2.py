# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: system_monitor.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import nullabletypes_pb2 as nullabletypes__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='system_monitor.proto',
  package='xbospb',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x14system_monitor.proto\x12\x06xbospb\x1a\x13nullabletypes.proto\"\xcc\x01\n\x11\x42\x61sicServerStatus\x12\x0c\n\x04time\x18\x01 \x01(\x04\x12\x10\n\x08hostname\x18\x06 \x01(\t\x12 \n\x08\x63pu_load\x18\x02 \x03(\x0b\x32\x0e.xbospb.Double\x12)\n\x12phys_mem_available\x18\x03 \x01(\x0b\x32\r.xbospb.Int64\x12\"\n\ndisk_usage\x18\x04 \x01(\x0b\x32\x0e.xbospb.Double\x12&\n\x0e\x64isk_available\x18\x05 \x01(\x0b\x32\x0e.xbospb.Doubleb\x06proto3')
  ,
  dependencies=[nullabletypes__pb2.DESCRIPTOR,])




_BASICSERVERSTATUS = _descriptor.Descriptor(
  name='BasicServerStatus',
  full_name='xbospb.BasicServerStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='time', full_name='xbospb.BasicServerStatus.time', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hostname', full_name='xbospb.BasicServerStatus.hostname', index=1,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cpu_load', full_name='xbospb.BasicServerStatus.cpu_load', index=2,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='phys_mem_available', full_name='xbospb.BasicServerStatus.phys_mem_available', index=3,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='disk_usage', full_name='xbospb.BasicServerStatus.disk_usage', index=4,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='disk_available', full_name='xbospb.BasicServerStatus.disk_available', index=5,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=54,
  serialized_end=258,
)

_BASICSERVERSTATUS.fields_by_name['cpu_load'].message_type = nullabletypes__pb2._DOUBLE
_BASICSERVERSTATUS.fields_by_name['phys_mem_available'].message_type = nullabletypes__pb2._INT64
_BASICSERVERSTATUS.fields_by_name['disk_usage'].message_type = nullabletypes__pb2._DOUBLE
_BASICSERVERSTATUS.fields_by_name['disk_available'].message_type = nullabletypes__pb2._DOUBLE
DESCRIPTOR.message_types_by_name['BasicServerStatus'] = _BASICSERVERSTATUS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BasicServerStatus = _reflection.GeneratedProtocolMessageType('BasicServerStatus', (_message.Message,), dict(
  DESCRIPTOR = _BASICSERVERSTATUS,
  __module__ = 'system_monitor_pb2'
  # @@protoc_insertion_point(class_scope:xbospb.BasicServerStatus)
  ))
_sym_db.RegisterMessage(BasicServerStatus)


# @@protoc_insertion_point(module_scope)
