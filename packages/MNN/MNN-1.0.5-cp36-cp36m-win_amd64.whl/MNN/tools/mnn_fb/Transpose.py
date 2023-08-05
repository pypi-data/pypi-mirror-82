# automatically generated by the FlatBuffers compiler, do not modify

# namespace: MNN

import flatbuffers

class Transpose(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsTranspose(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Transpose()
        x.Init(buf, n + offset)
        return x

    # Transpose
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Transpose
    def Tperm(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

def TransposeStart(builder): builder.StartObject(1)
def TransposeAddTperm(builder, Tperm): builder.PrependInt32Slot(0, Tperm, 0)
def TransposeEnd(builder): return builder.EndObject()
