# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import IdentityService_pb2 as IdentityService__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


class IdentityServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.authenticate = channel.unary_unary(
        '/org.apache.custos.identity.service.IdentityService/authenticate',
        request_serializer=IdentityService__pb2.AuthenticationRequest.SerializeToString,
        response_deserializer=IdentityService__pb2.AuthToken.FromString,
        )
    self.isAuthenticate = channel.unary_unary(
        '/org.apache.custos.identity.service.IdentityService/isAuthenticate',
        request_serializer=IdentityService__pb2.AuthToken.SerializeToString,
        response_deserializer=IdentityService__pb2.IsAuthenticateResponse.FromString,
        )
    self.getUser = channel.unary_unary(
        '/org.apache.custos.identity.service.IdentityService/getUser',
        request_serializer=IdentityService__pb2.AuthToken.SerializeToString,
        response_deserializer=IdentityService__pb2.User.FromString,
        )
    self.getUserManagementServiceAccountAccessToken = channel.unary_unary(
        '/org.apache.custos.identity.service.IdentityService/getUserManagementServiceAccountAccessToken',
        request_serializer=IdentityService__pb2.GetUserManagementSATokenRequest.SerializeToString,
        response_deserializer=IdentityService__pb2.AuthToken.FromString,
        )
    self.getToken = channel.unary_unary(
        '/org.apache.custos.identity.service.IdentityService/getToken',
        request_serializer=IdentityService__pb2.GetTokenRequest.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
        )
    self.getAuthorizeEndpoint = channel.unary_unary(
        '/org.apache.custos.identity.service.IdentityService/getAuthorizeEndpoint',
        request_serializer=IdentityService__pb2.GetAuthorizationEndpointRequest.SerializeToString,
        response_deserializer=IdentityService__pb2.AuthorizationResponse.FromString,
        )
    self.getOIDCConfiguration = channel.unary_unary(
        '/org.apache.custos.identity.service.IdentityService/getOIDCConfiguration',
        request_serializer=IdentityService__pb2.GetOIDCConfiguration.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
        )
    self.getTokenByPasswordGrantType = channel.unary_unary(
        '/org.apache.custos.identity.service.IdentityService/getTokenByPasswordGrantType',
        request_serializer=IdentityService__pb2.GetTokenRequest.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
        )
    self.getTokenByRefreshTokenGrantType = channel.unary_unary(
        '/org.apache.custos.identity.service.IdentityService/getTokenByRefreshTokenGrantType',
        request_serializer=IdentityService__pb2.GetTokenRequest.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
        )
    self.getJWKS = channel.unary_unary(
        '/org.apache.custos.identity.service.IdentityService/getJWKS',
        request_serializer=IdentityService__pb2.GetJWKSRequest.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
        )
    self.endSession = channel.unary_unary(
        '/org.apache.custos.identity.service.IdentityService/endSession',
        request_serializer=IdentityService__pb2.EndSessionRequest.SerializeToString,
        response_deserializer=IdentityService__pb2.OperationStatus.FromString,
        )


class IdentityServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def authenticate(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def isAuthenticate(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getUser(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getUserManagementServiceAccountAccessToken(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getToken(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getAuthorizeEndpoint(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getOIDCConfiguration(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getTokenByPasswordGrantType(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getTokenByRefreshTokenGrantType(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getJWKS(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def endSession(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_IdentityServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'authenticate': grpc.unary_unary_rpc_method_handler(
          servicer.authenticate,
          request_deserializer=IdentityService__pb2.AuthenticationRequest.FromString,
          response_serializer=IdentityService__pb2.AuthToken.SerializeToString,
      ),
      'isAuthenticate': grpc.unary_unary_rpc_method_handler(
          servicer.isAuthenticate,
          request_deserializer=IdentityService__pb2.AuthToken.FromString,
          response_serializer=IdentityService__pb2.IsAuthenticateResponse.SerializeToString,
      ),
      'getUser': grpc.unary_unary_rpc_method_handler(
          servicer.getUser,
          request_deserializer=IdentityService__pb2.AuthToken.FromString,
          response_serializer=IdentityService__pb2.User.SerializeToString,
      ),
      'getUserManagementServiceAccountAccessToken': grpc.unary_unary_rpc_method_handler(
          servicer.getUserManagementServiceAccountAccessToken,
          request_deserializer=IdentityService__pb2.GetUserManagementSATokenRequest.FromString,
          response_serializer=IdentityService__pb2.AuthToken.SerializeToString,
      ),
      'getToken': grpc.unary_unary_rpc_method_handler(
          servicer.getToken,
          request_deserializer=IdentityService__pb2.GetTokenRequest.FromString,
          response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
      ),
      'getAuthorizeEndpoint': grpc.unary_unary_rpc_method_handler(
          servicer.getAuthorizeEndpoint,
          request_deserializer=IdentityService__pb2.GetAuthorizationEndpointRequest.FromString,
          response_serializer=IdentityService__pb2.AuthorizationResponse.SerializeToString,
      ),
      'getOIDCConfiguration': grpc.unary_unary_rpc_method_handler(
          servicer.getOIDCConfiguration,
          request_deserializer=IdentityService__pb2.GetOIDCConfiguration.FromString,
          response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
      ),
      'getTokenByPasswordGrantType': grpc.unary_unary_rpc_method_handler(
          servicer.getTokenByPasswordGrantType,
          request_deserializer=IdentityService__pb2.GetTokenRequest.FromString,
          response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
      ),
      'getTokenByRefreshTokenGrantType': grpc.unary_unary_rpc_method_handler(
          servicer.getTokenByRefreshTokenGrantType,
          request_deserializer=IdentityService__pb2.GetTokenRequest.FromString,
          response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
      ),
      'getJWKS': grpc.unary_unary_rpc_method_handler(
          servicer.getJWKS,
          request_deserializer=IdentityService__pb2.GetJWKSRequest.FromString,
          response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
      ),
      'endSession': grpc.unary_unary_rpc_method_handler(
          servicer.endSession,
          request_deserializer=IdentityService__pb2.EndSessionRequest.FromString,
          response_serializer=IdentityService__pb2.OperationStatus.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'org.apache.custos.identity.service.IdentityService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
