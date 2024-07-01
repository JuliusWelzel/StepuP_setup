"""
    Minimal usage example
    Connects to QTM and streams 3D data forever
"""

import pylsl
import asyncio
import qtm_rt
import time

def create_lsl_outlet():
    """
    Creates and returns an LSL (Lab Streaming Layer) outlet for Qualisys data.

    Returns:
        pylsl.StreamOutlet: The LSL outlet object.

    Raises:
        None
    """
    info = pylsl.StreamInfo(
        name="Qualisys",
        type="6D",
        channel_count=3,
        nominal_srate=100,
        channel_format=pylsl.cf_float32, # make sure to define the correct data type you get from the SDK
        source_id="qtm_6d",
    )
    outlet = pylsl.StreamOutlet(info)
    return outlet

def on_packet(packet):
    """
    Process a packet received from the Qualisys system.
    Each iteration of this function will push a sample to the LSL outlet.
    All markers are pushed as a single sample.

    Args:
        packet: The packet received from the Qualisys system.

    Returns:
        None

    Raises:
        None
    """
    header, markers = packet.get_3d_markers_no_label()
    for marker in markers:
        outlet.push_sample(list(marker[0:4])) # this corresponds to the x, y, z, and marker id
        print(marker)

async def setup():
    """
    Connects to the Qualisys system and sets up an LSL outlet for streaming frames.
    Only streams marker data which is not automatically labeled by the Qualisys system.

    Returns:
        None

    Raises:
        None
    """
    connection = await qtm_rt.connect("127.0.0.1")
    if connection is None:
        return
    
    # create lsl outlet
    global outlet
    outlet = create_lsl_outlet()
    input("Start LabRecorder ... Press Enter to continue")

    await connection.stream_frames(components=["3dnolabels"], on_packet=on_packet)


if __name__ == "__main__":
    asyncio.ensure_future(setup())
    asyncio.get_event_loop().run_forever()