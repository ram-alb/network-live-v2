lte_select = """
    SELECT
        atoll_mrat.xgcellslte.cell_id,
        atoll_mrat.xgtransmitters.azimut,
        atoll_mrat.xgtransmitters.height,
        atoll_mrat.sites.longitude,
        atoll_mrat.sites.latitude
    FROM atoll_mrat.xgtransmitters
        INNER JOIN atoll_mrat.sites
            ON atoll_mrat.xgtransmitters.site_name = atoll_mrat.sites.name
        INNER JOIN atoll_mrat.xgcellslte
            ON atoll_mrat.xgtransmitters.tx_id = atoll_mrat.xgcellslte.tx_id
"""

wcdma_select = """
    SELECT
        atoll_mrat.ucells.cell_id,
        atoll_mrat.utransmitters.azimut,
        atoll_mrat.utransmitters.height,
        atoll_mrat.sites.longitude,
        atoll_mrat.sites.latitude
    FROM atoll_mrat.utransmitters
        INNER JOIN atoll_mrat.sites
            ON atoll_mrat.utransmitters.site_name = atoll_mrat.sites.name
        INNER JOIN atoll_mrat.ucells
            ON atoll_mrat.utransmitters.tx_id = atoll_mrat.ucells.tx_id
"""

gsm_select = """
    SELECT
        atoll_mrat.gtransmitters.tx_id,
        atoll_mrat.gtransmitters.azimut,
        atoll_mrat.gtransmitters.height,
        atoll_mrat.sites.longitude,
        atoll_mrat.sites.latitude
    FROM atoll_mrat.gtransmitters
        INNER JOIN atoll_mrat.sites
            ON atoll_mrat.gtransmitters.site_name = atoll_mrat.sites.name
"""

nr_select = """
    SELECT
        atoll_mrat.xgcells5gnr.cell_id,
        atoll_mrat.xgtransmitters.azimut,
        atoll_mrat.xgtransmitters.height,
        atoll_mrat.sites.longitude,
        atoll_mrat.sites.latitude
    FROM
        atoll_mrat.xgtransmitters
    INNER JOIN atoll_mrat.xgcells5gnr
        ON atoll_mrat.xgcells5gnr.tx_id = atoll_mrat.xgtransmitters.tx_id
    INNER JOIN atoll_mrat.sites
        ON atoll_mrat.xgtransmitters.site_name = atoll_mrat.sites.name
"""

lte_insert = """
    INSERT
        INTO ltecells2
    VALUES (
        :subnetwork,
        :enodeb_id,
        :site_name,
        :cell_name,
        :tac,
        :cellId,
        :eci,
        :earfcndl,
        :qRxLevMin,
        :administrativeState,
        :rachRootSequence,
        :physicalLayerCellId,
        :cellRange,
        :vendor,
        :ip_address,
        :oss,
        :azimut,
        :height,
        :longitude,
        :latitude,
        :insert_date,
        :primaryPlmnReserved
    )
"""

wcdma_insert = """
    INSERT
        INTO wcdmacells2
    VALUES (
        :operator,
        :rnc_id,
        :rnc_name,
        :site_name,
        :cell_name,
        :localCellId,
        :cId,
        :uarfcnDl,
        :uarfcnUl,
        :primaryScramblingCode,
        :LocationArea,
        :RoutingArea,
        :ServiceArea,
        :Ura,
        :primaryCpichPower,
        :maximumTransmissionPower,
        :qRxLevMin,
        :qQualMin,
        :IubLink,
        :MocnCellProfile,
        :administrativeState,
        :ip_address,
        :vendor,
        :oss,
        :azimut,
        :height,
        :longitude,
        :latitude,
        :insert_date
    )
"""

gsm_insert = """
    INSERT
        INTO gsmcells2
    VALUES (
        :operator,
        :bsc_id,
        :bsc_name,
        :site_name,
        :cell_name,
        :bcc,
        :ncc,
        :lac,
        :cell_id,
        :bcchNo,
        :hsn,
        :maio,
        :dchNo,
        :state,
        :vendor,
        :oss,
        :azimut,
        :height,
        :longitude,
        :latitude,
        :insert_date
    )
"""

nr_insert = """
    INSERT
        INTO nrcells
    VALUES (
        :subnetwork,
        :gNBId,
        :site_name,
        :cell_name,
        :cellLocalId,
        :cellState,
        :nCI,
        :nRPCI,
        :nRTAC,
        :rachRootSequence,
        :qRxLevMin,
        :arfcnDL,
        :bSChannelBwDL,
        :configuredMaxTxPower,
        :ip_address,
        :vendor,
        :oss,
        :azimut,
        :height,
        :longitude,
        :latitude,
        :insert_date,
        :ssbFrequency
    )
"""

atoll_selects = {
    'LTE': lte_select,
    'WCDMA': wcdma_select,
    'GSM': gsm_select,
    'NR': nr_select,
}

network_live_inserts = {
    'LTE': lte_insert,
    'WCDMA': wcdma_insert,
    'GSM': gsm_insert,
    'NR': nr_insert,
}
