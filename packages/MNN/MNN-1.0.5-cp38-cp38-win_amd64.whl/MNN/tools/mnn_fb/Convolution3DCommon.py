# automatically generated by the FlatBuffers compiler, do not modify

# namespace: MNN

import flatbuffers

class Convolution3DCommon(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsConvolution3DCommon(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Convolution3DCommon()
        x.Init(buf, n + offset)
        return x

    # Convolution3DCommon
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Convolution3DCommon
    def Dilates(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Int32Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # Convolution3DCommon
    def DilatesAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Int32Flags, o)
        return 0

    # Convolution3DCommon
    def DilatesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Convolution3DCommon
    def Strides(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Int32Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # Convolution3DCommon
    def StridesAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Int32Flags, o)
        return 0

    # Convolution3DCommon
    def StridesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Convolution3DCommon
    def Kernels(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Int32Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # Convolution3DCommon
    def KernelsAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Int32Flags, o)
        return 0

    # Convolution3DCommon
    def KernelsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Convolution3DCommon
    def Pads(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Int32Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # Convolution3DCommon
    def PadsAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Int32Flags, o)
        return 0

    # Convolution3DCommon
    def PadsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Convolution3DCommon
    def PadMode(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int8Flags, o + self._tab.Pos)
        return 0

    # Convolution3DCommon
    def InputCount(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # Convolution3DCommon
    def OutputCount(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # Convolution3DCommon
    def Relu(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # Convolution3DCommon
    def Relu6(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(20))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

def Convolution3DCommonStart(builder): builder.StartObject(9)
def Convolution3DCommonAddDilates(builder, dilates): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(dilates), 0)
def Convolution3DCommonStartDilatesVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def Convolution3DCommonAddStrides(builder, strides): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(strides), 0)
def Convolution3DCommonStartStridesVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def Convolution3DCommonAddKernels(builder, kernels): builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(kernels), 0)
def Convolution3DCommonStartKernelsVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def Convolution3DCommonAddPads(builder, pads): builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(pads), 0)
def Convolution3DCommonStartPadsVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def Convolution3DCommonAddPadMode(builder, padMode): builder.PrependInt8Slot(4, padMode, 0)
def Convolution3DCommonAddInputCount(builder, inputCount): builder.PrependInt32Slot(5, inputCount, 0)
def Convolution3DCommonAddOutputCount(builder, outputCount): builder.PrependInt32Slot(6, outputCount, 0)
def Convolution3DCommonAddRelu(builder, relu): builder.PrependBoolSlot(7, relu, 0)
def Convolution3DCommonAddRelu6(builder, relu6): builder.PrependBoolSlot(8, relu6, 0)
def Convolution3DCommonEnd(builder): return builder.EndObject()
