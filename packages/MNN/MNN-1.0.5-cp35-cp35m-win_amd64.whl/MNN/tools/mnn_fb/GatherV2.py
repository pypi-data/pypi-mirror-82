# automatically generated by the FlatBuffers compiler, do not modify

# namespace: MNN

import flatbuffers

class GatherV2(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsGatherV2(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = GatherV2()
        x.Init(buf, n + offset)
        return x

    # GatherV2
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # GatherV2
    def Taxis(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # GatherV2
    def Tindices(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # GatherV2
    def Tparams(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

def GatherV2Start(builder): builder.StartObject(3)
def GatherV2AddTaxis(builder, Taxis): builder.PrependInt32Slot(0, Taxis, 0)
def GatherV2AddTindices(builder, Tindices): builder.PrependInt32Slot(1, Tindices, 0)
def GatherV2AddTparams(builder, Tparams): builder.PrependInt32Slot(2, Tparams, 0)
def GatherV2End(builder): return builder.EndObject()
