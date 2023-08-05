# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from dapr.proto.common.v1 import common_pb2 as dapr_dot_proto_dot_common_dot_v1_dot_common__pb2
from dapr.proto.runtime.v1 import dapr_pb2 as dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class DaprStub(object):
  """Dapr service provides APIs to user application to access Dapr building blocks.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.InvokeService = channel.unary_unary(
        '/dapr.proto.runtime.v1.Dapr/InvokeService',
        request_serializer=dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2.InvokeServiceRequest.SerializeToString,
        response_deserializer=dapr_dot_proto_dot_common_dot_v1_dot_common__pb2.InvokeResponse.FromString,
        )
    self.GetState = channel.unary_unary(
        '/dapr.proto.runtime.v1.Dapr/GetState',
        request_serializer=dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2.GetStateRequest.SerializeToString,
        response_deserializer=dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2.GetStateResponse.FromString,
        )
    self.GetBulkState = channel.unary_unary(
        '/dapr.proto.runtime.v1.Dapr/GetBulkState',
        request_serializer=dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2.GetBulkStateRequest.SerializeToString,
        response_deserializer=dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2.GetBulkStateResponse.FromString,
        )
    self.SaveState = channel.unary_unary(
        '/dapr.proto.runtime.v1.Dapr/SaveState',
        request_serializer=dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2.SaveStateRequest.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
    self.DeleteState = channel.unary_unary(
        '/dapr.proto.runtime.v1.Dapr/DeleteState',
        request_serializer=dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2.DeleteStateRequest.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
    self.ExecuteStateTransaction = channel.unary_unary(
        '/dapr.proto.runtime.v1.Dapr/ExecuteStateTransaction',
        request_serializer=dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2.ExecuteStateTransactionRequest.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
    self.PublishEvent = channel.unary_unary(
        '/dapr.proto.runtime.v1.Dapr/PublishEvent',
        request_serializer=dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2.PublishEventRequest.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
    self.InvokeBinding = channel.unary_unary(
        '/dapr.proto.runtime.v1.Dapr/InvokeBinding',
        request_serializer=dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2.InvokeBindingRequest.SerializeToString,
        response_deserializer=dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2.InvokeBindingResponse.FromString,
        )
    self.GetSecret = channel.unary_unary(
        '/dapr.proto.runtime.v1.Dapr/GetSecret',
        request_serializer=dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2.GetSecretRequest.SerializeToString,
        response_deserializer=dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2.GetSecretResponse.FromString,
        )


class DaprServicer(object):
  """Dapr service provides APIs to user application to access Dapr building blocks.
  """

  def InvokeService(self, request, context):
    """Invokes a method on a remote Dapr app.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetState(self, request, context):
    """Gets the state for a specific key.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetBulkState(self, request, context):
    """Gets a bulk of state items for a list of keys
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SaveState(self, request, context):
    """Saves the state for a specific key.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DeleteState(self, request, context):
    """Deletes the state for a specific key.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ExecuteStateTransaction(self, request, context):
    """Executes transactions for a specified store
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def PublishEvent(self, request, context):
    """Publishes events to the specific topic.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def InvokeBinding(self, request, context):
    """Invokes binding data to specific output bindings
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetSecret(self, request, context):
    """Gets secrets from secret stores.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_DaprServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'InvokeService': grpc.unary_unary_rpc_method_handler(
          servicer.InvokeService,
          request_deserializer=dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2.InvokeServiceRequest.FromString,
          response_serializer=dapr_dot_proto_dot_common_dot_v1_dot_common__pb2.InvokeResponse.SerializeToString,
      ),
      'GetState': grpc.unary_unary_rpc_method_handler(
          servicer.GetState,
          request_deserializer=dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2.GetStateRequest.FromString,
          response_serializer=dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2.GetStateResponse.SerializeToString,
      ),
      'GetBulkState': grpc.unary_unary_rpc_method_handler(
          servicer.GetBulkState,
          request_deserializer=dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2.GetBulkStateRequest.FromString,
          response_serializer=dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2.GetBulkStateResponse.SerializeToString,
      ),
      'SaveState': grpc.unary_unary_rpc_method_handler(
          servicer.SaveState,
          request_deserializer=dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2.SaveStateRequest.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
      'DeleteState': grpc.unary_unary_rpc_method_handler(
          servicer.DeleteState,
          request_deserializer=dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2.DeleteStateRequest.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
      'ExecuteStateTransaction': grpc.unary_unary_rpc_method_handler(
          servicer.ExecuteStateTransaction,
          request_deserializer=dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2.ExecuteStateTransactionRequest.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
      'PublishEvent': grpc.unary_unary_rpc_method_handler(
          servicer.PublishEvent,
          request_deserializer=dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2.PublishEventRequest.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
      'InvokeBinding': grpc.unary_unary_rpc_method_handler(
          servicer.InvokeBinding,
          request_deserializer=dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2.InvokeBindingRequest.FromString,
          response_serializer=dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2.InvokeBindingResponse.SerializeToString,
      ),
      'GetSecret': grpc.unary_unary_rpc_method_handler(
          servicer.GetSecret,
          request_deserializer=dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2.GetSecretRequest.FromString,
          response_serializer=dapr_dot_proto_dot_runtime_dot_v1_dot_dapr__pb2.GetSecretResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'dapr.proto.runtime.v1.Dapr', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
