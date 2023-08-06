﻿'''_3878.py

SynchroniserModalAnalysesAtStiffnesses
'''


from mastapy.system_model.part_model.couplings import _2180
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6246
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3862
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'SynchroniserModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserModalAnalysesAtStiffnesses',)


class SynchroniserModalAnalysesAtStiffnesses(_3862.SpecialisedAssemblyModalAnalysesAtStiffnesses):
    '''SynchroniserModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2180.Synchroniser':
        '''Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2180.Synchroniser)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6246.SynchroniserLoadCase':
        '''SynchroniserLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6246.SynchroniserLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
