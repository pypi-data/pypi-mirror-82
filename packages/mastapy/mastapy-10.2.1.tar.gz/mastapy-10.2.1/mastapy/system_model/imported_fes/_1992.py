﻿'''_1992.py

ImportedFEWithSelection
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.imported_fes import (
    _1978, _1969, _2003, _1955
)
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_WITH_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ImportedFEWithSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEWithSelection',)


class ImportedFEWithSelection(_1955.BaseFEWithSelection):
    '''ImportedFEWithSelection

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_WITH_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEWithSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def import_external_fe_mesh(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ImportExternalFEMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ImportExternalFEMesh

    @property
    def selected_nodes(self) -> 'str':
        '''str: 'SelectedNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectedNodes

    @property
    def create_element_face_group(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CreateElementFaceGroup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CreateElementFaceGroup

    @property
    def ground_selected_faces(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'GroundSelectedFaces' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.GroundSelectedFaces

    @property
    def remove_grounding_on_selected_faces(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'RemoveGroundingOnSelectedFaces' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RemoveGroundingOnSelectedFaces

    @property
    def create_condensation_node_connected_to_current_selection(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CreateCondensationNodeConnectedToCurrentSelection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CreateCondensationNodeConnectedToCurrentSelection

    @property
    def create_node_group(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CreateNodeGroup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CreateNodeGroup

    @property
    def imported_fe(self) -> '_1978.ImportedFE':
        '''ImportedFE: 'ImportedFE' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1978.ImportedFE)(self.wrapped.ImportedFE) if self.wrapped.ImportedFE else None

    @property
    def element_face_groups(self) -> 'List[_1969.ElementFaceGroupWithSelection]':
        '''List[ElementFaceGroupWithSelection]: 'ElementFaceGroups' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ElementFaceGroups, constructor.new(_1969.ElementFaceGroupWithSelection))
        return value

    @property
    def node_groups(self) -> 'List[_2003.NodeGroupWithSelection]':
        '''List[NodeGroupWithSelection]: 'NodeGroups' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.NodeGroups, constructor.new(_2003.NodeGroupWithSelection))
        return value
