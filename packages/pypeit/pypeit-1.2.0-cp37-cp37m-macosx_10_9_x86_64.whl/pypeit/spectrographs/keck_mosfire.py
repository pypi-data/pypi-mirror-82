""" Module for Keck/MOSFIRE specific codes
"""
from pkg_resources import resource_filename
import numpy as np
from pypeit import msgs
from pypeit import telescopes
from pypeit.core import framematch
from pypeit.par import pypeitpar
from pypeit.spectrographs import spectrograph
from pypeit.images import detector_container

from IPython import embed

class KeckMOSFIRESpectrograph(spectrograph.Spectrograph):
    """
    Child to handle Keck/MOSFIRE specific code
    """
    ndet = 1

    def __init__(self):
        # Get it started
        super(KeckMOSFIRESpectrograph, self).__init__()
        self.telescope = telescopes.KeckTelescopePar()
        self.spectrograph = 'keck_mosfire'
        self.camera = 'MOSFIRE'

    def get_detector_par(self, hdu, det):
        """
        Return a DectectorContainer for the current image

        Args:
            hdu (`astropy.io.fits.HDUList`):
                HDUList of the image of interest.
                Ought to be the raw file, or else..
            det (int):

        Returns:
            :class:`pypeit.images.detector_container.DetectorContainer`:

        """
        # Detector 1
        detector_dict = dict(
            binning         = '1,1',
            det             = 1,
            dataext         = 0,
            specaxis        = 1,
            specflip        = False,
            spatflip        = False,
            platescale      = 0.1798,
            darkcurr        = 0.8,
            saturation      = 1e9, # ADU, this is hacked for now
            nonlinear       = 1.00,  # docs say linear to 90,000 but our flats are usually higher
            numamplifiers   = 1,
            mincounts       = -1e10,
            gain            = np.atleast_1d(2.15),  # Taken from MOSFIRE detector webpage
            ronoise         = np.atleast_1d(5.8), # This is for 16 non-destructuve reads, the default readout mode
            datasec         = np.atleast_1d('[:,:]'),
            oscansec        = np.atleast_1d('[:,:]')
        )
        return detector_container.DetectorContainer(**detector_dict)

    def default_pypeit_par(self):
        """
        Set default parameters for Keck/MOSFIRE
        """
        par = pypeitpar.PypeItPar()
        par['rdx']['spectrograph'] = 'keck_mosfire'
        # Wavelengths
        # 1D wavelength solution
        par['calibrations']['wavelengths']['rms_threshold'] = 0.30 #0.20  # Might be grating dependent..
        par['calibrations']['wavelengths']['sigdetect']=5.0
        par['calibrations']['wavelengths']['fwhm']= 5.0
        par['calibrations']['wavelengths']['n_final']= 4
        par['calibrations']['wavelengths']['lamps'] = ['OH_NIRES']
        #par['calibrations']['wavelengths']['nonlinear_counts'] = self.detector[0]['nonlinear'] * self.detector[0]['saturation']
        par['calibrations']['wavelengths']['method'] = 'holy-grail'
        # Reidentification parameters
        #par['calibrations']['wavelengths']['reid_arxiv'] = 'keck_nires.fits'
        par['calibrations']['slitedges']['edge_thresh'] = 50.
        par['calibrations']['slitedges']['sync_predict'] = 'nearest'


        # Flats
        # Do not illumination correct. We should also not be flat fielding given the bars.
        # TODO Implement imaging flats for MOSFIRE. Do test with/without illumination flats.
        # Turn of illumflat
        turn_off = dict(use_biasimage=False, use_overscan=False, use_darkimage=False)
        par.reset_all_processimages_par(**turn_off)

        # Extraction
        par['reduce']['skysub']['bspline_spacing'] = 0.8
        par['reduce']['extraction']['sn_gauss'] = 4.0

        # Flexure
        par['flexure']['spec_method'] = 'skip'

        par['scienceframe']['process']['sigclip'] = 20.0
        par['scienceframe']['process']['satpix'] ='nothing'

        # Set the default exposure time ranges for the frame typing
        par['calibrations']['standardframe']['exprng'] = [None, 20]
        par['calibrations']['arcframe']['exprng'] = [20, None]
        par['calibrations']['darkframe']['exprng'] = [20, None]
        par['scienceframe']['exprng'] = [20, None]


        # Sensitivity function parameters
        par['sensfunc']['algorithm'] = 'IR'
        par['sensfunc']['polyorder'] = 8
        par['sensfunc']['IR']['telgridfile'] = resource_filename('pypeit', '/data/telluric/TelFit_MaunaKea_3100_26100_R20000.fits')


        return par



    def init_meta(self):
        """
        Generate the meta data dict
        Note that the children can add to this
        Returns:
            self.meta: dict (generated in place)
        """
        meta = {}
        # Required (core)
        meta['ra'] = dict(ext=0, card='RA')
        meta['dec'] = dict(ext=0, card='DEC')
        meta['target'] = dict(ext=0, card='TARGNAME')
        meta['decker'] = dict(ext=0, card='MASKNAME')
        meta['binning'] = dict(ext=0, card=None, default='1,1')

        meta['mjd'] = dict(ext=0, card='MJD-OBS')
        meta['exptime'] = dict(ext=0, card='TRUITIME')
        meta['airmass'] = dict(ext=0, card='AIRMASS')
        # Extras for config and frametyping
        meta['dispname'] = dict(ext=0, card='OBSMODE')
        meta['idname'] = dict(card=None, compound=True)
        # Filter
        meta['filter1'] = dict(ext=0, card='FILTER')
        # Lamps
        lamp_names = ['FLATSPEC']
        for kk,lamp_name in enumerate(lamp_names):
            meta['lampstat{:02d}'.format(kk+1)] = dict(ext=0, card=lamp_name)
        # Ingest
        self.meta = meta

    def compound_meta(self, headarr, meta_key):
        """
        Args:
            headarr: list
            meta_key: str
        Returns:
            value
        """
        if meta_key == 'idname':
            if headarr[0].get('KOAIMTYP', None) is not None:
                return headarr[0].get('KOAIMTYP')
            else:
                try:
                    # TODO: This should be changed to except on a specific error.
                    FLATSPEC = int(headarr[0].get('FLATSPEC'))
                    PWSTATA7 = int(headarr[0].get('PWSTATA7'))
                    PWSTATA8 = int(headarr[0].get('PWSTATA8'))
                    if FLATSPEC == 0 and PWSTATA7 == 0 and PWSTATA8 == 0:
                        return 'object'
                    elif FLATSPEC == 1:
                        return 'flatlamp'
                    elif PWSTATA7 == 1 or PWSTATA8 == 1:
                        return 'arclamp'
                except:
                    return 'unknown'
        else:
            msgs.error("Not ready for this compound meta")

    def configuration_keys(self):
        return ['decker', 'dispname', 'filter1']

    def pypeit_file_keys(self):
        pypeit_keys = super(KeckMOSFIRESpectrograph, self).pypeit_file_keys()
        pypeit_keys += ['calib', 'comb_id', 'bkg_id']
        return pypeit_keys

    def check_frame_type(self, ftype, fitstbl, exprng=None):
        """
        Check for frames of the provided type.
        """
        good_exp = framematch.check_frame_exptime(fitstbl['exptime'], exprng)
        if ftype in ['science', 'standard']:
            return good_exp & (fitstbl['idname'] == 'object')
        if ftype in ['bias', 'dark']:
            return good_exp & self.lamps(fitstbl, 'off') & (fitstbl['idname'] == 'dark')
        if ftype in ['pixelflat', 'trace']:
            # Flats and trace frames are typed together
            return good_exp & self.lamps(fitstbl, 'dome') & (fitstbl['idname'] == 'flatlamp')
        if ftype == 'pinhole':
            # Don't type pinhole frames
            return np.zeros(len(fitstbl), dtype=bool)
        if ftype in ['arc', 'tilt']:
            # TODO: This is a kludge.  Allow science frames to also be
            # classified as arcs
            is_arc = self.lamps(fitstbl, 'arcs') & (fitstbl['idname'] == 'arclamp')
            is_obj = self.lamps(fitstbl, 'off') & (fitstbl['idname'] == 'object')
            return good_exp & (is_arc | is_obj)
        msgs.warn('Cannot determine if frames are of type {0}.'.format(ftype))
        return np.zeros(len(fitstbl), dtype=bool)

    def lamps(self, fitstbl, status):
        """
        Check the lamp status.
        Args:
            fitstbl (:obj:`astropy.table.Table`):
                The table with the fits header meta data.
            status (:obj:`str`):
                The status to check.  Can be `off`, `arcs`, or `dome`.
        Returns:
            numpy.ndarray: A boolean array selecting fits files that
            meet the selected lamp status.
        Raises:
            ValueError:
                Raised if the status is not one of the valid options.
        """
        if status == 'off':
            # Check if all are off
            return np.all(np.array([fitstbl[k] == 0 for k in fitstbl.keys() if 'lampstat' in k]),
                          axis=0)
        if status == 'arcs':
            # Check if any arc lamps are on
            arc_lamp_stat = [ 'lampstat{0:02d}'.format(i) for i in range(1,6) ]
            return np.any(np.array([ fitstbl[k] == 1 for k in fitstbl.keys()
                                            if k in arc_lamp_stat]), axis=0)
        if status == 'dome':
            return fitstbl['lampstat01'] == '1'

        raise ValueError('No implementation for status = {0}'.format(status))



