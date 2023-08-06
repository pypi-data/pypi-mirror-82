#!/usr/bin/python
import pandas as pd
import numpy as np
from numpy.linalg import svd
from os import path, listdir, stat, remove
from math import log2
from . import image_analysis as IA
from scipy import stats
from scipy.optimize import least_squares
from skimage.util import img_as_ubyte
from skimage.transform import downscale_local_mean
import imageio
import time
import configparser

class Autofocus():
    """Autofocus.

       The autofocus will follow the routine set in hs.AF

       **Autofocus routines:**
        - full: Scan the entire section at a predetermined objective position,
          even if a previous in focus objective position was found. Use for
          small sections and the zstage has changed positions.
        - partial: Image only center of section at a predetermined objective
          position, even if a previous in focus objective position was found.
          Use for large sections and the zstage has changed positions.
        - full once: Scan the entire section at a predetermined objective
          position, only if a previous in focus objective position has not been
          found. Use for small sections and the zstage has not changed position.
        - partial once: Image only center of section at a predetermined
          objective position, only if a previous in focus objective position has
          not been found. Use for large sections and the zstage has not changed
          position.

       **Attributes:**
        - hs (HiSeq): HiSeq object.
        - pos_dict (int): Stage position information of the section.
        - rough_ims (list): Thumbnails of the focusing section.
        - scale (int): Down scale factor for thumbnails.
        - files (list): Filenames of images stitched for rough_ims.
        - logger (logger): Logger object to log communication with HiSeq.

    """

    def __init__(self, hs, pos_dict):
        """Constructor for the Autofocus object."""

        self.hs = hs
        self.pos_dict = pos_dict
        self.rough_ims = []
        self.scale = None
        self.files = []
        self.logger = hs.logger

        if hs.virtual:
            self.image_path = hs.focus_data
        else:
            self.image_path = hs.image_path

    def partial_scan(self, image_name = 'RoughScan'):
        """Out of focus center scan of the section.

           The middle full length of the section is imaged at a predefined,
           probably out of focus, objective position. The channel images
           are scaled down (if the images are larger the 256 kb) and then
           normalized.

           **Parameters:**
            - image_name (str): Common name for images, default is 'RoughScan'.

           **Returns:**
            - list: Processed images of the section from 4 channels.
            - int: Scale down factor of the images.
            - list: Filenames of the raw images used to make the processed images.

         """

        name_ = 'PartialScan::'
        hs = self.hs
        pos_dict = self.pos_dict

        hs.x.move(pos_dict['x_center'])
        x_initial = hs.x.position
        y_initial = hs.y.position
        # Move to rough focus position
        #hs.obj.move(hs.obj.focus_rough)
        #z_pos = [hs.z.focus_pos, hs.z.focus_pos, hs.z.focus_pos]
        #hs.z.move(z_pos)
        # Take rough focus image
        self.message(name_+'Scanning section')
        if hs.virtual:
            im_path = path.join(self.image_path, 'partial')
        else:
            im_path = self.image_path
            hs.scan(1, 1, pos_dict['n_frames'], image_name)
        hs.y.move(y_initial)
        hs.x.move(x_initial)

        # Scale & Normalize partial focus image
        self.message(name_+'Scaling & Normalizing images')
        for ch in hs.channels:
            df_x = IA.get_image_df(im_path, 'c'+str(ch)+'_'+image_name)
            plane, scale = IA.stitch(im_path, df_x, scaled = True)
            self.rough_ims.append(IA.normalize(plane, scale))
            self.files += [*df_x.index]

        self.scale = scale

        return self.rough_ims, scale, self.files

    def full_scan(self, image_name = 'RoughScan'):
        """Scan entire out of focus section.

           The section is imaged at a predefined objective position. Multiple
           images comprising the section are stitched together and possiblly
           scaled down (if the images are larger the 256 kb) and then
           normalized.

           **Parameters:**
            - image_name (str): Common name for images, default is 'RoughScan'.

           **Returns:**
            - list: Processed images of the section from 4 channels.
            - int: Scale down factor of the images.
            - list: Filenames of the raw images used to make the processed images.

         """

        name_ = 'FullScan::'
        hs = self.hs
        pos_dict = self.pos_dict

        x_initial = hs.x.position
        y_initial = hs.y.position
        # Move to rough focus position
        #hs.obj.move(hs.obj.focus_rough)
        #z_pos = [hs.z.focus_pos, hs.z.focus_pos, hs.z.focus_pos]
        #hs.z.move(z_pos)
        # Take rough focus image
        self.message(name_+'Scanning section')
        if hs.virtual:
            im_path = path.join(self.image_path,'full')
        else:
            im_path = self.image_path
            hs.scan(pos_dict['n_tiles'], 1, pos_dict['n_frames'], image_name)
        hs.y.move(y_initial)
        hs.x.move(x_initial)

        # Stitch rough focus image
        self.message(name_+'Stitching & Normalizing images')
        for ch in hs.channels:
            df_x = IA.get_image_df(im_path, 'c'+str(ch)+'_'+image_name)
            plane, scale = IA.stitch(im_path, df_x, scaled = True)
            self.rough_ims.append(IA.normalize(plane, scale))
            self.files += [*df_x.index]

        self.scale = scale

        return self.rough_ims, scale, self.files

    def get_focus_data(self, px_points, n_markers):
        """Return stage position focal point at each pixel point.

           Loop through candidate focus *px_points*, and take an objective stack
           at each position until n_markers with an optimal objective position
           have been found.

           **Parameters:**
            - px_points (2xN array): Row x Column position of candidate focal points
            - n_markers (int): Number of focus markers to find

           **Returns:**
            - 4x*n_markers array*: X-stage step, Y-stage step, Obj step, and
              index of focal position.

        """

        hs = self.hs
        pos_dict = self.pos_dict
        scale = self.scale
        p2s = self.hs.px_to_step
        name_ = 'GetFocusData::'

        focus_points = np.full((n_markers,4), -1)
        i = 0
        n_obj = 0
        focus_data = None
        while n_obj < n_markers:
        # Take obj_stack at focus points until n_markers have been found
            px_pt = px_points[i,:]
            [x_pos, y_pos] = p2s(px_pt[0], px_pt[1], pos_dict, scale)
            hs.y.move(y_pos)
            hs.x.move(x_pos)
            fs = hs.obj_stack()

            f_fs = self.format_focus(fs)
            if f_fs is not False:
               obj_pos = self.fit_mixed_gaussian(f_fs)
               if obj_pos:
                   self.message(name_+'Found focus point ', n_obj+1)
                   self.message(False, name_+'Point at x =', x_pos,
                                       'y =',y_pos,'obj =', obj_pos )

                   ##################################################################
                   # Save in focus frame
    ##               in_focus_frame = np.argmin(abs(f_fs[:,0]-obj_pos))
    ##               frame_name = '740_'+str(in_focus_frame)+'.jpeg'
    ##               z_pos = ''
    ##               for z in z_pos:
    ##                   z_pos += str(z) + '_'
    ##               os.rename(path.join(hs.image_path,frame_name), path.join(hs.image_path,
    ##                         z_pos+str(px_pt[0])+'_'+str(px_pt[1])+'.jpeg'))
                   ##################################################################

                   focus_points[n_obj,:] = [x_pos, y_pos, obj_pos, i]
                   n_obj += 1

               else:
                   self.message(False, name_+'No Focus at point',n_obj+1,
                                 'at x =',x_pos,'and y =',y_pos)

            if i == len(px_points)-1:
                focus_points = focus_points[focus_points[:,3]>-1,:]
                self.message(name_+'Only found',n_obj+1,'focus points')
                break
            else:
                i += 1

        return focus_points


    def message(self, *args):
        """Print output text to console (default) or log file.

           If there is no logger, text is printed to the console.
           If a logger is assigned, and the first argument is False, text is
           printed to the log file, otherwise text is printed to the console.

        """

        i = 0
        if isinstance(args[0], bool):
            i = 1
            screen = args[0]
        else:
            screen = True

        msg = 'Autofocus::'
        for a in args[i:]:
            msg += str(a) + ' '

        if self.logger is None:
            print(msg)
        else:
            if screen:
                self.logger.log(21, msg)
            else:
                self.logger.info(msg)

    def delete_focus_images(self):
        """Delete images used for focusing."""

        if not self.hs.virtual:
            for f in self.files:
                remove(path.join(self.hs.image_path, f))

    def format_focus(self, focus_data):
        """Return processed focus frame file sizes.

           Objective positions are calculated for corresponding frames. The
           objective position series of JPEG frame sizes from each camera are
           determined to contain a signal if the kurtosis of the series is
           significant. Series with signals are summed and normalized.

           **Parameters:**
            - focus_data (Nx4 array): JPEG frame file sizes from the 4 cameras.

           **Returns:**
            - array (Nx2): The 1st column is the objective step and the 2nd
              column is the corresponding processed frame size.

        """

        name_ = 'FormatFocus::'
        hs = self.hs

        if hs.cam1.getFrameInterval() != hs.cam2.getFrameInterval():
            message(hs.logger,name_,'Frame interval mismatch')

        frame_interval = hs.cam1.getFrameInterval()
        spf = hs.obj.v*1000*hs.obj.spum*frame_interval # steps/frame

        # Remove frames after objective stops moving
        n_frames = len(focus_data)
        _frames = range(n_frames)
        objsteps = hs.obj.focus_start + np.array(_frames)*spf
        objsteps = objsteps[objsteps < hs.obj.focus_stop]


        # Number of formatted frames
        n_f_frames = len(objsteps)
        objsteps = np.reshape(objsteps, (n_f_frames, 1))

        #formatted focus data
        f_fd = np.zeros(shape = (n_f_frames,1))

        nrows, ncols = focus_data.shape
        for i in range(ncols):
            # test if there is a tail in data and add if True
            #kurt_z, pvalue = stats.kurtosistest(focus_data[0:n_f_frames,i])
            kurt_z, pvalue = stats.kurtosistest(focus_data[:,i])
            if kurt_z > 1.96:
                self.message(False, name_,'Signal in', hs.channels[i], 'channel')
                f_fd = f_fd + np.reshape(focus_data[0:n_f_frames,i], (n_f_frames,1))

        # Normalize
        if np.sum(f_fd) == 0:
            return False
        else:
            f_fd = f_fd/ np.sum(f_fd)
            f_fd = np.reshape(f_fd, (n_f_frames, 1))

            return np.concatenate((objsteps,f_fd), axis=1)

    def fit_mixed_gaussian(self, data):
        """Fit focus data & return optimal objective focus step.

           Focus objective step vs frame JPEG file size is fit to a mixed
           gaussian model. The optimal objective focus step is returned at step
           of the max fit JPEG file. If the objective focus step is not
           returned, False is returned.

           **Parameters:**
            - data (array Nx2): Focus data where the 1st column is the objective
              step and the 2nd column is the corresponding file size.

           **Returns:**
            - int: Optimal focus objective step if found (if not, False).

        """

        name_ = 'FitMixedGaussian::'
        hs = self.hs

        # initialize values
        max_peaks = 4
        # Initialize varibles
        amp = []; amp_lb = []; amp_ub = []
        cen = []; cen_lb = []; cen_ub = []
        sigma = []; sigma_lb = []; sigma_ub = []
        y = data[:,1]
        SST = np.sum((y-np.mean(y))**2)
        R2 = 0
        tolerance = 0.9                                                             # Tolerance for R2
        xfun = data[:,0]; yfun = data[:,1]

        # Add peaks until fit reaches threshold
        while len(amp) <= max_peaks and R2 < tolerance:
            # set initial guesses
            max_y = np.max(y)
            amp.append(max_y*10000)
            index = np.argmax(y)
            y = np.delete(y, index)
            index = np.where(data[:,1] == max_y)[0][0]
            cen.append(data[index,0])
            sigma.append(np.sum(data[:,1]**2)**0.5*10000)
            p0 = np.array([amp, cen, sigma])
            p0 = p0.flatten()

            # set bounds
            amp_lb.append(0); amp_ub.append(np.inf)
            cen_lb.append(np.min(data[:,0])); cen_ub.append(np.max(data[:,0]))
            sigma_lb.append(0); sigma_ub.append(np.inf)
            lo_bounds = np.array([amp_lb, cen_lb, sigma_lb])
            up_bounds = np.array([amp_ub, cen_ub, sigma_ub])
            lo_bounds = lo_bounds.flatten()
            up_bounds = up_bounds.flatten()

            # Optimize parameters
            results = least_squares(res_gaussian, p0, bounds=(lo_bounds,up_bounds),
                                    args=(data[:,0],data[:,1]))

            if not results.success:
                self.message(False,name_,results.message)
            else:
                R2 = 1 - np.sum(results.fun**2)/SST
                self.message(False,name_,'R2=',R2,'with',len(amp),'peaks')


            if results.success and R2 > tolerance:
                _objsteps = range(hs.obj.focus_start, hs.obj.focus_stop,
                                  int(hs.nyquist_obj/2))
                _focus = gaussian(_objsteps, results.x)
                optobjstep = int(_objsteps[np.argmax(_focus)])
            else:
                optobjstep = False
                if len(amp) == max_peaks:
                    self.message(False, name_, 'Bad fit')
                    break

        return optobjstep

        def get_obj_step(section):
            if self.config.has_section(section):
                obj_step = int(self.config.get(section,))




# def calibrate(hs, pos_list):
#
#     e_ = enumerate(pos_list)
#     for index, pos_dict in e_:
# ##        while index <= 0:
# ##            index, pos_dict = e_.__next__()
# ##        # Position objective for optimal focus for Rough Scan
# ##        print(index)
#
#         hs.y.move(pos_dict['y_center'])
#         hs.x.move(pos_dict['x_center'])
#         hs.z.move([21500, 21500, 21500])
#
#         fs = hs.obj_stack()
#         f_fs = format_focus(hs, fs)
#         if f_fs is not False:
#             obj_pos = fit_mixed_gaussian(hs, f_fs)
#             if obj_pos:
#                 hs.obj.move(obj_pos)
#             else:
#                 obj_pos = int((hs.obj.focus_stop - hs.obj.focus_start)/2 + hs.obj.focus_start)
#         else:
#             obj_pos = int((hs.obj.focus_stop - hs.obj.focus_start)/2 + hs.obj.focus_start)
#
#         hs.obj.move(obj_pos)
#
#         pos_i = str(index)
#         # Initial scan of section
#         hs.y.move(pos_dict['y_initial'])
#         hs.x.move(pos_dict['x_initial'])
#         hs.obj.move(obj_pos)
#         rough_ims, scale = rough_focus(hs, pos_dict['n_tiles'], pos_dict['n_frames'], 'RoughScan'+pos_i)
#         for i in range(len(hs.channels)):
#             imageio.imwrite(path.join(hs.image_path,'c'+str(hs.channels[i])+'INIT'+pos_i+'.tiff'), rough_ims[i])
#
#         # Sum channels with signal
#         sum_im = image.sum_images(rough_ims)
#         imageio.imwrite(path.join(hs.image_path,'sum_im' + pos_i + '.tiff'), sum_im)
#     ##    sum_im = imageio.imread(path.join(hs.image_path,'sum_im.tiff'))
#     ##    scale = 16
#
#         # Find pixels to focus on
#         px_rows, px_cols = sum_im.shape
#         #n_markers = 3 + int((px_rows*px_cols*scale**2)**0.5*hs.resolution/1000)
#         n_markers = 6
#         ord_points = image.get_focus_points(sum_im, scale, n_markers*10)
#         np.savetxt(path.join(hs.image_path, 'ord_points'+pos_i+'.txt'), ord_points)
#
#     ##    ord_points = np.loadtxt(path.join(hs.image_path, 'ord_points.txt'))
#
#         #Get stage positions on in-focus points
#         focus_points = get_focus_data(hs, ord_points, n_markers, scale, pos_dict)
#         np.savetxt(path.join(hs.image_path, 'focus_points'+pos_i+'.txt'), focus_points)
#         last_point = focus_points[-1,3]
#         np.savetxt(path.join(hs.image_path, 'last_point'+pos_i+'.txt'), np.array([last_point]))
#     ##    focus_points = np.loadtxt(path.join(hs.image_path, 'focus_points.txt'))
#         pos_ord_points = ord_points[focus_points[:,3].astype(int)]
#         np.savetxt(path.join(hs.image_path, 'pos_ord_points'+pos_i+'.txt'), pos_ord_points)
#
#     z_list = [21320, 21380, 21440, 21560, 21620, 21680]
#     n_markers = 6
#     scale = 8
#     for motor in range(3):
#         for z in z_list:
#             print('moving motor ' + str(motor) + ' to ' + str(z))
#             z_pos = [21500, 21500, 21500]
#             z_pos[motor] = z
#             hs.z.move(z_pos)
#             for index, pos_dict in enumerate(pos_list):
#                 pos_i = str(index)
#                 pos_ord_points = np.loadtxt(path.join(hs.image_path,  'pos_ord_points'+pos_i+'.txt'))
#                 fp_name = ''
#                 for z_ in hs.z.position:
#                     fp_name += str(z_) + '_'
#                 fp_name += 'm'+str(motor)+'_'+str(pos_i) + '.txt'
#                 fp = get_focus_data(hs, pos_ord_points, n_markers, scale, pos_dict)
#                 if fp.any():
#                     np.savetxt(path.join(hs.image_path, fp_name), fp)
#                 else:
#                     print('no data for motor ' + str(motor) + ' at ' + str(z))


def autofocus(hs, pos_dict):
    """Finds and returns the objective step for optimal focus.

       The section defined by the *pos_dict* is imaged at a predefined objective
       position. Channel images with signal are summed together into 1 image.
       Ideal positions to focus on are extracted from the summed image. The
       optimal focus objective step are found from a number of focus positions
       and the median objective step is returned.

       **Parameters:**
        - hs (HiSeq): HiSeq object.
        - pos_dict (dict): Dictionary of stage position information.

       **Returns:**
        - int: Objective step for optimal focus.

     """


    start = time.time()
    old_obj_pos = pos_dict['obj_pos']
    # Scan section
    af = Autofocus(hs, pos_dict)

    if hs.AF == 'partial':
        af.partial_scan()
        old_obj_pos = None
    elif hs.AF == 'full':
        af.full_scan()
        old_obj_pos = None
    elif old_obj_pos is None:
        if hs.AF == 'partial once':
            af.partial_scan()
        if hs.AF == 'full once':
            af.full_scan()

    if old_obj_pos is None:
        af.message('Analyzing out of focus image')
        # Sum channels with signal
        sum_im = IA.sum_images(af.rough_ims, hs.logger)
    else:
        sum_im = None

    # Find pixels to focus on
    if sum_im is not None:
        af.message('Finding potential focus positions')
        px_rows, px_cols = sum_im.shape
        n_markers = int((px_rows*px_cols*af.scale**2)**0.5*hs.resolution/1000)
        n_markers += 3
        ord_points = IA.get_focus_points(sum_im, af.scale, n_markers*10,hs.logger)
        af.message('Found',len(ord_points),'focus positions')

        # Get stage positions on in-focus points
        af.message('Finding optimal focus')
        focus_points = af.get_focus_data(ord_points, n_markers)
        if focus_points.any():
            opt_obj_pos = int(np.median(focus_points[:,2]))
        else:
            af.message('FAILED::Could not find focus')
            opt_obj_pos = False
    elif old_obj_pos is not None:
        af.message('Using previous objective position')
        opt_obj_pos = old_obj_pos
    else:
        af.message('FAILED::No signal in channels')
        opt_obj_pos = False

    # Remove rough focus images
    af.delete_focus_images()

    stop = time.time()
    af_time = int((stop-start)/60)
    af.message('Completed in',af_time,'minutes')

    return opt_obj_pos



# def autofocus_test(hs, pos_dict, af = False):
#
#     hs.z.move([21500, 21500, 21500])
#     obj_pos = False
#     if af:
#       hs.y.move(pos_dict['y_center'])
#       hs.x.move(pos_dict['x_center'])
#       fs = hs.obj_stack()
#       f_fs = format_focus(hs, fs)
#       if f_fs is not False:
#           obj_pos = fit_mixed_gaussian(hs, f_fs)
#           if obj_pos:
#               hs.obj.move(obj_pos)
#
#     if not obj_pos:
#       obj_pos = int((hs.obj.focus_stop - hs.obj.focus_start)/2 + hs.obj.focus_start)
#       hs.obj.move(obj_pos)
#
#     # Initial scan of section
#     hs.y.move(pos_dict['y_initial'])
#     hs.x.move(pos_dict['x_initial'])
#
#     rough_ims, scale = rough_scan(hs, pos_dict['n_tiles'], pos_dict['n_frames'], image_name = 'INIT')
#     for i in range(len(hs.channels)):
#       imageio.imwrite(path.join(hs.image_path,'c'+str(hs.channels[i])+'INIT.tiff'), rough_ims[i])
#     ####    #rough_ims = []
#     ####    #for i in range(len(hs.channels)):
#     ####    #    rough_ims.append(imageio.imread(path.join(hs.image_path,'c'+str(hs.channels[i])+'RoughFocus.tiff')))
#     ####    #    scale = 16
#
#     # Sum channels with signal
#     sum_im = image.sum_images(rough_ims)
#     imageio.imwrite(path.join(hs.image_path,'INIT_sum_im.tiff'), sum_im)
#     ##    sum_im = imageio.imread(path.join(hs.image_path,'sum_tilt_im.tiff'))
#     ##    scale = 16
#
#     # Find pixels to focus on
#     px_rows, px_cols = sum_im.shape
#     n_markers = 3 + int((px_rows*px_cols*scale**2)**0.5*hs.resolution/1000)
#     ord_points = image.get_focus_points(sum_im, scale, n_markers*10)
#     np.savetxt(path.join(hs.image_path, 'INIT_ord_points.txt'), ord_points)
#     #ord_points = np.loadtxt(path.join(hs.image_path, 'INIT_ord_points.txt'))
#
#
#     # Get stage positions on in-focus points
#     focus_points = get_focus_data(hs, ord_points, n_markers, scale, pos_dict)
#     np.savetxt(path.join(hs.image_path, 'INIT_focus_points.txt'), focus_points)
#     last_point = focus_points[-1,3]
#     np.savetxt(path.join(hs.image_path, 'last_point.txt'), np.array([last_point]))
#
#     # Save focus positions
#     pos_points = ord_points[focus_points[:,3].astype(int)]
#
#     # Drastic Tilt
#     hs.y.move(pos_dict['y_initial'])
#     hs.x.move(pos_dict['x_initial'])
#     hs.z.move([21000, 22000, 21500])
#     rough_ims, scale = rough_focus(hs, pos_dict['n_tiles'], pos_dict['n_frames'], image_name = 'TILT')
#     for i in range(len(hs.channels)):
#        imageio.imwrite(path.join(hs.image_path,'c'+str(hs.channels[i])+'TILT.tiff'), rough_ims[i])
#
#     # Get stage positions on in-focus points
#     focus_points = get_focus_data(hs, pos_points, n_markers, scale, pos_dict)
#     np.savetxt(path.join(hs.image_path, 'TILT_focus_points.txt'), focus_points)
#     #focus_points = np.loadtxt(path.join(hs.image_path, 'TILT_focus_points.txt'))
#
#     # Get adjusted z stage positions for level image
#     hs.im_obj_pos = 30000
#     center, n_ip = planeFit(focus_points[:,0:3])
#     n_ip[2] = abs(n_ip[2])
#     z_pos = autolevel(hs, n_ip, center)
#     print('zpos', z_pos)
#     np.savetxt(path.join(hs.image_path, 'z_pos_raw.txt'), np.array(z_pos))
#     for i in range(3):
#        if z_pos[i] > 25000:
#            z_pos[i] = 25000
#     np.savetxt(path.join(hs.image_path, 'z_pos_check.txt'), np.array(z_pos))
#     print('leveling... ', z_pos)
#     hs.z.move(z_pos)
#
#     # Move to p=optimal objective position
#     for i in range(last_point, len(ord_points)):
#        [x_pos, y_pos] = hs.px_to_step(ord_points[i,0], ord_points[i,1], pos_dict, scale)
#        hs.y.move(y_pos)
#        hs.x.move(x_pos)
#        fs = hs.obj_stack()
#        f_fs = format_focus(hs, fs)
#        if f_fs is not False:
#           obj_pos = fit_mixed_gaussian(hs, f_fs)
#           if obj_pos:
#               np.savetxt(path.join(hs.image_path, 'last_focus_point.txt' ), ord_points[i,:])
#               break
#
#     # Image leveled planeFit
#     hs.y.move(pos_dict['y_initial'])
#     hs.x.move(pos_dict['x_initial'])
#     hs.obj.move(obj_pos)
#     rough_ims, scale = rough_focus(hs, pos_dict['n_tiles'], pos_dict['n_frames'], image_name = 'LVL')
#     for i in range(len(hs.channels)):
#        imageio.imwrite(path.join(hs.image_path,'c'+str(hs.channels[i])+'LVL.tiff'), rough_ims[i])
#
#     # Get stage positions on in-focus points
#     focus_points = get_focus_data(hs, pos_points, n_markers, scale, pos_dict)
#     np.savetxt(path.join(hs.image_path, 'LVL_focus_points.txt'), focus_points)
#
#     return z_pos, obj_pos

# def rough_scan(hs, n_tiles, n_frames, image_name = 'RoughScan'):
#     """Scan out of focus section and return stitched and normalized images.
#
#        The section is imaged at a predefined objective position. Multiple images
#        comprising the section are stitched together and possible scaled down (if
#        the images are larger the 256 kb) and then normalized.
#
#        **Parameters:**
#        - hs (HiSeq): HiSeq object.
#        - n_tiles (int): Number of x positions to image.
#        - n_frames (int): Number of frames to image.
#        - image_name (str): Common name for images, the default is 'RoughScan'.
#
#        **Returns:**
#        - list: Processed images of the section from 4 channels.
#        - int: Scale down factor of the images.
#        - list: Filenames of the raw images used to make the processed images.
#
#      """
#
#     name_ = 'RoughScan::'
#     x_initial = hs.x.position
#     y_initial = hs.y.position
#     # Move to rough focus position
#     #hs.obj.move(hs.obj.focus_rough)
#     #z_pos = [hs.z.focus_pos, hs.z.focus_pos, hs.z.focus_pos]
#     #hs.z.move(z_pos)
#     # Take rough focus image
#     message(hs.logger, True, name_+'Scanning section')
#     if not hs.virtual:
#         hs.scan(n_tiles, 1, n_frames, image_name)
#     hs.y.move(y_initial)
#     hs.x.move(x_initial)
#     rough_ims = []
#     files = []
#     # Stitch rough focus image
#     message(hs.logger, True, name_+'Stitching & Normalizing images')
#     for ch in hs.channels:
#         if hs.virtual:
#             im_path = hs.focus_data
#         else:
#             im_path = hs.image_path
#         df_x = IA.get_image_df(im_path, 'c'+str(ch)+'_'+image_name)
#         plane, scale_factor = IA.stitch(im_path, df_x, scaled = True)
#         rough_ims.append(IA.normalize(plane, scale_factor))
#         files += [*df_x.index]
#
#     return rough_ims, scale_factor, files





def gaussian(x, *args):
    """Gaussian function for curve fitting."""

    name_ = 'Gaussian::'
    if len(args) == 1:
      args = args[0]

    n_peaks = int(len(args)/3)


    if len(args) - n_peaks*3 != 0:
      print('Unequal number of parameters')
    else:
      for i in range(n_peaks):
        amp = args[0:n_peaks]
        cen = args[n_peaks:n_peaks*2]
        sigma = args[n_peaks*2:n_peaks*3]

      g_sum = 0
      for i in range(len(amp)):
          g_sum += amp[i]*(1/(sigma[i]*(np.sqrt(2*np.pi))))*(np.exp((-1.0/2.0)*(((x-cen[i])/sigma[i])**2)))

      return g_sum

def res_gaussian(args, xfun, yfun):
    """Gaussian residual function for curve fitting."""

    g_sum = gaussian(xfun, args)

    return yfun-g_sum




def autolevel(hs, n_ip, centroid):
    """Level stage, work in progress."""

    # Find normal vector of motor plane
    mp = np.array(hs.z.get_motor_points(),dtype = float)
    mp[:,0] = mp[:,0] / hs.x.spum
    mp[:,1] = mp[:,1] / hs.y.spum
    mp[:,2] = mp[:,2] / hs.z.spum
    u_mp = mp[1,:] - mp[0,:]
    v_mp = mp[2,:] - mp[0,:]
    n_mp = np.cross(u_mp, v_mp)
    n_mp = n_mp/np.linalg.norm(n_mp)
    n_mp[2] = abs(n_mp[2])


    tilt = [0, 0, 1] - n_ip
    # Pick reference motor based on tilt of imaging plane
    if tilt[0] >= 0:
        p_mp = 0 # right motor
    elif tilt[1] >= 0:
        p_mp = 2 # left back motors
    else:
        p_mp = 1 # left front motor

    d_mp = -np.dot(n_mp, mp[p_mp,:])

    # Find objective position on imaging plane at reference motor
    d_ip = -np.dot(n_ip, centroid)

    mag_ip = np.linalg.norm(centroid)
    correction = [0, 0, mag_ip] - n_ip*mag_ip
    print('correction', correction)


    z_centroid = -(centroid[0]*n_mp[0] + centroid[1]*n_mp[1] + d_mp)/n_mp[2]
    # print(obj_mp)
    ##mp[p_mp,2] = obj_mp
    # # Calculate plane correction
    mag_mp = np.linalg.norm(np.array([centroid[0],centroid[1],z_centroid]))
    #mag_mp = np.linalg.norm(mp[p_mp,:])
    print('z mag',mag_mp)
    # n_ip = n_ip * mag_mp
    print('obj mag',mag_ip)
    # correction = [0, 0, mag_mp] - n_ip
    # #correction = [0, 0, 1] - n_ip

    # Calculate target motor plane for a flat, level image plane
    n_mp = n_mp * mag_mp
    print('n_mp', n_mp)
    correction = correction * mag_mp / mag_ip
    print('correction', correction)
    n_tp = n_mp +  correction
    print('target plane', n_tp)

    #n_tp = n_mp
    #n_tp = n_tp / np.linalg.norm(n_tp)
    #n_tp = n_tp * mag_mp

    # Move motor plane to preferred objective position
    offset_distance = hs.im_obj_pos/hs.obj.spum - centroid[2]
    offset_distance = offset_distance + hs.z.position[p_mp]/hs.z.spum
    #mp[p_mp,2] = offset_distance

    #offset_distance = int(offset_distance*hs.z.spum)

    #d_tp = -np.dot(n_tp, mp[p_mp,:])
    d_tp = -np.dot(n_tp, [centroid[0],centroid[1],z_centroid])

    z_pos = []
    for i in range(3):
        z_pos.append(int(-(n_tp[0]*mp[i,0] + n_tp[1]*mp[i,1] + d_tp)/n_tp[2]))

    # Convert back to z step position
    z_pos = np.array(z_pos)
    z_pos = z_pos * hs.z.spum
    z_pos = z_pos.astype('int')
    #hs.z.move(z_pos)

    return z_pos


def planeFit(points):
    """Fit points to a plane.

    Code copied from `math stackexchange
    <https://math.stackexchange.com/questions/99299/best-fitting-plane-given-a-set-of-points>`_

    Given an array, points, of shape (d,...) representing points in
    d-dimensional space, fit an d-dimensional plane to the points.

    **Example:**

    .. code-block:: python

        p, n = planeFit(points)

    **Parameters:**
     - points (array): Points of shape (d,...) representing points in
                      d-dimensional space.

    **Returns:**
     - array: Point, p, on the plane (the point-cloud centroid)
     - array: Normal, n of the plane

    """

    points = np.transpose(points)

    points = np.reshape(points, (np.shape(points)[0], -1)) # Collapse trialing dimensions
    assert points.shape[0] <= points.shape[1], "There are only {} points in {} dimensions.".format(points.shape[1], points.shape[0])
    ctr = points.mean(axis=1)
    x = points - ctr[:,np.newaxis]
    M = np.dot(x, x.T) # Could also use np.cov(x) here.
    return ctr, svd(M)[0][:,-1]
