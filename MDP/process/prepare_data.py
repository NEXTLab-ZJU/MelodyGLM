import os
from tqdm import tqdm
from glob import glob
from utils.process_ts import process_ts44
from utils.process_extract_melody import extract_melody
from utils.process_quantization import quantise
from utils.process_segment import process_seg
from utils.process_tonality import process_normalization
from utils.process_quality import process_quality
from utils.process_dedup import deduplicate

if __name__ == '__main__':
    # datasets you want to process
    dataset_list = ['pop909']
    for dataset_name in dataset_list[:]:

        # -------------------------------------------------------------------------------- #
        # parameters
        # -------------------------------------------------------------------------------- #
        raw_data_root = 'data/raw'
        dst_data_root = 'data/processed'
        src_dir = os.path.join(raw_data_root, dataset_name)
        dst_dir = os.path.join(dst_data_root, dataset_name)

        src_dir_ts44 = os.path.join(src_dir)
        dst_dir_ts44 = os.path.join(dst_dir, '1_TS44')
        dst_dir_melody = os.path.join(dst_dir, '2_melody')
        dst_dir_quantization = os.path.join(dst_dir, '3_quantization')
        dst_dir_segment = os.path.join(dst_dir, '4_segment')
        dst_dir_tonality = os.path.join(dst_dir, '5_tonality')
        dst_dir_quality = os.path.join(dst_dir, '6_quality')
        dst_dir_dedup = os.path.join(dst_dir, '7_dedup')


        # -------------------------------------------------------------------------------- #
        # process pipline
        # -------------------------------------------------------------------------------- #
        # >>>> step01: select 4/4 ts (Time Signature, ts). requirement >= 8 bars 
        process_ts44(src_dir_ts44, dst_dir_ts44)

        # >>>> step02: extract melody
        extract_melody(src_dir=dst_dir_ts44, dst_dir=dst_dir_melody)

        # >>>> step03: quantization (base and triplets)
        quantise(dst_dir_melody, dst_dir_quantization)  

        # >>>> step04: segment
        process_seg(dst_dir_quantization, dst_dir_segment)

        # >>>> step05: tonality normaliztion
        process_normalization(dst_dir_segment, dst_dir_tonality)

        # >>>> step06: filter midis by heuristic rules
        process_quality(dst_dir_tonality, dst_dir_quality)

        # >>>> step07: internal dedup by pitch intercal 
        deduplicate(dst_dir_quality, dst_dir_dedup)