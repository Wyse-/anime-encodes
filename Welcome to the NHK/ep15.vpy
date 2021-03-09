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
		return core.vivtc.VDecimate(matched_clip, ovr='./decimate_overrides/ep_15_vdecimate_override.txt', dupthresh=2.0, dryrun=True)
	else:
		return core.vivtc.VDecimate(matched_clip, ovr='./decimate_overrides/ep_15_vdecimate_override.txt', dupthresh=2.0)
		
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

source = core.lsmas.LWLibavSource(source='/home/wyse/Videos/NHK_NI_YOUKOSO_01/nhk_ep_15.mkv')
decimated_clip = ivtc_clip_ovr(source)	
filtered_clip = filter_clip(decimated_clip)
filtered_clip = replace_frame_with_next(filtered_clip, 323)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 2829, 0)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 2830, 0)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 2832, 0)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 2834, 0)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 2836, 0)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 2991, 0)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 2993, 0)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 2995, 0)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 2997, 0)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 2999, 0)
filtered_clip = replace_frame_with_next(filtered_clip, 4770)
filtered_clip = replace_frame_with_next(filtered_clip, 8549)
filtered_clip = replace_frame_with_previous(filtered_clip, 11983)
filtered_clip = replace_frame_with_next(filtered_clip, 14093)
filtered_clip = replace_frame_with_next(filtered_clip, 16789)
filtered_clip = replace_frame_with_previous(filtered_clip, 18636)
filtered_clip = replace_frame_with_previous(filtered_clip, 22066)
filtered_clip = replace_frame_with_next(filtered_clip, 22190)
filtered_clip = replace_frame_with_next(filtered_clip, 22973)
filtered_clip = replace_frame_with_previous(filtered_clip, 30475)
filtered_clip = replace_frame_with_next(filtered_clip, 33924)
filtered_clip = replace_frame_with_previous(filtered_clip, 33968)

# Manual Smartfademod Start
fadefixed_clip = manual_smartfademod(filtered_clip, 2172, 2206)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 2828, 2839)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 2989, 3001)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 7365, 7388)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 8223, 8245)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 9379, 9414)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 11505, 11529)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 15071, 15094)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 15932, 15955)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 19523, 19546)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 20064, 20110)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 24903, 24938)
output_clip = manual_smartfademod(fadefixed_clip, 27452, 27498)
# Manual Smartfademod End

output_clip = fvf.Depth(output_clip, 10)

if DEBUG_MODE:
	output_clip = core.text.FrameProps(output_clip, props=['VDecimateDrop'])

output_clip.set_output()