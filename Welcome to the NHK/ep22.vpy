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
		return core.vivtc.VDecimate(matched_clip, ovr='./decimate_overrides/ep_22_vdecimate_override.txt', dupthresh=2.0, dryrun=True)
	else:
		return core.vivtc.VDecimate(matched_clip, ovr='./decimate_overrides/ep_22_vdecimate_override.txt', dupthresh=2.0)
		
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

source = core.lsmas.LWLibavSource(source='/home/wyse/Videos/NHK_NI_YOUKOSO_01/nhk_ep_22.mkv')
decimated_clip = ivtc_clip_ovr(source)	
filtered_clip = filter_clip(decimated_clip)
filtered_clip = replace_frame_with_next(filtered_clip, 323)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 2337)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 2367, 0)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 2667)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 2668)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 2671)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 5548)
filtered_clip = replace_frame_with_previous(filtered_clip, 6401)
filtered_clip = replace_frame_with_previous(filtered_clip, 10692)
filtered_clip = replace_frame_with_previous(filtered_clip, 15278)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 17142)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 17148)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 17152)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 17160)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 17164)
filtered_clip = replace_frame_with_previous(filtered_clip, 22620)
filtered_clip = replace_frame_with_previous(filtered_clip, 24216)
filtered_clip = replace_frame_with_next(filtered_clip, 25765)
filtered_clip = replace_frame_with_previous(filtered_clip, 26184)
filtered_clip = replace_frame_with_previous(filtered_clip, 27064)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 33940)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 33995)


# Manual Smartfademod Start
fadefixed_clip = manual_smartfademod(filtered_clip, 2171, 2218)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 2666, 2685)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 2858, 2878)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 4915, 4920)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 18767, 18826)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 18858, 18904)
output_clip = manual_smartfademod(fadefixed_clip, 30565, 30583)
# Manual Smartfademod End

output_clip = fvf.Depth(output_clip, 10)

if DEBUG_MODE:
	output_clip = core.text.FrameProps(output_clip, props=['VDecimateDrop'])

output_clip.set_output()