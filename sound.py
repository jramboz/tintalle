import warnings
with warnings.catch_warnings(): #pydub prints a warning if ffmpeg or avlib aren't installed, but we don't care
    warnings.simplefilter('ignore')
    from pydub import AudioSegment
import os
import logging

# Polaris compatible sound specifications
_SAMPLE_RATE = 44100
_CHANNELS = 1 # mono
_BIT_DEPTH = 2 # 16-bit

def convert_wav_to_polaris_raw(input: str, output: str = None) -> str | None:
    '''Converts a wav file to a raw file with the appropriate parameters for use in a Polaris Anima.
    If no output path/filename is specified, it will use the input filename with '.RAW' in the same directory.
    Returns filename (with path) if successful. Returns None if failed.'''
    _log = logging.getLogger('Sound')

    try:
        #open the file
        _log.debug(f'Opening audio file: {input}')
        sound: AudioSegment = AudioSegment.from_file(input, format='wav')

        # set sound to proper parameters
        _log.debug(f'Converting file to parameters: Sample Rate = {_SAMPLE_RATE}, Channels = {_CHANNELS}, Bit Depth = {_BIT_DEPTH*8}-bit')
        sound = sound.set_frame_rate(_SAMPLE_RATE)
        sound = sound.set_channels(_CHANNELS)
        sound = sound.set_sample_width(_BIT_DEPTH)

        # get output path and filename
        if not output:
            # if no output is specified, use '{basename}.RAW' in the same directory
            path = os.path.dirname(os.path.realpath(input))
            output = os.path.join(path, os.path.splitext(os.path.basename(input))[0] + '.RAW')
        if not os.path.dirname(output):
            # if output didn't include a path, default to the same path as the input
            path = os.path.dirname(os.path.realpath(input))
            output = os.path.join(path, output)
        if os.path.isdir(output) or output.endswith(os.path.sep):
            # if output was specified as a directory but no filename, first check if it's an absolute or relative path
            if not os.path.isabs(output):
                # if it's a relative path, use the input file location as the base
                output = os.path.join(os.path.dirname(os.path.realpath(input)), output)
            # create dir (if needed) and append filename
            if not os.path.exists(output) or not os.path.isdir(output):
                _log.debug(f'Creating output directory: {output}')
                os.mkdir(output)
            output = os.path.join(output, os.path.splitext(os.path.basename(input))[0] + '.RAW')

        # write output file
        _log.debug(f'Writing output file: {output}')
        sound.export(output, format='raw')
        return output

    except Exception as e:
        _log.error(e)
        return None
