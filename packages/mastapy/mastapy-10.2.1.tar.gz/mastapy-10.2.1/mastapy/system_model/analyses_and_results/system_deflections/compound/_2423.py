﻿'''_2423.py

ClutchHalfCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2159
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2273
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2439
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'ClutchHalfCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalfCompoundSystemDeflection',)


class ClutchHalfCompoundSystemDeflection(_2439.CouplingHalfCompoundSystemDeflection):
    '''ClutchHalfCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_HALF_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchHalfCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2159.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2159.ClutchHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2273.ClutchHalfSystemDeflection]':
        '''List[ClutchHalfSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2273.ClutchHalfSystemDeflection))
        return value

    @property
    def component_system_deflection_load_cases(self) -> 'List[_2273.ClutchHalfSystemDeflection]':
        '''List[ClutchHalfSystemDeflection]: 'ComponentSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionLoadCases, constructor.new(_2273.ClutchHalfSystemDeflection))
        return value
