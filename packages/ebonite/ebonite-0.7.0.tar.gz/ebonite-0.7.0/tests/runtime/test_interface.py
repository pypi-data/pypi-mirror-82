import pytest
from pyjackson.core import Field, Signature

import ebonite
from ebonite.core.objects import DatasetType
from ebonite.core.objects.core import Pipeline, PipelineStep
from ebonite.ext.numpy.dataset import NumpyNdarrayDatasetType
from ebonite.runtime import Interface
from ebonite.runtime.interface import expose
from ebonite.runtime.interface.base import InterfaceDescriptor, InterfaceMethodDescriptor
from ebonite.runtime.interface.pipeline import pipeline_interface


class Container(DatasetType):
    type = 'test_container'

    def __init__(self, field: int):
        self.field = field


@pytest.fixture
def interface() -> Interface:
    class MyInterface(Interface):
        @expose
        def method1(self, arg1: Container(5)) -> Container(5):
            self.method2()
            return arg1

        def method2(self):
            pass

    return MyInterface()


def test_interface_descriptor__from_interface(interface: Interface):
    d = InterfaceDescriptor.from_interface(interface)
    assert d.version == ebonite.__version__
    sig = Signature(args=[
        Field('arg1', Container(5), False)
    ], output=Field(None, Container(5), False))
    assert d.methods == [InterfaceMethodDescriptor.from_signature('method1', sig)]


def test_interface_descriptor__to_dict(interface: Interface):
    d = InterfaceDescriptor.from_interface(interface)

    assert d.to_dict() == {
        'version': ebonite.__version__,
        'methods': [{
            'name': 'method1',
            'args': {
                'arg1': {'field': 5, 'type': 'test_container'}
            },
            'out_type': {'field': 5, 'type': 'test_container'}
        }]}


@pytest.fixture
def pipeline():
    return Pipeline('Test Pipeline', [PipelineStep('a', 'b'), PipelineStep('c', 'd')], NumpyNdarrayDatasetType,
                    NumpyNdarrayDatasetType)


def test_pipeline_interface(pipeline):
    iface = pipeline_interface(pipeline)
    assert 'run' in iface.exposed_methods()
    assert iface.exposed_method_args('run')[0] == Field('data', NumpyNdarrayDatasetType, False)
    assert iface.exposed_method_returns('run') == Field(None, NumpyNdarrayDatasetType, False)
