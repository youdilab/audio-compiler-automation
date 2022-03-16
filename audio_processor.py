#******Upwork Prototype******---------------------
#Credits
#Music: https://www.bensound.com
#Text to Speech Clips: https://ttsreader.com/
#-------------------------------------------------

import numpy as np
from scipy.io.wavfile import read,write

#Constants------------------------(START)
PEAK_LEVEL = 32767
#Constants------------------------(FINISH)

#Functions------------------------(START)

#Function to merge 2 wav files----
def merge_2_in_sequence(data1,data2):
    return np.concatenate((data1, data2))

#Function to merge 3 wav files----
def merge_3_in_sequence(data1,data2,data3):
    return np.concatenate((data1, data2,data3))


#Function to amplify by factor---
#factor is represented as a percentage
def amplify_by_factor(data,factor):
    data_float = data.astype('f')
    data_mult_float = (data_float * factor)/100
    data_mult_float_clipped = avoid_clipping_distortion(data_mult_float)
    return np.rint(data_mult_float_clipped).astype('int16')

#Function to slice the length of wav file---
#slice_length = Sampling Rate * Length of Slice in seconds
def slice_at_end(data,slice_length):
    return data[:len(data)-slice_length,:]

def slice_from_beginning(data,slice_length):
    print('slice length',slice_length)
    return data[0:slice_length,:]

def get_length_seconds(data,sample_rate):
    return len(data)/sample_rate

def get_length_samples(data):
    return len(data)

#Function to regulate levels over PEAK_LEVEL----
def avoid_clipping_distortion(data_int32):
    clipped_int32 = np.clip(data_int32, a_min = ((-1) * PEAK_LEVEL), a_max = PEAK_LEVEL)
    return clipped_int32.astype('int16')
    # for frame in data_int32:
    #     for channel_point in frame:
    #         if (channel_point>PEAK_LEVEL):
    #             channel_point = PEAK_LEVEL
    
    # data_int16 = data_int32.astype('int16')
    # return data_int16

#Function to mix 2 wav files with an offset----
def mix_with_offset(long_data,short_data,offset_length):
    long_length = len(long_data)
    short_length = len(short_data)

    if (long_length<short_length):
        print("Please recheck data lengths.")
        return short_data
    elif(long_length-offset_length<short_length):
        print("Offset is too long.")
        return short_data
    else:
        overlapping_long_data = long_data[offset_length:offset_length+short_length,:]
        overlapping_long_data_int32 = overlapping_long_data.astype('int32')
        short_data_int32 =  short_data.astype('int32')
        mixed_data_int32 = np.add(overlapping_long_data_int32,short_data_int32)
        mixed_part_noclip_int16 = avoid_clipping_distortion(mixed_data_int32)

        long_pre_overlap = long_data[0:offset_length,:]
        long_post_overlap = long_data[offset_length+short_length:,:]
        data_merged = merge_3_in_sequence(long_pre_overlap,mixed_part_noclip_int16,long_post_overlap)
    return data_merged


#Function to fade in and fade out from the start and the end---
#fade_length = Sampling Rate * Length of Fade in Period in seconds
def fade_in_out(data, fade_length):
    if(len(data)<fade_length):
        print("Audio clip is too short. Please make the fade-in duration shorter and try again.")
        return data
    elif(fade_length==1 or fade_length==0):
        print("Fade length is too short to hear any change.")
        return data
    else:
        data_float = data.astype('f')
        fade_in_part_float = data_float[:fade_length,:]
        fade_out_part_float = data_float[(len(data_float)-fade_length):,:]
        non_fading_part_float = data_float[fade_length:(len(data_float)-fade_length),:]

        for i in range(fade_length):
            frame_in = fade_in_part_float[i,:]
            frame_out = fade_out_part_float[i,:]
            n_channels_in = len(frame_in)
            n_channels_out = len(frame_out)

            factor_in = (i/(fade_length-1))
            factor_out = ((fade_length-(i+1))/(fade_length-1))
            for j in range(n_channels_in):    
                fade_in_part_float[i,j] = fade_in_part_float[i,j]*factor_in
                fade_out_part_float[i,j] = fade_out_part_float[i,j]*factor_out
        
        merged_float = merge_3_in_sequence(fade_in_part_float,non_fading_part_float,fade_out_part_float)
        merged_int = np.rint(merged_float).astype('int16')
        return merged_int

#Functions------------------------(FINISH)