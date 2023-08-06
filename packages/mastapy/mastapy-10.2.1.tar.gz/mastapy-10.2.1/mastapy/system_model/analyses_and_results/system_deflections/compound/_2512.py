﻿'''_2512.py

SynchroniserSleeveCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2184
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2374
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2511
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_SLEEVE_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'SynchroniserSleeveCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserSleeveCompoundSystemDeflection',)


class SynchroniserSleeveCompoundSystemDeflection(_2511.SynchroniserPartCompoundSystemDeflection):
    '''SynchroniserSleeveCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_SLEEVE_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserSleeveCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2184.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2184.SynchroniserSleeve)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2374.SynchroniserSleeveSystemDeflection]':
        '''List[SynchroniserSleeveSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2374.SynchroniserSleeveSystemDeflection))
        return value

    @property
    def component_system_deflection_load_cases(self) -> 'List[_2374.SynchroniserSleeveSystemDeflection]':
        '''List[SynchroniserSleeveSystemDeflection]: 'ComponentSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionLoadCases, constructor.new(_2374.SynchroniserSleeveSystemDeflection))
        return value
