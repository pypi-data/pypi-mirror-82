# automatically generated by the FlatBuffers compiler, do not modify

# namespace: MNN

import flatbuffers

class DetectionPostProcessParam(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsDetectionPostProcessParam(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = DetectionPostProcessParam()
        x.Init(buf, n + offset)
        return x

    # DetectionPostProcessParam
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # DetectionPostProcessParam
    def MaxDetections(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # DetectionPostProcessParam
    def MaxClassesPerDetection(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # DetectionPostProcessParam
    def DetectionsPerClass(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # DetectionPostProcessParam
    def NmsScoreThreshold(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

    # DetectionPostProcessParam
    def IouThreshold(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

    # DetectionPostProcessParam
    def NumClasses(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # DetectionPostProcessParam
    def UseRegularNMS(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # DetectionPostProcessParam
    def CenterSizeEncoding(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Float32Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # DetectionPostProcessParam
    def CenterSizeEncodingAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Float32Flags, o)
        return 0

    # DetectionPostProcessParam
    def CenterSizeEncodingLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def DetectionPostProcessParamStart(builder): builder.StartObject(8)
def DetectionPostProcessParamAddMaxDetections(builder, maxDetections): builder.PrependInt32Slot(0, maxDetections, 0)
def DetectionPostProcessParamAddMaxClassesPerDetection(builder, maxClassesPerDetection): builder.PrependInt32Slot(1, maxClassesPerDetection, 0)
def DetectionPostProcessParamAddDetectionsPerClass(builder, detectionsPerClass): builder.PrependInt32Slot(2, detectionsPerClass, 0)
def DetectionPostProcessParamAddNmsScoreThreshold(builder, nmsScoreThreshold): builder.PrependFloat32Slot(3, nmsScoreThreshold, 0.0)
def DetectionPostProcessParamAddIouThreshold(builder, iouThreshold): builder.PrependFloat32Slot(4, iouThreshold, 0.0)
def DetectionPostProcessParamAddNumClasses(builder, numClasses): builder.PrependInt32Slot(5, numClasses, 0)
def DetectionPostProcessParamAddUseRegularNMS(builder, useRegularNMS): builder.PrependBoolSlot(6, useRegularNMS, 0)
def DetectionPostProcessParamAddCenterSizeEncoding(builder, centerSizeEncoding): builder.PrependUOffsetTRelativeSlot(7, flatbuffers.number_types.UOffsetTFlags.py_type(centerSizeEncoding), 0)
def DetectionPostProcessParamStartCenterSizeEncodingVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def DetectionPostProcessParamEnd(builder): return builder.EndObject()
