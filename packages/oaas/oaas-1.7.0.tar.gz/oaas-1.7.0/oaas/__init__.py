from typing import Callable, TypeVar, Type, Optional, Dict

import oaas._registrations as registrations
from oaas.client_definition import ClientDefinitionMetadata, ClientDefinition
from oaas.client_provider import ClientMiddleware
from oaas.server_provider import ServerMiddleware
from oaas.service_definition import ServiceDefinition, ServiceDefinitionMetadata

T = TypeVar("T")


def client(
    name: str,
    namespace: str = "default",
    version: str = "1",
    tags: Dict[str, str] = None,
) -> Callable[..., Type[T]]:
    """
    Declare a service from the system. All the input and output data
    should be serializable. The serialization format depends on
    the provider being used. To get an instance to the client, call
    `get_client`.
    """

    def wrapper_builder(t: Type[T]) -> Type[T]:
        cd = ClientDefinition(
            name=name,
            namespace=namespace,
            version=version,
            code=t,
            tags=tags,
        )
        registrations.clients[t] = cd

        return t

    return wrapper_builder


def service(
    name: str,
    *,
    namespace: str = "default",
    version: str = "1",
    tags: Optional[Dict[str, str]] = None,
) -> Callable[..., Type[T]]:
    """
    Mark a service to be exposed to the system. All the input
    and output data should be serializable. The serialization
    format depends on the provider being used.
    """

    def wrapper_builder(t: Type[T]) -> Type[T]:
        sd = ServiceDefinition(
            namespace=namespace,
            name=name,
            version=version,
            code=t,
            tags=tags,
        )
        registrations.services.append(sd)

        return t

    return wrapper_builder


def serve() -> None:
    """
    Expose all the defined services using the underlying
    providers.
    """
    services_without_middleware = set()

    for service in registrations.services:
        if not _has_server_middleware(service):
            services_without_middleware.add(service)

    if services_without_middleware:
        raise Exception(
            "Some services have no backing middleware. Make sure the "
            "middleware servers are added using oaas.register_server_provider() "
            f"before calling serve(): {services_without_middleware}"
        )

    for provider in registrations.servers_middleware:
        provider.serve()


def _has_server_middleware(service) -> bool:
    for provider in registrations.servers_middleware:
        if provider.can_serve(service):
            return True

    return False


def join() -> None:
    """
    Wait for all the defined servers to come down.
    """
    for provider in registrations.servers_middleware:
        provider.join()


def get_client(t: Type[T]) -> T:
    """
    Create a client for the given type.
    """
    for provider in registrations.clients_middleware:
        if t not in registrations.clients:
            raise Exception(
                f"Type {t} was not registered using @oaas.client(). You "
                f"need to register first the client using @oaas.client() "
                f"either as oaas.client('service-name')(GrpcTypeStub) or "
                f"decorate the Simple service with @oaas.client."
            )

        client_definition = registrations.clients[t]
        if provider.can_handle(client_definition):
            return provider.create_client(client_definition)

    raise Exception(
        f"No serialization provider was registered to handle " f"{t} clients."
    )


def register_server_provider(server_middleware: ServerMiddleware):
    """
    Register a serialization provider. Normally this should be taken
    care by the middleware.
    """
    registrations.servers_middleware.add(server_middleware)


def register_client_provider(client_middleware: ClientMiddleware):
    """
    Register a serialization provider. Normally this should be taken
    care by the middleware.
    """
    registrations.clients_middleware.add(client_middleware)
