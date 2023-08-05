# automatically generated by the FlatBuffers compiler, do not modify

# namespace: MNN

import flatbuffers

class Scale(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsScale(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Scale()
        x.Init(buf, n + offset)
        return x

    # Scale
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Scale
    def Channels(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # Scale
    def ScaleData(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Float32Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # Scale
    def ScaleDataAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Float32Flags, o)
        return 0

    # Scale
    def ScaleDataLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Scale
    def BiasData(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Float32Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # Scale
    def BiasDataAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Float32Flags, o)
        return 0

    # Scale
    def BiasDataLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def ScaleStart(builder): builder.StartObject(3)
def ScaleAddChannels(builder, channels): builder.PrependInt32Slot(0, channels, 0)
def ScaleAddScaleData(builder, scaleData): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(scaleData), 0)
def ScaleStartScaleDataVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def ScaleAddBiasData(builder, biasData): builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(biasData), 0)
def ScaleStartBiasDataVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def ScaleEnd(builder): return builder.EndObject()
