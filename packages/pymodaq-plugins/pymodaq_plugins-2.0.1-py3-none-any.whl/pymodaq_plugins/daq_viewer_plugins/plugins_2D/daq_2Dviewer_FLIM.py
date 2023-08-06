from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSlot, QObject, pyqtSignal
import numpy as np
import os
from easydict import EasyDict as edict
import ctypes
from collections import OrderedDict
from pymodaq.daq_utils.daq_utils import ThreadCommand, getLineInfo, ScanParameters, zeros_aligned, extract_TTTR_histo_every_pixels

from pyqtgraph.parametertree import Parameter, ParameterTree
import pyqtgraph.parametertree.parameterTypes as pTypes
import pymodaq.daq_utils.custom_parameter_tree as custom_tree

from pymodaq_plugins.hardware.piezoconcept.piezoconcept import PiezoConcept, Position, Time
from pymodaq_plugins.daq_viewer_plugins.plugins_1D.daq_1Dviewer_TH260 import DAQ_1DViewer_TH260, T3Reader
import time

# find available COM ports
import serial.tools.list_ports

ports = [str(port)[0:4] for port in list(serial.tools.list_ports.comports())]
port = 'COM6' if 'COM6' in ports else ports[0] if len(ports) > 0 else ''

stage_params = [{'title': 'Stage Settings:', 'name': 'stage_settings', 'type': 'group', 'expanded': True, 'children': [
                    {'title': 'Show Navigator:', 'name': 'show_navigator', 'type': 'bool', 'value': False},
                    {'title': 'Stage Type:', 'name': 'stage_type', 'type': 'list', 'value': 'PiezoConcept', 'values': ['PiezoConcept']},
                    {'title': 'Controller Info:', 'name': 'controller_id', 'type': 'text', 'value': '', 'readonly': True},
                    {'title': 'COM Port:', 'name': 'com_port', 'type': 'list', 'values': ports, 'value': port},
                    {'title': 'Time interval (ms):', 'name': 'time_interval', 'type': 'int', 'value': 20},
                    {'title': 'Stage X:', 'name': 'stage_x', 'type': 'group', 'expanded': True, 'children': [
                        {'title': 'Axis:', 'name': 'stage_x_axis', 'type': 'list', 'value': 'Y', 'values': ['X', 'Y']},
                        {'title': 'Direction:', 'name': 'stage_x_direction', 'type': 'list', 'value': 'Inverted', 'values': ['Normal', 'Inverted']},
                        {'title': 'Offset (µm):', 'name': 'offset_x', 'type': 'float', 'value': 100},
                        ]},
                    {'title': 'Stage Y:', 'name': 'stage_y', 'type': 'group', 'expanded': True, 'children': [
                         {'title': 'Axis:', 'name': 'stage_y_axis', 'type': 'list', 'value': 'X', 'values': ['X', 'Y']},
                         {'title': 'Direction:', 'name': 'stage_y_direction', 'type': 'list', 'value': 'Normal', 'values': ['Normal', 'Inverted']},
                         {'title': 'Offset (µm):', 'name': 'offset_y', 'type': 'float', 'value': 100},
                        ]},

                    ]}]

class DAQ_2DViewer_FLIM(DAQ_1DViewer_TH260):
    """
        ==================== ==================
        **Atrributes**        **Type**
        *params*              dictionnary list
        *hardware_averaging*  boolean
        *x_axis*              1D numpy array      
        *ind_data*            int
        ==================== ==================

        See Also
        --------

        utility_classes.DAQ_Viewer_base
    """
    params = DAQ_1DViewer_TH260.params + stage_params
    stop_scanner = pyqtSignal()
    start_tttr_scan = pyqtSignal()

    def __init__(self, parent=None, params_state=None):

        super(DAQ_2DViewer_FLIM, self).__init__(parent, params_state) #initialize base class with commom attributes and methods
        self.settings.child('acquisition', 'acq_type').setOpts(limits=['Counting', 'Histo', 'T3', 'FLIM'])
        self.settings.child('acquisition', 'acq_type').setValue('Histo')

        self.stage = None
        self.scan_parameters = None
        self.x_axis = None
        self.y_axis = None
        self.Nx = 1
        self.Ny = 1
        self.signal_axis = None

    def commit_settings(self, param):

        if param.name() not in custom_tree.iter_children(self.settings.child(('stage_settings'))):
            super(DAQ_2DViewer_FLIM, self).commit_settings(param)

        else:
            if param.name() == 'time_interval':
                self.stage._get_read()
                self.stage.set_time_interval(Time(param.value(),
                                                  unit='m'))  # set time interval between pixels

            elif param.name() == 'show_navigator':
                self.emit_status(ThreadCommand('show_navigator'))
                param.setValue(False)

    def emit_data(self):
        """
        """
        try:
            mode = self.settings.child('acquisition', 'acq_type').value()
            if mode == 'Counting' or mode == 'Histo' or mode == 'T3':
                super(DAQ_2DViewer_FLIM, self).emit_data()

            elif mode == 'FLIM':
                self.stop_scanner.emit()
                self.data_grabed_signal.emit([OrderedDict(name='TH260', data=self.datas, type='DataND', nav_axes=(0, 1),
                                                          nav_x_axis=self.get_nav_xaxis(),
                                                          nav_y_axis=self.get_nav_yaxis(),
                                                          xaxis=self.get_xaxis())])
                self.stop()

        except Exception as e:
            self.emit_status(ThreadCommand('Update_Status', [getLineInfo() + str(e), 'log']))

    def emit_data_tmp(self):
        """
        """
        try:
            mode = self.settings.child('acquisition', 'acq_type').value()
            if mode == 'Counting' or mode == 'Histo' or mode == 'T3':
                super(DAQ_2DViewer_FLIM, self).emit_data_tmp()

            elif mode == 'FLIM':

                self.data_grabed_signal_temp.emit([OrderedDict(name='TH260', data=self.datas, type='DataND', nav_axes=(0, 1),
                                                          nav_x_axis=self.get_nav_xaxis(),
                                                          nav_y_axis=self.get_nav_yaxis(),
                                                          xaxis=self.get_xaxis())])

        except Exception as e:
            self.emit_status(ThreadCommand('Update_Status', [getLineInfo() + str(e), 'log']))


    def process_histo_from_h5(self, Nx=1, Ny=1, channel=0, marker=65):
        mode = self.settings.child('acquisition', 'acq_type').value()
        if mode == 'Counting' or mode == 'Histo' or mode == 'T3':
            datas = super(DAQ_2DViewer_FLIM, self).process_histo_from_h5(Nx, Ny, channel)
            return datas
        else:
            markers_array = self.h5file.get_node('/markers')
            ind_lines = np.squeeze(np.where(self.h5file.get_node('/markers')[self.ind_reading:] == marker))
            if ind_lines.size == 0:
                return np.zeros_like(self.datas)  # basically do nothing
            else:
                ind_last_line = ind_lines[-1]
            print(self.ind_reading, ind_last_line)
            markers = markers_array[self.ind_reading:self.ind_reading+ind_last_line]
            nanotimes = self.h5file.get_node('/nanotimes')[self.ind_reading:self.ind_reading+ind_last_line]

            nbins = self.settings.child('acquisition', 'timings', 'nbins').value()
            datas = extract_TTTR_histo_every_pixels(nanotimes, markers, marker=marker, Nx=Nx, Ny=Ny,
                                            Ntime=nbins, ind_line_offset=self.ind_reading, channel=channel)
            self.ind_reading = ind_last_line
            return datas

    def ini_detector(self, controller=None):
        """
            See Also
            --------
            DAQ_utils.ThreadCommand, hardware1D.DAQ_1DViewer_Picoscope.update_pico_settings
        """
        self.status.update(edict(initialized=False, info="", x_axis=None, y_axis=None, controller=None))
        try:
            self.status = super(DAQ_2DViewer_FLIM, self).ini_detector(controller)

            self.ini_stage()
            self.status.x_axis = self.x_axis
            self.status.initialized = True
            self.status.controller = self.controller

            return self.status

        except Exception as e:
            self.status.info = getLineInfo() + str(e)
            self.status.initialized = False
            return self.status

    @pyqtSlot(ScanParameters)
    def update_scanner(self, scan_parameters):
        self.scan_parameters = scan_parameters
        self.x_axis = self.scan_parameters.axis_2D_1
        self.Nx = self.x_axis.size
        self.y_axis = self.scan_parameters.axis_2D_2
        self.Ny = self.y_axis.size




    def get_nav_xaxis(self):
        """
        """
        return self.scan_parameters.axis_2D_1

    def get_nav_yaxis(self):
        """
        """
        return self.scan_parameters.axis_2D_2

    def ini_stage(self):
        if self.settings.child('stage_settings', 'stage_type').value() == 'PiezoConcept':
            self.stage = PiezoConcept()
            self.controller.stage = self.stage
            self.stage.init_communication(self.settings.child('stage_settings', 'com_port').value())

            controller_id = self.stage.get_controller_infos()
            self.settings.child('stage_settings', 'controller_id').setValue(controller_id)
            self.stage.set_time_interval(Time(self.settings.child('stage_settings', 'time_interval').value(), unit='m'))  #set time interval between pixels
            #set the TTL outputs for each displacement of first axis
            self.stage.set_TTL_state(1, self.settings.child('stage_settings', 'stage_x', 'stage_x_axis').value(),
                                     'output', dict(type='start'))

            self.move_abs(0, 'X')
            self.move_abs(0, 'Y')

    @pyqtSlot(float, float)
    def move_at_navigator(self, posx, posy):
        self.move_abs(posx, 'X')
        self.move_abs(posy, 'Y')

    def move_abs(self, position, axis='X'):
        offset = self.settings.child('stage_settings', 'stage_x', 'offset_x').value()
        if self.settings.child('stage_settings', 'stage_x', 'stage_x_direction').value() == 'Normal':
            posi = position + offset
        else:
            posi = -position + offset
        if axis == 'X':
            ax = self.settings.child('stage_settings', 'stage_x', 'stage_x_axis').value()
        else:
            ax = self.settings.child('stage_settings', 'stage_y', 'stage_y_axis').value()
        pos = Position(ax, int(posi * 1000), unit='n')
        out = self.stage.move_axis('ABS', pos)

    def close(self):
        """

        """
        super(DAQ_2DViewer_FLIM, self).close()
        self.stage.close_communication()

    def set_acq_mode(self, mode='FLIM', update=False):
        """
        herited method

        Change the acquisition mode (histogram for mode=='Counting' and 'Histo' or T3 for mode == 'FLIM')
        Parameters
        ----------
        mode

        Returns
        -------

        """


        # check enabled channels
        labels = [k for k in self.channels_enabled.keys() if self.channels_enabled[k]['enabled']]
        N = len(labels)

        if mode != self.actual_mode or update:
            if mode == 'Counting' or mode == 'Histo' or mode == 'T3':
                super(DAQ_2DViewer_FLIM, self).set_acq_mode(mode, update)

            elif mode == 'FLIM':

                self.emit_status(ThreadCommand('show_scanner'))
                QtWidgets.QApplication.processEvents()
                self.emit_status(ThreadCommand('show_navigator'))

                self.controller.TH260_Initialize(self.device, mode=3)  # mode T3
                self.controller.TH260_SetMarkerEnable(self.device, 1)
                self.datas = np.zeros((10, 10, 1024))
                self.data_grabed_signal_temp.emit([OrderedDict(name='TH260', data=self.datas, nav_axes=[0, 1], type='DataND')])

                self.data_pointers = self.datas.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
                self.actual_mode = mode

            self.actual_mode = mode

    def grab_data(self, Naverage=1, **kwargs):
        """
            Start new acquisition in two steps :
                * Initialize data: self.datas for the memory to store new data and self.data_average to store the average data
                * Start acquisition with the given exposure in ms, in "1d" or "2d" mode

            =============== =========== =============================
            **Parameters**   **Type**    **Description**
            Naverage         int         Number of images to average
            =============== =========== =============================

            See Also
            --------
            DAQ_utils.ThreadCommand
        """
        try:
            self.acq_done = False
            mode = self.settings.child('acquisition', 'acq_type').value()
            if mode == 'Counting' or mode == 'Histo' or mode == 'T3':
                super(DAQ_2DViewer_FLIM, self).grab_data(Naverage, **kwargs)

            elif mode == 'FLIM':
                self.ind_reading = 0
                self.do_process_tttr = False

                self.init_h5file()
                self.datas = np.zeros((self.Nx, self.Ny, self.settings.child('acquisition', 'timings', 'nbins').value(),),
                                       dtype=np.float64)
                self.init_histo_group()

                time_acq = int(self.settings.child('acquisition', 'acq_time').value() * 1000)  # in ms
                self.general_timer.stop()

                self.prepare_moves()

                # prepare asynchronous tttr time event reading
                t3_reader = T3Reader_scan(self.device, self.controller, time_acq, self.stage, self.Nchannels)
                self.detector_thread = QThread()
                t3_reader.moveToThread(self.detector_thread)
                t3_reader.data_signal[dict].connect(self.populate_h5)
                self.stop_tttr.connect(t3_reader.stop_TTTR)
                self.start_tttr_scan.connect(t3_reader.start_TTTR)
                self.detector_thread.t3_reader = t3_reader
                self.detector_thread.start()
                self.detector_thread.setPriority(QThread.HighestPriority)



                #start acquisition and scanner
                self.time_t3 = time.perf_counter()
                self.time_t3_rate = time.perf_counter()

                self.start_tttr_scan.emit()



        except Exception as e:
            self.emit_status(ThreadCommand('Update_Status', [getLineInfo() + str(e), "log"]))

    def init_histo_group(self):

        mode = self.settings.child('acquisition', 'acq_type').value()
        if mode == 'Counting' or mode == 'Histo' or mode == 'T3':
            super(DAQ_2DViewer_FLIM, self).init_histo_group()
        else:

            histo_group = self.h5file.create_group(self.h5file.root, 'histograms')
            self.histo_array = self.h5file.create_carray(histo_group, 'histogram', obj=self.datas,
                                                         title='histogram')
            x_axis = self.get_xaxis()
            xarray = self.h5file.create_carray(histo_group, "x_axis", obj=x_axis['data'], title='x_axis')
            xarray.attrs['shape'] = xarray.shape
            xarray.attrs['type'] = 'signal_axis'
            xarray.attrs['data_type'] = '1D'

            navxarray = self.h5file.create_carray(self.h5file.root, 'scan_x_axis_unique', obj=self.get_nav_xaxis(),
                                                  title='data')
            navxarray.set_attr('shape', navxarray.shape)
            navxarray.attrs['type'] = 'navigation_axis'
            navxarray.attrs['data_type'] = '1D'

            navyarray = self.h5file.create_carray(self.h5file.root, 'scan_y_axis_unique', obj=self.get_nav_yaxis(),
                                                  title='data')
            navyarray.set_attr('shape', navyarray.shape)
            navyarray.attrs['type'] = 'navigation_axis'
            navyarray.attrs['data_type'] = '1D'

            self.histo_array._v_attrs['data_type'] = '1D'
            self.histo_array._v_attrs['type'] = 'histo_data'
            self.histo_array._v_attrs['shape'] = self.datas.shape
            self.histo_array._v_attrs['scan_type'] = 'Scan2D'

    def prepare_moves(self):
        """
        prepare given actuators with positions from scan_parameters
        Returns
        -------

        """
        self.x_axis = self.scan_parameters.axis_2D_1
        self.Nx = self.x_axis.size
        self.y_axis = self.scan_parameters.axis_2D_2
        self.Ny = self.y_axis.size
        positions_real = self.transform_scan_coord(self.scan_parameters.positions)
        # interval_time = self.settings.child('stage_settings', 'time_interval').value()/1000
        # total_time = self.settings.child('acquisition', 'acq_time').value()
        # Ncycles = int(total_time/(interval_time*len(positions_real)))
        # total_time = Ncycles * interval_time*len(positions_real)
        # self.settings.child('acquisition', 'acq_time').setValue(total_time)
        # positions = []
        # for ind in range(Ncycles):
        #     positions.extend(positions_real)

        self.stage.set_positions_arbitrary(positions_real)

        self.move_at_navigator(*self.scan_parameters.positions[0][0:2])

    def transform_scan_coord(self, positions):

        offset = self.settings.child('stage_settings', 'stage_x', 'offset_x').value()
        if self.settings.child('stage_settings', 'stage_x', 'stage_x_direction').value() == 'Normal':
            scaling_x = 1
        else:
            scaling_x = -1

        if self.settings.child('stage_settings', 'stage_y', 'stage_y_direction').value() == 'Normal':
            scaling_y = 1
        else:
            scaling_y = -1
        if self.settings.child('stage_settings', 'stage_x', 'stage_x_axis').value() == 'X':
            ind_x = 0
        else:
            ind_x = 1

        if self.settings.child('stage_settings', 'stage_y', 'stage_y_axis').value() == 'Y':
            ind_y = 1
        else:
            ind_y = 0

        positions_out = []
        for pos in positions:
            pos_tmp = [(scaling_x*pos[ind_x]+offset)*1000, (scaling_y*pos[ind_y]+offset)*1000]
            positions_out.append(pos_tmp)

        return positions_out


    def stop(self):
        super(DAQ_2DViewer_FLIM, self).stop()
        self.stop_scanner.emit()
        try:
            self.move_at_navigator(*self.scan_parameters.positions[0][0:2])
        except:
            pass

class T3Reader_scan(T3Reader):

    def __init__(self, device, controller, time_acq, stage, Nchannels=2):
        super(T3Reader_scan, self).__init__(device, controller, time_acq, Nchannels)
        self.stage = stage

    def start_TTTR(self):

        self.controller.TH260_StartMeas(self.device, self.time_acq)
        self.stage.run_arbitrary()

        while not self.acquisition_stoped:
            if 'FIFOFULL' in self.controller.TH260_GetFlags(self.device):
                print("\nFiFo Overrun!")
                #self.stop_TTTR()

            if 'Completed' in self.stage._get_read():
                self.stage.run_arbitrary()

            rates = self.get_rates()
            elapsed_time = self.controller.TH260_GetElapsedMeasTime(self.device)  # in ms

            nrecords = self.controller.TH260_ReadFiFo(self.device, self.buffer.size, self.data_ptr)

            if nrecords > 0:
                # We could just iterate through our buffer with a for loop, however,
                # this is slow and might cause a FIFO overrun. So instead, we shrinken
                # the buffer to its appropriate length with array slicing, which gives
                # us a python list. This list then needs to be converted back into
                # a ctype array which can be written at once to the output file
                self.data_signal.emit(dict(data=self.buffer[0:nrecords], rates=rates, elapsed_time=elapsed_time, acquisition_done=False))
            else:

                if self.controller.TH260_CTCStatus(self.device):
                    print("\nDone")
                    self.stop_TTTR()
                    self.data_signal.emit(dict(data=[], rates=rates, elapsed_time=elapsed_time, acquisition_done=True))
            # within this loop you can also read the count rates if needed.


