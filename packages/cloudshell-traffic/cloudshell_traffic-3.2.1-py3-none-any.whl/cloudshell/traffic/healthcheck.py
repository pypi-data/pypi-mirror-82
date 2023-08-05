import logging
from typing import Optional, Union

from cloudshell.api.cloudshell_api import CloudShellAPISession, InputNameValue, ServiceInstance
from cloudshell.logging.qs_logger import get_qs_logger
from cloudshell.shell.core.driver_context import ResourceCommandContext
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext
from cloudshell.workflow.orchestration.sandbox import Sandbox

from .helpers import get_reservation_id, get_reservation_description

ACS_MODEL = 'Acs'
CABLE_MODEM_MODEL = 'Cable_Modem'
CPE_MODEL = 'Cpe'
CNR_MODEL = 'Cnr'
HEALTHCHECK_STATUS = 'Healthcheck_Status'
JIRA_MODEL = 'Jira'
REDIRECT_DB_MODEL = 'Redirect_DB'
RESOURCE_PROVIDER_MODEL = 'Resource_Provider'


def get_health_check_service(context: Union[ResourceCommandContext, Sandbox], object_name: str,
                             status_selector: Optional[str] = 'none') -> ServiceInstance:
    """ Set the live status attribute for a healthcheck status service connected to an object (resource of service).

    :param context: Resource command context.
    :param object_name: The object that the healthcheck service is connected to.
    :param status_selector: Selects the requested healthcheck status service in case multiple services are connected
        to the resource.
    """
    description = get_reservation_description(context)
    resource_connectors = [c for c in description.Connectors if object_name in [c.Source, c.Target]]
    for connector in resource_connectors:
        other_end_name = connector.Target if connector.Source == object_name else connector.Source
        other_end_services = [s for s in description.Services if s.Alias == other_end_name]
        if other_end_services:
            other_end_service = other_end_services[0]
            if other_end_service.ServiceName == HEALTHCHECK_STATUS:
                a_name = 'Healthcheck_Status.status_selector'
                hc_service_selector = [a for a in other_end_service.Attributes if a.Name == a_name][0].Value
                if hc_service_selector == status_selector:
                    return other_end_service


def set_health_check_live_status(context: ResourceCommandContext, object_name: str, status: bool,
                                 status_selector: Optional[str] = 'none') -> ServiceInstance:
    """ Set the live status attribute for a healthcheck status service connected to an object (resource of service).

    :param context: Resource command context.
    :param object_name: The object that the healthcheck service is connected to.
    :param status: True will set the live status to Online, False will set the live status to Error.
    :param status_selector: Selects the requested healthcheck status service in case multiple services are connected
        to the resource.
    """
    hc_service = get_health_check_service(context, object_name, status_selector)
    if hc_service:
        cs_session = CloudShellAPISession(host=context.connectivity.server_address,
                                          token_id=context.connectivity.admin_auth_token,
                                          domain=context.reservation.domain)
        cs_session.ExecuteCommand(get_reservation_id(context), hc_service.Alias, 'Service',
                                  'set_live_status',
                                  [InputNameValue('status', 'Online' if status else 'Error')])
    return hc_service


class HealthCheckDriver(ResourceDriverInterface):
    """ Base class for all Health Check resource drivers. """

    def initialize(self, context, resource, log_group='healthcheck_shells', packages_loggers=None):

        super().initialize(context)

        self.resource = resource
        self.service = resource

        self.logger = get_qs_logger(log_group=log_group, log_file_prefix=context.resource.name)
        self.logger.setLevel(logging.DEBUG)

        for package_logger in packages_loggers or ['pycmts', 'pycnr', 'pylgi']:
            package_logger = logging.getLogger(package_logger)
            package_logger.setLevel(self.logger.level)
            for handler in self.logger.handlers:
                if handler not in package_logger.handlers:
                    package_logger.addHandler(handler)

        self.get_connection_details(context)

    def cleanup(self):
        pass

    def get_connection_details(self, context):
        self.address = context.resource.address
        self.logger.debug(f'Address - {self.address}')
        self.user = self.resource.user
        self.logger.debug(f'User - {self.user}')
        self.logger.debug(f'Encrypted password - {self.resource.password}')
        self.password = CloudShellSessionContext(context).get_api().DecryptPassword(self.resource.password).Value
        self.logger.debug(f'Password - {self.password}')

    @property
    def clean_report(self):
        report = {}
        report['name'] = ''
        report['result'] = False
        report['status'] = ''
        report['summary'] = {}
        report['log'] = {}
        return report
