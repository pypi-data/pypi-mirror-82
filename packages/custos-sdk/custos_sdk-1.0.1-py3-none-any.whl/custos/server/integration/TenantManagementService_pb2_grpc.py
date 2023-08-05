# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import custos.server.core.IamAdminService_pb2 as IamAdminService__pb2
import custos.server.integration.TenantManagementService_pb2 as TenantManagementService__pb2
import custos.server.core.TenantProfileService_pb2 as TenantProfileService__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class TenantManagementServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.createTenant = channel.unary_unary(
        '/org.apache.custos.tenant.management.service.TenantManagementService/createTenant',
        request_serializer=TenantProfileService__pb2.Tenant.SerializeToString,
        response_deserializer=TenantManagementService__pb2.CreateTenantResponse.FromString,
        )
    self.getTenant = channel.unary_unary(
        '/org.apache.custos.tenant.management.service.TenantManagementService/getTenant',
        request_serializer=TenantManagementService__pb2.GetTenantRequest.SerializeToString,
        response_deserializer=TenantManagementService__pb2.GetTenantResponse.FromString,
        )
    self.updateTenant = channel.unary_unary(
        '/org.apache.custos.tenant.management.service.TenantManagementService/updateTenant',
        request_serializer=TenantManagementService__pb2.UpdateTenantRequest.SerializeToString,
        response_deserializer=TenantManagementService__pb2.GetTenantResponse.FromString,
        )
    self.deleteTenant = channel.unary_unary(
        '/org.apache.custos.tenant.management.service.TenantManagementService/deleteTenant',
        request_serializer=TenantManagementService__pb2.DeleteTenantRequest.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
    self.addTenantRoles = channel.unary_unary(
        '/org.apache.custos.tenant.management.service.TenantManagementService/addTenantRoles',
        request_serializer=IamAdminService__pb2.AddRolesRequest.SerializeToString,
        response_deserializer=IamAdminService__pb2.AllRoles.FromString,
        )
    self.addProtocolMapper = channel.unary_unary(
        '/org.apache.custos.tenant.management.service.TenantManagementService/addProtocolMapper',
        request_serializer=IamAdminService__pb2.AddProtocolMapperRequest.SerializeToString,
        response_deserializer=IamAdminService__pb2.OperationStatus.FromString,
        )
    self.configureEventPersistence = channel.unary_unary(
        '/org.apache.custos.tenant.management.service.TenantManagementService/configureEventPersistence',
        request_serializer=IamAdminService__pb2.EventPersistenceRequest.SerializeToString,
        response_deserializer=IamAdminService__pb2.OperationStatus.FromString,
        )
    self.updateTenantStatus = channel.unary_unary(
        '/org.apache.custos.tenant.management.service.TenantManagementService/updateTenantStatus',
        request_serializer=TenantProfileService__pb2.UpdateStatusRequest.SerializeToString,
        response_deserializer=TenantProfileService__pb2.UpdateStatusResponse.FromString,
        )
    self.getAllTenants = channel.unary_unary(
        '/org.apache.custos.tenant.management.service.TenantManagementService/getAllTenants',
        request_serializer=TenantProfileService__pb2.GetTenantsRequest.SerializeToString,
        response_deserializer=TenantProfileService__pb2.GetAllTenantsResponse.FromString,
        )
    self.getChildTenants = channel.unary_unary(
        '/org.apache.custos.tenant.management.service.TenantManagementService/getChildTenants',
        request_serializer=TenantProfileService__pb2.GetTenantsRequest.SerializeToString,
        response_deserializer=TenantProfileService__pb2.GetAllTenantsResponse.FromString,
        )
    self.getAllTenantsForUser = channel.unary_unary(
        '/org.apache.custos.tenant.management.service.TenantManagementService/getAllTenantsForUser',
        request_serializer=TenantProfileService__pb2.GetAllTenantsForUserRequest.SerializeToString,
        response_deserializer=TenantProfileService__pb2.GetAllTenantsForUserResponse.FromString,
        )
    self.getTenantStatusUpdateAuditTrail = channel.unary_unary(
        '/org.apache.custos.tenant.management.service.TenantManagementService/getTenantStatusUpdateAuditTrail',
        request_serializer=TenantProfileService__pb2.GetAuditTrailRequest.SerializeToString,
        response_deserializer=TenantProfileService__pb2.GetStatusUpdateAuditTrailResponse.FromString,
        )
    self.getTenantAttributeUpdateAuditTrail = channel.unary_unary(
        '/org.apache.custos.tenant.management.service.TenantManagementService/getTenantAttributeUpdateAuditTrail',
        request_serializer=TenantProfileService__pb2.GetAuditTrailRequest.SerializeToString,
        response_deserializer=TenantProfileService__pb2.GetAttributeUpdateAuditTrailResponse.FromString,
        )


class TenantManagementServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def createTenant(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getTenant(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def updateTenant(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def deleteTenant(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def addTenantRoles(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def addProtocolMapper(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def configureEventPersistence(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def updateTenantStatus(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getAllTenants(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getChildTenants(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getAllTenantsForUser(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getTenantStatusUpdateAuditTrail(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getTenantAttributeUpdateAuditTrail(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_TenantManagementServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'createTenant': grpc.unary_unary_rpc_method_handler(
          servicer.createTenant,
          request_deserializer=TenantProfileService__pb2.Tenant.FromString,
          response_serializer=TenantManagementService__pb2.CreateTenantResponse.SerializeToString,
      ),
      'getTenant': grpc.unary_unary_rpc_method_handler(
          servicer.getTenant,
          request_deserializer=TenantManagementService__pb2.GetTenantRequest.FromString,
          response_serializer=TenantManagementService__pb2.GetTenantResponse.SerializeToString,
      ),
      'updateTenant': grpc.unary_unary_rpc_method_handler(
          servicer.updateTenant,
          request_deserializer=TenantManagementService__pb2.UpdateTenantRequest.FromString,
          response_serializer=TenantManagementService__pb2.GetTenantResponse.SerializeToString,
      ),
      'deleteTenant': grpc.unary_unary_rpc_method_handler(
          servicer.deleteTenant,
          request_deserializer=TenantManagementService__pb2.DeleteTenantRequest.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
      'addTenantRoles': grpc.unary_unary_rpc_method_handler(
          servicer.addTenantRoles,
          request_deserializer=IamAdminService__pb2.AddRolesRequest.FromString,
          response_serializer=IamAdminService__pb2.AllRoles.SerializeToString,
      ),
      'addProtocolMapper': grpc.unary_unary_rpc_method_handler(
          servicer.addProtocolMapper,
          request_deserializer=IamAdminService__pb2.AddProtocolMapperRequest.FromString,
          response_serializer=IamAdminService__pb2.OperationStatus.SerializeToString,
      ),
      'configureEventPersistence': grpc.unary_unary_rpc_method_handler(
          servicer.configureEventPersistence,
          request_deserializer=IamAdminService__pb2.EventPersistenceRequest.FromString,
          response_serializer=IamAdminService__pb2.OperationStatus.SerializeToString,
      ),
      'updateTenantStatus': grpc.unary_unary_rpc_method_handler(
          servicer.updateTenantStatus,
          request_deserializer=TenantProfileService__pb2.UpdateStatusRequest.FromString,
          response_serializer=TenantProfileService__pb2.UpdateStatusResponse.SerializeToString,
      ),
      'getAllTenants': grpc.unary_unary_rpc_method_handler(
          servicer.getAllTenants,
          request_deserializer=TenantProfileService__pb2.GetTenantsRequest.FromString,
          response_serializer=TenantProfileService__pb2.GetAllTenantsResponse.SerializeToString,
      ),
      'getChildTenants': grpc.unary_unary_rpc_method_handler(
          servicer.getChildTenants,
          request_deserializer=TenantProfileService__pb2.GetTenantsRequest.FromString,
          response_serializer=TenantProfileService__pb2.GetAllTenantsResponse.SerializeToString,
      ),
      'getAllTenantsForUser': grpc.unary_unary_rpc_method_handler(
          servicer.getAllTenantsForUser,
          request_deserializer=TenantProfileService__pb2.GetAllTenantsForUserRequest.FromString,
          response_serializer=TenantProfileService__pb2.GetAllTenantsForUserResponse.SerializeToString,
      ),
      'getTenantStatusUpdateAuditTrail': grpc.unary_unary_rpc_method_handler(
          servicer.getTenantStatusUpdateAuditTrail,
          request_deserializer=TenantProfileService__pb2.GetAuditTrailRequest.FromString,
          response_serializer=TenantProfileService__pb2.GetStatusUpdateAuditTrailResponse.SerializeToString,
      ),
      'getTenantAttributeUpdateAuditTrail': grpc.unary_unary_rpc_method_handler(
          servicer.getTenantAttributeUpdateAuditTrail,
          request_deserializer=TenantProfileService__pb2.GetAuditTrailRequest.FromString,
          response_serializer=TenantProfileService__pb2.GetAttributeUpdateAuditTrailResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'org.apache.custos.tenant.management.service.TenantManagementService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
