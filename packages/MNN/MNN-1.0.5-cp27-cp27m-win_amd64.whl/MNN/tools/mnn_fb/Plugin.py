# automatically generated by the FlatBuffers compiler, do not modify

# namespace: MNN

import flatbuffers

class Plugin(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsPlugin(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Plugin()
        x.Init(buf, n + offset)
        return x

    # Plugin
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Plugin
    def Type(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # Plugin
    def Attr(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from .Attribute import Attribute
            obj = Attribute()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Plugin
    def AttrLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def PluginStart(builder): builder.StartObject(2)
def PluginAddType(builder, type): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(type), 0)
def PluginAddAttr(builder, attr): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(attr), 0)
def PluginStartAttrVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def PluginEnd(builder): return builder.EndObject()
