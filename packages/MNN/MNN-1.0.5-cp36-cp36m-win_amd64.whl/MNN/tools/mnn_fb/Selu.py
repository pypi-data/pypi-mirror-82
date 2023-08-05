# automatically generated by the FlatBuffers compiler, do not modify

# namespace: MNN

import flatbuffers

class Selu(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsSelu(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Selu()
        x.Init(buf, n + offset)
        return x

    # Selu
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Selu
    def Scale(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

    # Selu
    def Alpha(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

def SeluStart(builder): builder.StartObject(2)
def SeluAddScale(builder, scale): builder.PrependFloat32Slot(0, scale, 0.0)
def SeluAddAlpha(builder, alpha): builder.PrependFloat32Slot(1, alpha, 0.0)
def SeluEnd(builder): return builder.EndObject()
