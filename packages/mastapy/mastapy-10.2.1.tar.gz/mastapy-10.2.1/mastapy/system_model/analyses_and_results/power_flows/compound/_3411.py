﻿'''_3411.py

CoaxialConnectionCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1875
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3286
from mastapy.system_model.analyses_and_results.power_flows.compound import _3478
from mastapy._internal.python_net import python_net_import

_COAXIAL_CONNECTION_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'CoaxialConnectionCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('CoaxialConnectionCompoundPowerFlow',)


class CoaxialConnectionCompoundPowerFlow(_3478.ShaftToMountableComponentConnectionCompoundPowerFlow):
    '''CoaxialConnectionCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _COAXIAL_CONNECTION_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CoaxialConnectionCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1875.CoaxialConnection':
        '''CoaxialConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1875.CoaxialConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1875.CoaxialConnection':
        '''CoaxialConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1875.CoaxialConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3286.CoaxialConnectionPowerFlow]':
        '''List[CoaxialConnectionPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3286.CoaxialConnectionPowerFlow))
        return value

    @property
    def connection_power_flow_load_cases(self) -> 'List[_3286.CoaxialConnectionPowerFlow]':
        '''List[CoaxialConnectionPowerFlow]: 'ConnectionPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionPowerFlowLoadCases, constructor.new(_3286.CoaxialConnectionPowerFlow))
        return value
