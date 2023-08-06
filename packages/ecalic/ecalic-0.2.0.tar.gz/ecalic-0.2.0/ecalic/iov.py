#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd, numpy as np
from lxml import etree
import os
import ecalic

class xml:
    payload = None
    def __init__(self, xml, type = 'ic'):
        """
        The class xml handles an ecal payload xml. The xml is transformed in
        a pandas dataframe that can be directly given to the module ic.

        Parameters:
        -----------
        xml : input xml file
        type: support different type of xml file, available types:
              - ic         : EcalIntercalibConstantsRcd (default)
              - laser      : EcalLaserAPDPNRatiosRcd
              - alpha      : EcalLaserAlphasRcd
              - thresholds : EcalPFRecHitThresholdsRcd
              - status     : EcalChannelStatusRcd
              - adc        : EcalADCToGeVConstantRcd
              - noise      : EcalPedestalsRcd (noise x12)
              - pedestal   : EcalPedestalsRcd (pedestal x12)
              - noiseG     : EcalPedestalsRcd (noise xG with G = gain)
              - pedestalG  : EcalPedestalsRcd (pedestal xG with G = gain)
        """
        if   type.lower().find('ic') >= 0 or type.lower().find('alpha') >= 0 or type.lower().find('thresholds') >= 0:
            ebPath = '/boost_serialization/cmsCondPayload/eb-/m_items/item'
            eePath = '/boost_serialization/cmsCondPayload/ee-/m_items/item'
        elif type.lower().find( 'laser'    ) >= 0:
            ebPath = '/boost_serialization/cmsCondPayload/laser-map/eb-/m_items/item/p1'
            eePath = '/boost_serialization/cmsCondPayload/laser-map/ee-/m_items/item/p1'
        elif type.lower().find( 'status'   ) >= 0:
            ebPath = '/boost_serialization/cmsCondPayload/eb-/m_items/item/status-'
            eePath = '/boost_serialization/cmsCondPayload/ee-/m_items/item/status-'
        elif type.lower().find( 'adc'      ) >= 0:
            ebPath = '/boost_serialization/cmsCondPayload/EBvalue-'
            eePath = '/boost_serialization/cmsCondPayload/EEvalue-'
        elif type.lower().find( 'pedestal' ) >= 0:
            gstr = type.split('tal')
            g = gstr[1] if len(gstr)>0 and gstr[1] != '' else '12'
            ebPath = '/boost_serialization/cmsCondPayload/eb-/m_items/item/mean-x' + g
            eePath = '/boost_serialization/cmsCondPayload/ee-/m_items/item/mean-x' + g
        elif type.lower().find( 'noise'   ) >= 0:
            gstr = type.split('oise')
            g = gstr[1] if len(gstr)>0 and gstr[1] != '' else '12'
            ebPath = '/boost_serialization/cmsCondPayload/eb-/m_items/item/rms-x' + g
            eePath = '/boost_serialization/cmsCondPayload/ee-/m_items/item/rms-x' + g
        else:
            raise Exception('xml type %s is wrong (supported type can be find in xml doc)' % type.lower())

        iov = etree.parse( xml )
        iov_eb = [ [index, 0,float(xtal.text)] for index,xtal in enumerate(iov.xpath(ebPath)) ]
        iov_ee = [ [index, 1,float(xtal.text)] for index,xtal in enumerate(iov.xpath(eePath)) ]
        if type.lower().find('adc') >= 0:
            iov_eb = np.array(iov_eb * (ecalic.geom.iz == 0).sum())
            iov_ee = np.array(iov_ee * (ecalic.geom.iz != 0).sum())
            iov_eb[:,0] = ecalic.geom[ecalic.geom['iz'] == 0].hashedId
            iov_ee[:,0] = ecalic.geom[ecalic.geom['iz'] != 0].hashedId

        self.payload = pd.concat( [ pd.DataFrame( iov_eb, columns = ['hashedId','ecal','ic'] ),
                                    pd.DataFrame( iov_ee, columns = ['hashedId','ecal','ic'] ) ] )

    def icCMS( self, name = ''):
        """
        return an object of type ecalic.icCMS
        """
        return ecalic.icCMS(self.payload,name=name )

    def dump_txt( self,fileout ):
        """
        dump xml content to a txt file (ix iy iz ic)
        """
        print (' Saving payload to txt file: ' + fileout)
        ## replace nan ic with 1 and nan (the latter should not exist)
        geom  = ecalic.geom
        geom['ecal'] = geom['iz'].where(geom['iz']==0,1)
        out = pd.merge(geom, self.payload, on = ['hashedId','ecal'] )
        out.replace({'ic' : { np.nan : 1 } }).to_csv( fileout,
                            columns = ['ix','iy','iz','ic'],
                            header = False, index = False, sep = '\t', float_format = '%+6.5f' )
