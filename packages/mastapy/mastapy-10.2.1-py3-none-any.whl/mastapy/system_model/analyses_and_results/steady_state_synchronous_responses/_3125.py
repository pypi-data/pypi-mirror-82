﻿'''_3125.py

TorqueConverterConnectionSteadyStateSynchronousResponse
'''


from mastapy.system_model.connections_and_sockets.couplings import _1946
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6251
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3047
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'TorqueConverterConnectionSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterConnectionSteadyStateSynchronousResponse',)


class TorqueConverterConnectionSteadyStateSynchronousResponse(_3047.CouplingConnectionSteadyStateSynchronousResponse):
    '''TorqueConverterConnectionSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterConnectionSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1946.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1946.TorqueConverterConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6251.TorqueConverterConnectionLoadCase':
        '''TorqueConverterConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6251.TorqueConverterConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
