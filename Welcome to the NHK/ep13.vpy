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
		return core.vivtc.VDecimate(matched_clip, ovr='./decimate_overrides/ep_13_vdecimate_override.txt', dupthresh=2.0, dryrun=True)
	else:
		return core.vivtc.VDecimate(matched_clip, ovr='./decimate_overrides/ep_13_vdecimate_override.txt', dupthresh=2.0)
		
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

source = core.lsmas.LWLibavSource(source='/home/wyse/Videos/NHK_NI_YOUKOSO_01/nhk_ep_13.mkv')
decimated_clip = ivtc_clip_ovr(source)
filtered_clip = filter_clip(decimated_clip)
filtered_clip = replace_frame_with_next(filtered_clip, 323)
filtered_clip = replace_frame_with_next(filtered_clip, 11501)
filtered_clip = replace_frame_with_previous(filtered_clip, 12246)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 15355)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 15359)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 15363)
filtered_clip = replace_frame_with_next(filtered_clip, 18425)
filtered_clip = replace_frame_with_previous(filtered_clip, 27494)
filtered_clip = replace_frame_with_next(filtered_clip, 28682)
filtered_clip = replace_frame_with_next(filtered_clip, 28929)
filtered_clip = replace_frame_with_previous(filtered_clip, 30469)
filtered_clip = replace_frame_with_previous(filtered_clip, 30956)
filtered_clip = replace_frame_with_previous(filtered_clip, 31296)

# Manual Smartfademod Start
fadefixed_clip = manual_smartfademod(filtered_clip, 2172, 2213)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 5501, 5507)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 7979, 8021)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 17985, 17993)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 18033, 18056)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 19712, 19724)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 19726, 19733)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 19755, 19775)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 19797, 19818)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 19840, 19860)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 19882, 19902)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 22552, 22559)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 22692, 22703)
output_clip = manual_smartfademod(fadefixed_clip, 30271, 30306)
# Manual Smartfademod End

output_clip = fvf.Depth(output_clip, 10)

if DEBUG_MODE:
	output_clip = core.text.FrameProps(output_clip, props=['VDecimateDrop'])

output_clip.set_output()