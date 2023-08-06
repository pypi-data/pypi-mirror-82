# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import BinaryIO

from azure.ml.component._restclients.service_caller_factory import _DesignerServiceCallerFactory


class ComponentAPICaller:
    """Implementation for CRUD operations for component.

    Actual operations are implemented via auto generated rest clients.
    # TODO: replace this class with auto generated CRUD implementation.
    """

    def __init__(self, workspace, from_cli=False):
        self._workspace = workspace
        self.service_caller = _DesignerServiceCallerFactory.get_instance(workspace, from_cli)

    def register(self, component_source_type: str, yaml_file: str = None,
                 snapshot_source_zip_file: BinaryIO = None, devops_artifacts_zip_url: str = None,
                 validate_only: bool = False, anonymous_registration: bool = True, set_as_default: bool = False,
                 version: str = None):
        result = self.service_caller.register_module(
            anonymous_registration=anonymous_registration,
            validate_only=validate_only,
            module_source_type=component_source_type, yaml_file=yaml_file,
            snapshot_source_zip_file=snapshot_source_zip_file,
            devops_artifacts_zip_url=devops_artifacts_zip_url,
            set_as_default=set_as_default,
            overwrite_module_version=version
        )
        return result

    def parse(self, component_source_type: str, yaml_file: str = None,
              snapshot_source_zip_file: BinaryIO = None, devops_artifacts_zip_url: str = None):
        result = self.service_caller.parse_module(
            module_source_type=component_source_type,
            yaml_file=yaml_file,
            snapshot_source_zip_file=snapshot_source_zip_file,
            devops_artifacts_zip_url=devops_artifacts_zip_url
        )
        return result

    def list(self, include_disabled: bool, continuation_header: dict):
        result = self.service_caller.list_modules(
            active_only=not include_disabled,
            continuation_header=continuation_header
        )
        return result

    def get(self, name, namespace, version=None):
        result = self.service_caller.get_module(
            module_name=name,
            module_namespace=namespace,
            version=version
        )
        return result

    def enable(self, name, namespace):
        body = {'ModuleUpdateOperationType': 'EnableModule'}
        return self.update(name, namespace, body)

    def disable(self, name, namespace):
        body = {'ModuleUpdateOperationType': 'DisableModule'}
        return self.update(name, namespace, body)

    def set_default_version(self, name, namespace, version):
        body = {'ModuleUpdateOperationType': 'SetDefaultVersion', 'ModuleVersion': version}
        return self.update(name, namespace, body)

    def update(self, name, namespace, body):
        result = self.service_caller.update_module(
            module_name=name,
            module_namespace=namespace,
            body=body
        )
        # The PATCH api will not return full data of the updated module,
        # so we do a GET operation here.
        result = self.service_caller.get_module(
            module_name=result.module_name,
            module_namespace=result.namespace,
        )
        return result

    def get_module_yaml(self, name, namespace, version):
        result = self.service_caller.get_module_yaml(module_namespace=namespace, module_name=name, version=version)
        return result

    def get_snapshot_url(self, name, namespace, version):
        snapshot_url = self.service_caller.get_module_snapshot_url(module_namespace=namespace, module_name=name,
                                                                   version=version)
        return snapshot_url

    def get_snapshot_url_by_id(self, component_id):
        snapshot_url = self.service_caller.get_module_snapshot_url_by_id(module_id=component_id)
        return snapshot_url
