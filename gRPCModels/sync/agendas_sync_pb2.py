# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: agendas_sync.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12\x61gendas_sync.proto\x12\x0b\x61genda_sync\x1a\x1bgoogle/protobuf/empty.proto\"6\n\x0cSyncResponse\x12\x11\n\tisSuccess\x18\x01 \x01(\x08\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\"*\n\x0bSyncContact\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05phone\x18\x02 \x01(\t\">\n\x10SyncContactsList\x12*\n\x08\x63ontacts\x18\x01 \x03(\x0b\x32\x18.agenda_sync.SyncContact2\xa5\x01\n\x11SyncAgendaService\x12G\n\x0bSyncAgendas\x12\x1d.agenda_sync.SyncContactsList\x1a\x19.agenda_sync.SyncResponse\x12G\n\x0eSyncFromOthers\x12\x16.google.protobuf.Empty\x1a\x1d.agenda_sync.SyncContactsListb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'agendas_sync_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_SYNCRESPONSE']._serialized_start=64
  _globals['_SYNCRESPONSE']._serialized_end=118
  _globals['_SYNCCONTACT']._serialized_start=120
  _globals['_SYNCCONTACT']._serialized_end=162
  _globals['_SYNCCONTACTSLIST']._serialized_start=164
  _globals['_SYNCCONTACTSLIST']._serialized_end=226
  _globals['_SYNCAGENDASERVICE']._serialized_start=229
  _globals['_SYNCAGENDASERVICE']._serialized_end=394
# @@protoc_insertion_point(module_scope)
