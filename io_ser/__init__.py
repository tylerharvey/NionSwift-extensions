"""
    Support for TIA ser file I/O. Adapted from TIFFIO by Tyler Harvey (trh).
"""

# standard libraries
import gettext
import warnings

# third party libraries
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from io_ser import serReader
import numpy

# local libraries
# None


_ = gettext.gettext


class serIODelegate(object):

    def __init__(self, api):
        self.__api = api
        self.io_handler_id = "ser-io-handler"
        self.io_handler_name = _("ser Files")
        self.io_handler_extensions = ["ser"]

    def read_data_and_metadata(self, extension, file_path):
        serFile = serReader.serReader(file_path)
        # for 2d image data
        if 'imageData' in serFile:
            # serReader uses x,y,z axes; Swift uses z,y,x
            data = serFile['imageData'].transpose()
            pixel_size_x = serFile['pixelSizeX']
            pixel_size_y = serFile['pixelSizeY']
            offset_x = serFile['offsetX']
            offset_y = serFile['offsetY']
            # very basic readout of units
            unit = '{0:2.2e} '.format(serFile['scanCalibration'][1,0])+serFile['scanUnit']
            xcal = self.__api.create_calibration(scale=pixel_size_x,units=unit,offset=offset_x)
            ycal = self.__api.create_calibration(scale=pixel_size_y,units=unit,offset=offset_y)
            zcal = self.__api.create_calibration(scale=1)
            # borrowed this from TIFFIO
            # if data.dtype == numpy.uint8 and data.shape[-1] == 3 and len(data.shape) > 1:
            #     data = data[:,:,(2, 1, 0)]
            # if data.dtype == numpy.uint8 and data.shape[-1] == 4 and len(data.shape) > 1:
            #     data = data[:,:,(2, 1, 0, 3)]
        return self.__api.create_data_and_metadata_from_data(data,dimensional_calibrations=(zcal,ycal,xcal))
        if 'spectra' in serFile:
            spectra = serFile['spectra']
            E_start = serFile['startE']
            pixel_size_E = serFile['eDelta']
            unit = '{0:2.2e} '.format(serFile['scanCalibration'][1,0])+serFile['scanUnit']
            Ecal = self.__api.create_calibration(scale=pixel_size_E,units=unit,offset=E_start)
            zcal = self.__api.create_calibration(scale=1)
        return self.__api.create_data_and_metadata_from_data(spectra,dimensional_calibrations=(zcal,Ecal))

    def can_write_data_and_metadata(self, data_and_metadata, extension):
        raise NotImplementedError
        return data_and_metadata.is_data_2d

    def write_data_and_metadata(self, data_and_metadata, file_path, extension):
        raise NotImplementedError
        data = data_and_metadata.data
        if data is not None:
            if data.dtype == numpy.uint8 and data.shape[-1] == 3 and len(data.shape) > 1:
                data = data[:,:,(2, 1, 0)]
            if data.dtype == numpy.uint8 and data.shape[-1] == 4 and len(data.shape) > 1:
                data = data[:,:,(2, 1, 0, 3)]
            # save function should go here
            # serWriter.imsave(file_path, data)
            pass 


class serIOExtension(object):

    # required for Swift to recognize this as an extension class.
    extension_id = "nion.swift.extensions.ser_io"

    def __init__(self, api_broker):
        # grab the api object.
        api = api_broker.get_api(version="1", ui_version="1")
        # be sure to keep a reference or it will be closed immediately.
        self.__io_handler_ref = api.create_data_and_metadata_io_handler(serIODelegate(api))

    def close(self):
        # close will be called when the extension is unloaded. in turn, close any references so they get closed. this
        # is not strictly necessary since the references will be deleted naturally when this object is deleted.
        self.__io_handler_ref.close()
        self.__io_handler_ref = None

