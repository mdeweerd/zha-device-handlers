"""LIDL TS011F plug."""


from zigpy.profiles import zha
from zigpy.zcl.clusters.general import (
    Basic,
    GreenPowerProxy,
    Groups,
    Identify,
    OnOff,
    Ota,
    Scenes,
    Time,
)

from zhaquirks.const import (
    DEVICE_TYPE,
    ENDPOINTS,
    INPUT_CLUSTERS,
    MODEL,
    OUTPUT_CLUSTERS,
    PROFILE_ID,
)
from zhaquirks.tuya.ts011f_plug import Plug_3AC_4USB


class Lidl_Plug_3AC_4USB(Plug_3AC_4USB):
    """LIDL 3 outlet + 4 USB with restore power state support."""

    def __init__(self, *args, **kwargs):
        """Initialize with task."""
        super().__init__(*args, **kwargs)

        # self._init_plug_task = asyncio.create_task(self.spell())

    async def spell(self) -> None:
        """Initialize device so that all endpoints become available."""
        basic_cluster = self.endpoints[1].in_clusters[0]

        # The magic spell is needed only once.
        # TODO: Improve by doing this only once (successfully).

        # Magic spell - part 1
        attr_to_read = [4, 0, 1, 5, 7, 0xFFFE]
        await basic_cluster.read_attributes(attr_to_read)

        # Magic spell - part 2 (skipped - does not seem to be needed)
        # attr_to_write={0xffde:13}
        # basic_cluster.write_attributes(attr_to_write)

    signature = {
        MODEL: "TS011F",
        ENDPOINTS: {
            # <SimpleDescriptor endpoint=1 profile=260 device_type=266
            # device_version=1
            # input_clusters=[0, 3, 4, 5, 6]
            # output_clusters=[10, 25]>
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_PLUG_IN_UNIT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    OnOff.cluster_id,
                ],
                OUTPUT_CLUSTERS: [Time.cluster_id, Ota.cluster_id],
            },
            # <SimpleDescriptor endpoint=242 profile=41440 device_type=97
            # device_version=1
            # input_clusters=[]
            # output_clusters=[33]>
            242: {
                PROFILE_ID: 41440,
                DEVICE_TYPE: 97,
                INPUT_CLUSTERS: [],
                OUTPUT_CLUSTERS: [GreenPowerProxy.cluster_id],
            },
        },
    }