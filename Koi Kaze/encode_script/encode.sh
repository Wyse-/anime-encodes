cd ..
mkdir encode
for i in `ls *.vpy -1v` ; do
	vspipe -c y4m "$i" --timecodes encode/"$i"_timecodes.dat encode/"$i".y4m
	x264 --demuxer y4m encode/"$i".y4m --output encode/"$i".h264 --tcfile-in encode/"$i"_timecodes.dat --preset placebo --deblock -2:-2 --crf 13 --merange 32 --no-dct-decimate --no-mbtree --qcomp 0.75 --aq-mode 3 --aq-strength 0.7 --output-depth 10
	cd encode/
	mkvmerge -o "$i".mkv --timecodes 0:"$i"_timecodes.dat "$i".h264
	rm "$i".y4m
	rm "$i"_timecodes.dat
	rm "$i".h264
	cd ..
done