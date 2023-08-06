""" Utilities for spectograph codes
"""
import numpy as np

from pypeit import spectrographs
from pypeit import msgs
from IPython import embed

# TODO: Allow the spectrographs to be identified by their camera?  Won't
# work for 'shane_kast_red' and 'shane_kast_red_ret'.


def load_spectrograph(spectrograph):
    """
    Instantiate a :class:`spectrographs.spectrograph.Spectrograph`, if
    possible.

    Args:
        spectrograph (:obj:`str`, :class:`spectrographs.spectrograph.Spectrograph`): The
            spectrograph to instantiate.  If the input is a spectrograph
            instance, the instance is simply returned.  If a string, the
            string is used to select the spectrograph to instantiate.
            If None, None is returned.

    Returns:
        :class:`spectrographs.spectrograph.Spectrograph`: The spectrograph used to obtain the data to be reduced.

    """

    if spectrograph is None:
        return None

    if isinstance(spectrograph, spectrographs.spectrograph.Spectrograph):
        return spectrograph

    if spectrograph == 'gemini_gnirs':
        return spectrographs.gemini_gnirs.GeminiGNIRSSpectrograph()

    if spectrograph == 'gemini_flamingos1':
        return spectrographs.gemini_flamingos.GeminiFLAMINGOS1Spectrograph()

    if spectrograph == 'gemini_flamingos2':
        return spectrographs.gemini_flamingos.GeminiFLAMINGOS2Spectrograph()

    if spectrograph == 'keck_deimos':
        return spectrographs.keck_deimos.KeckDEIMOSSpectrograph()

    if spectrograph == 'keck_kcwi':
        return spectrographs.keck_kcwi.KeckKCWISpectrograph()

    if spectrograph == 'keck_lris_blue':
        return spectrographs.keck_lris.KeckLRISBSpectrograph()

    if spectrograph == 'keck_lris_blue_orig':
        return spectrographs.keck_lris.KeckLRISBOrigSpectrograph()

    if spectrograph == 'keck_lris_red':
        return spectrographs.keck_lris.KeckLRISRSpectrograph()

    if spectrograph == 'keck_lris_red_orig':
        return spectrographs.keck_lris.KeckLRISROrigSpectrograph()

    if spectrograph == 'keck_hires_red':
        return spectrographs.keck_hires.KECKHIRESRSpectrograph()

#    if spectrograph == 'keck_hires_blue':
#        return spectrographs.keck_hires.KECKHIRESBSpectrograph()

    if spectrograph == 'keck_nires':
        return spectrographs.keck_nires.KeckNIRESSpectrograph()

    if spectrograph == 'keck_nirspec_low':
        return spectrographs.keck_nirspec.KeckNIRSPECLowSpectrograph()

    if spectrograph == 'keck_mosfire':
        return spectrographs.keck_mosfire.KeckMOSFIRESpectrograph()

    if spectrograph == 'magellan_fire':
        return spectrographs.magellan_fire.MagellanFIREEchelleSpectrograph()

    if spectrograph == 'magellan_fire_long':
        return spectrographs.magellan_fire.MagellanFIRELONGSpectrograph()

    if spectrograph == 'magellan_mage':
        return spectrographs.magellan_mage.MagellanMAGESpectrograph()

    if spectrograph == 'shane_kast_blue':
        return spectrographs.shane_kast.ShaneKastBlueSpectrograph()

    if spectrograph == 'shane_kast_red':
        return spectrographs.shane_kast.ShaneKastRedSpectrograph()

    if spectrograph == 'shane_kast_red_ret':
        return spectrographs.shane_kast.ShaneKastRedRetSpectrograph()

    if spectrograph == 'wht_isis_blue':
        return spectrographs.wht_isis.WHTISISBlueSpectrograph()

    if spectrograph == 'wht_isis_red':
        return spectrographs.wht_isis.WHTISISRedSpectrograph()

    if spectrograph == 'tng_dolores':
        return spectrographs.tng_dolores.TNGDoloresSpectrograph()

    if spectrograph == 'vlt_xshooter_uvb':
        return spectrographs.vlt_xshooter.VLTXShooterUVBSpectrograph()

    if spectrograph == 'vlt_xshooter_vis':
        return spectrographs.vlt_xshooter.VLTXShooterVISSpectrograph()

    if spectrograph == 'vlt_xshooter_nir':
        return spectrographs.vlt_xshooter.VLTXShooterNIRSpectrograph()

    if spectrograph == 'vlt_fors2':
        return spectrographs.vlt_fors.VLTFORS2Spectrograph()

    if spectrograph == 'gemini_gmos_south_ham':
        return spectrographs.gemini_gmos.GeminiGMOSSHamSpectrograph()

    if spectrograph == 'gemini_gmos_north_e2v':
        return spectrographs.gemini_gmos.GeminiGMOSNE2VSpectrograph()

    if spectrograph == 'gemini_gmos_north_ham':
        return spectrographs.gemini_gmos.GeminiGMOSNHamSpectrograph()

    if spectrograph == 'lbt_mods1r':
        return spectrographs.lbt_mods.LBTMODS1RSpectrograph()

    if spectrograph == 'lbt_mods2r':
        return spectrographs.lbt_mods.LBTMODS2RSpectrograph()

    if spectrograph == 'lbt_mods1b':
        return spectrographs.lbt_mods.LBTMODS1BSpectrograph()

    if spectrograph == 'lbt_mods2b':
        return spectrographs.lbt_mods.LBTMODS2BSpectrograph()

    if spectrograph == 'lbt_luci1':
        return spectrographs.lbt_luci.LBTLUCI1Spectrograph()

    if spectrograph == 'lbt_luci2':
        return spectrographs.lbt_luci.LBTLUCI2Spectrograph()

    if spectrograph == 'mmt_binospec':
        return spectrographs.mmt_binospec.MMTBINOSPECSpectrograph()

    if spectrograph == 'mmt_mmirs':
        return spectrographs.mmt_mmirs.MMTMMIRSSpectrograph()

    if spectrograph == 'mdm_osmos_mdm4k':
        return spectrographs.mdm_osmos.MDMOSMOSMDM4KSpectrograph()

    if spectrograph == 'not_alfosc':
        return spectrographs.not_alfosc.NOTALFOSCSpectrograph()

    if spectrograph == 'p200_dbsp_red':
        return spectrographs.p200_dbsp.P200DBSPRedSpectrograph()
    
    if spectrograph == 'p200_dbsp_blue':
        return spectrographs.p200_dbsp.P200DBSPBlueSpectrograph()

    if spectrograph == 'p200_tspec':
        return spectrographs.p200_tspec.P200TSPECSpectrograph()


    msgs.error('{0} is not a supported spectrograph.'.format(spectrograph))

