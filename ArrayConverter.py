import numpy as np

class ArrayConverter:

    @staticmethod
    def convertP(arr):

        convertArr = []
        for s in arr:
            convertArr.append(np.float32(s[0]))
            convertArr.append(np.float32(s[1]))
            convertArr.append(s[2])
            convertArr.append(s[3])
            convertArr.append(1)

        toret=np.array(convertArr,dtype=object)
        shp=np.shape(arr)
        toret=toret.reshape((shp[0],shp[1]+1))
        return toret

    @staticmethod
    def convertPO(arr):

        convertArr = []
        for s in arr:
            convertArr.append(np.float32(s[0]))
            convertArr.append(np.float32(s[1]))
            convertArr.append(s[2])
            convertArr.append(s[3])
            convertArr.append(s[4])

        toret = np.array(convertArr, dtype=object)
        toret = toret.reshape(np.shape(arr))
        return toret