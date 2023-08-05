# automatically generated by the FlatBuffers compiler, do not modify

# namespace: MNN

import flatbuffers

class QuantizedReshape(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsQuantizedReshape(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = QuantizedReshape()
        x.Init(buf, n + offset)
        return x

    # QuantizedReshape
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # QuantizedReshape
    def Dims(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Int32Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # QuantizedReshape
    def DimsAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Int32Flags, o)
        return 0

    # QuantizedReshape
    def DimsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # QuantizedReshape
    def ModelFormat(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int8Flags, o + self._tab.Pos)
        return 0

def QuantizedReshapeStart(builder): builder.StartObject(2)
def QuantizedReshapeAddDims(builder, dims): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(dims), 0)
def QuantizedReshapeStartDimsVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def QuantizedReshapeAddModelFormat(builder, modelFormat): builder.PrependInt8Slot(1, modelFormat, 0)
def QuantizedReshapeEnd(builder): return builder.EndObject()
