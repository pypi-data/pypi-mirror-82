# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ClusterManagementService.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='ClusterManagementService.proto',
  package='org.apache.custos.cluster.management.service',
  syntax='proto3',
  serialized_options=b'P\001',
  serialized_pb=b'\n\x1e\x43lusterManagementService.proto\x12,org.apache.custos.cluster.management.service\"D\n\x1bGetServerCertificateRequest\x12\x12\n\nsecretName\x18\x01 \x01(\t\x12\x11\n\tnamespace\x18\x02 \x01(\t\"3\n\x1cGetServerCertificateResponse\x12\x13\n\x0b\x63\x65rtificate\x18\x01 \x01(\t2\xd0\x01\n\x18\x43lusterManagementService\x12\xb3\x01\n\x1agetCustosServerCertificate\x12I.org.apache.custos.cluster.management.service.GetServerCertificateRequest\x1aJ.org.apache.custos.cluster.management.service.GetServerCertificateResponseB\x02P\x01\x62\x06proto3'
)




_GETSERVERCERTIFICATEREQUEST = _descriptor.Descriptor(
  name='GetServerCertificateRequest',
  full_name='org.apache.custos.cluster.management.service.GetServerCertificateRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='secretName', full_name='org.apache.custos.cluster.management.service.GetServerCertificateRequest.secretName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='namespace', full_name='org.apache.custos.cluster.management.service.GetServerCertificateRequest.namespace', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=80,
  serialized_end=148,
)


_GETSERVERCERTIFICATERESPONSE = _descriptor.Descriptor(
  name='GetServerCertificateResponse',
  full_name='org.apache.custos.cluster.management.service.GetServerCertificateResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='certificate', full_name='org.apache.custos.cluster.management.service.GetServerCertificateResponse.certificate', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=150,
  serialized_end=201,
)

DESCRIPTOR.message_types_by_name['GetServerCertificateRequest'] = _GETSERVERCERTIFICATEREQUEST
DESCRIPTOR.message_types_by_name['GetServerCertificateResponse'] = _GETSERVERCERTIFICATERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetServerCertificateRequest = _reflection.GeneratedProtocolMessageType('GetServerCertificateRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETSERVERCERTIFICATEREQUEST,
  '__module__' : 'ClusterManagementService_pb2'
  # @@protoc_insertion_point(class_scope:org.apache.custos.cluster.management.service.GetServerCertificateRequest)
  })
_sym_db.RegisterMessage(GetServerCertificateRequest)

GetServerCertificateResponse = _reflection.GeneratedProtocolMessageType('GetServerCertificateResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETSERVERCERTIFICATERESPONSE,
  '__module__' : 'ClusterManagementService_pb2'
  # @@protoc_insertion_point(class_scope:org.apache.custos.cluster.management.service.GetServerCertificateResponse)
  })
_sym_db.RegisterMessage(GetServerCertificateResponse)


DESCRIPTOR._options = None

_CLUSTERMANAGEMENTSERVICE = _descriptor.ServiceDescriptor(
  name='ClusterManagementService',
  full_name='org.apache.custos.cluster.management.service.ClusterManagementService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=204,
  serialized_end=412,
  methods=[
  _descriptor.MethodDescriptor(
    name='getCustosServerCertificate',
    full_name='org.apache.custos.cluster.management.service.ClusterManagementService.getCustosServerCertificate',
    index=0,
    containing_service=None,
    input_type=_GETSERVERCERTIFICATEREQUEST,
    output_type=_GETSERVERCERTIFICATERESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_CLUSTERMANAGEMENTSERVICE)

DESCRIPTOR.services_by_name['ClusterManagementService'] = _CLUSTERMANAGEMENTSERVICE

# @@protoc_insertion_point(module_scope)
