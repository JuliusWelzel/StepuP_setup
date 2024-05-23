"""
    Minimal usage example
    Connects to QTM and streams 3D data forever
    (start QTM first, load file, Play->Play with Real-Time output)
"""

import pylsl
import asyncio
import qtm_rt
import time

def create_lsl_outlet():
    """ Create a LSL outlet """
    info = pylsl.StreamInfo(
        name="Qualisys",
        type="6D",
        channel_count=3,
        nominal_srate=100,
        channel_format=pylsl.cf_float32,
        source_id="qtm_6d",
    )
    outlet = pylsl.StreamOutlet(info)
    return outlet

def on_packet(packet):
    """ Callback function that is called everytime a data packet arrives from QTM """
    #print("Framenumber: {}".format(packet.framenumber))
    header, markers = packet.get_3d_markers_no_label()
    for marker in markers:
        outlet.push_sample(list(marker[0:3]))
        print(marker)
        time.sleep(1)


async def setup():
    """ Main function """
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