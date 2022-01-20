cd ..
mkdir encode
for i in *.vpy ; do
	vspipe -c y4m "$i" --timecodes encode/"$i"_timecodes.dat - | x264 --demuxer y4m - --output encode/"$i".x264 --preset placebo --deblock -2:-2 --crf 13 --merange 32 --no-dct-decimate --no-mbtree --qcomp 0.75 --aq-mode 3 --aq-strength 0.7 --output-depth 10
	cd encode/	
	mkvmerge -o "$i".mkv --timecodes 0:"$i"_timecodes.dat "$i".x264
	cd ..
done