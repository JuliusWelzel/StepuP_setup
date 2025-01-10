from __future__ import print_function
from vicon_dssdk import ViconDataStream
import argparse
import sys
import pylsl as lsl

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('host', nargs='?', help="Host name, in the format of server:port", default = "localhost:801")
args = parser.parse_args()

client = ViconDataStream.Client()


try:
    client.Connect('192.168.10.1:801')
    # Check the version
    print( 'Version', client.GetVersion() )

    # Check setting the buffer size works
    client.SetBufferSize( 1 )

    #Enable all the data types
    client.EnableSegmentData()
    client.EnableMarkerData()
    client.EnableUnlabeledMarkerData()
    client.EnableMarkerRayData()
    client.EnableDeviceData()
    client.EnableCentroidData()
    # Report whether the data types have been enabled
    assert client.IsUnlabeledMarkerDataEnabled(), 'Unlabeled Marker Data Not Enabled, please check your setup'


    # prepare lsl stream
    srate = client.GetFrameRate() 
    n_channels = 4 # this should corresüond to x,y,z position and the marker id
    info = lsl.StreamInfo(
        name="Vicon",
        type="MoCap",
        channel_count=n_channels,
        nominal_srate=srate,
        channel_format=lsl.cf_float32, # make sure to define the correct data type you get from the SDK
    )
    outlet = lsl.StreamOutlet(info)
    print('LSL Stream created')

    HasFrame = False
    timeout = 50
    while not HasFrame:
        print( '.' )
        try:
            if client.GetFrame():
                HasFrame = True
            timeout=timeout-1
            if timeout < 0:
                print('Failed to get frame')
                sys.exit()
        except ViconDataStream.DataStreamException as e:
            client.GetFrame()
    
    # set stream mode
    client.SetStreamMode( ViconDataStream.Client.StreamMode.EClientPullPreFetch )
    print( 'Get Frame PreFetch', client.GetFrame(), client.GetFrameNumber() )

    # set axis mapping to Stepup standard (check your coordinatesystem and adjust if necessary)
    client.SetAxisMapping( ViconDataStream.Client.AxisMapping.EForward, ViconDataStream.Client.AxisMapping.ELeft, ViconDataStream.Client.AxisMapping.EUp )
    xAxis, yAxis, zAxis = client.GetAxisMapping()
    print( 'X Axis', xAxis, 'Y Axis', yAxis, 'Z Axis', zAxis )

    unlabeledMarkers = client.GetUnlabeledMarkers()
    for markerPos, trajID in unlabeledMarkers:
        print( 'Unlabeled Marker at', markerPos, 'with trajID', trajID )
        outlet.push_sample([*markerPos, trajID])

    labeledMarkers = client.GetLabeledMarkers()
    for markerPos, trajID in labeledMarkers:
        print( 'Labeled Marker at', markerPos, 'with trajID', trajID )
        outlet.push_sample([*markerPos, trajID])

except ViconDataStream.DataStreamException as e:
    print( 'Handled data stream error', e )
