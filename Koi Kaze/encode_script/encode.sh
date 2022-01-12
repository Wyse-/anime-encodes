cd ..
mkdir encode
for i in *.vpy ; do
	vspipe --y4m "$i" --timecodes encode/"$i"_timecodes.dat - | x264 --demuxer y4m - --output encode/"$i".x264 --level 4.1 --vbv-bufsize 78125 --vbv-maxrate 62500 --preset placebo --profile high10 --crf 13 --sar 32:27 --output-depth 10 --tune grain --min-keyint 24 --direct auto --rc-lookahead 250 --merange 32 --ipratio 1.30 --bframes 16
	cd encode/	
	mkvmerge -o "$i".mkv --timecodes 0:"$i"_timecodes.dat "$i".x264
	cd ..
done