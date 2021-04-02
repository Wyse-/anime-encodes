import vapoursynth as vs
from vapoursynth import core
import fvsfunc as fvf
import havsfunc as haf

DEBUG_MODE = False
	
def manual_smartfademod(clip, start_frame, end_frame):
	fixed_fade_clip = haf.smartfademod(clip, tff=True, threshold=0)
	return core.std.Trim(clip, 0, start_frame - 1) + core.std.Trim(fixed_fade_clip, start_frame, end_frame) + core.std.Trim(clip, end_frame + 1)
	
def replace_frame_with_previous(clip, frame):
	return core.std.Trim(clip, 0, frame - 1) + core.std.Trim(clip, frame - 1, frame - 1) + core.std.Trim(clip, frame + 1)
	
def replace_frame_with_next(clip, frame):
	return core.std.Trim(clip, 0, frame - 1) + core.std.Trim(clip, frame + 1, frame + 1) + core.std.Trim(clip, frame + 1)
	
def ivtc_clip_ovr(clip):
	matched_clip = core.vivtc.VFM(clip, 1)
	if DEBUG_MODE:
		return core.vivtc.VDecimate(matched_clip, ovr='./decimate_overrides/ep_21_vdecimate_override.txt', dupthresh=2.0, dryrun=True)
	else:
		return core.vivtc.VDecimate(matched_clip, ovr='./decimate_overrides/ep_21_vdecimate_override.txt', dupthresh=2.0)
		
def ivtc_clip(clip):
	matched_clip = core.vivtc.VFM(clip, 1)
	if DEBUG_MODE:
		return core.vivtc.VDecimate(matched_clip, dupthresh=2.0, dryrun=True)
	else:
		return core.vivtc.VDecimate(matched_clip, dupthresh=2.0)

def filter_clip(clip, is_nced = False):
	filterable_clip = fvf.Depth(clip, 16)
	if is_nced:
		cropped_clip = core.std.Crop(filterable_clip, bottom=2, top=2, left=4, right=2)
	else:	
		cropped_clip = core.std.Crop(filterable_clip, top=4, left=4, right=2)
	filtering_done_clip = fvf.Depth(cropped_clip, 8)				
	return filtering_done_clip;
	
def decomb_clip_whole_frame(clip, frame, order=1):
	deint = core.tdm.TDeintMod(clip, order=order, edeint=core.nnedi3.nnedi3(clip, field=order))
	return core.std.Trim(clip, 0, frame - 1) + core.std.Trim(deint, frame, frame) + core.std.Trim(clip, frame + 1)

source = core.lsmas.LWLibavSource(source='/home/wyse/Videos/NHK_NI_YOUKOSO_01/nhk_ep_21.mkv')
decimated_clip = ivtc_clip_ovr(source)	
filtered_clip = filter_clip(decimated_clip)
filtered_clip = replace_frame_with_next(filtered_clip, 323)
filtered_clip = replace_frame_with_next(filtered_clip, 5928)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 7476)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 7478)
filtered_clip = replace_frame_with_next(filtered_clip, 9532)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 9977)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 9978)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 9980)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 9982)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 9984)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 9986)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 9987)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 9988)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 9989)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 9991)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 9992)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 9993)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 9995)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 9996)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 9997)
filtered_clip = replace_frame_with_next(filtered_clip, 10826)
filtered_clip = replace_frame_with_next(filtered_clip, 10537)
filtered_clip = replace_frame_with_next(filtered_clip, 11096)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 11245)
filtered_clip = replace_frame_with_next(filtered_clip, 11400)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 11448)
filtered_clip = replace_frame_with_next(filtered_clip, 11831)
filtered_clip = replace_frame_with_next(filtered_clip, 11740)
filtered_clip = replace_frame_with_next(filtered_clip, 11761)
filtered_clip = replace_frame_with_next(filtered_clip, 14492)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 17101)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 17156)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 17546)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 17550)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 19714)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 19716)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 19718)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 19719)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 19720)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 19721)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 19723)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 19724)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 19725)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 19727)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 19728)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 19729)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 19731)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 19732)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 19733)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 19735)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 19736)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 19737)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 19739)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 19740)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 19741)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 19743)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 19744)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 19745)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 22107)
filtered_clip = replace_frame_with_next(filtered_clip, 26076)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 29109)
filtered_clip = replace_frame_with_next(filtered_clip, 30341)

# Manual Smartfademod Start
fadefixed_clip = manual_smartfademod(filtered_clip, 2171, 2194)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 7468, 7480)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 9850, 9872)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 9976, 9999)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 14015, 14038)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 17028, 17075)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 17541, 17600)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 18538, 18572)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 18734, 18758)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 19712, 19748)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 20176, 20181)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 21170, 21199)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 22925, 22976)
output_clip = manual_smartfademod(fadefixed_clip, 31253, 31259)
# Manual Smartfademod End

output_clip = fvf.Depth(output_clip, 10)

if DEBUG_MODE:
	output_clip = core.text.FrameProps(output_clip, props=['VDecimateDrop'])

output_clip.set_output()