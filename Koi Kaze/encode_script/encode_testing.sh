cd ..
mkdir encode
vspipe -c y4m encode_script/encode_testing.vpy --timecodes encode/encode_testing_timecodes.dat - | x264 --demuxer y4m - --output encode/encode_testing.x264 --preset placebo --deblock -2:-2 --crf 13 --merange 32 --no-dct-decimate --no-mbtree --qcomp 0.75 --aq-mode 3 --aq-strength 0.7 --output-depth 10
cd encode/
mkvmerge -o encode_testing.mkv --timecodes 0:encode_testing_timecodes.dat encode_testing.x264