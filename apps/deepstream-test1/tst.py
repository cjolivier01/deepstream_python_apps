import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

# Initialize GStreamer
Gst.init(None)

# Create a pipeline
pipeline = Gst.Pipeline.new('my-pipeline')

# Add elements to the pipeline
# Example: Read a video file and display it in a window
src = Gst.ElementFactory.make('filesrc', 'file-source')
src.set_property('location', '/mnt/src/hm/stiched.mp4')

decode = Gst.ElementFactory.make('decodebin', 'decoder')

sink = Gst.ElementFactory.make('autovideosink', 'video-sink')

pipeline.add(src)
pipeline.add(decode)
pipeline.add(sink)

# Link the elements
src.link(decode)
decode.connect('pad-added', lambda element, pad: pad.link(sink.get_static_pad('sink')))

# Set the pipeline to playing state
pipeline.set_state(Gst.State.PLAYING)

# Run the pipeline until EOS (End-of-Stream) is reached
bus = pipeline.get_bus()
while True:
    msg = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.ERROR | Gst.MessageType.EOS)
    if msg:
        if msg.type == Gst.MessageType.ERROR:
            print('Error:', msg.parse_error())
            break
        elif msg.type == Gst.MessageType.EOS:
            print('End-of-Stream reached')
            break

# Stop the pipeline
pipeline.set_state(Gst.State.NULL)