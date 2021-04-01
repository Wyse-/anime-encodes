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
		return core.vivtc.VDecimate(matched_clip, ovr='./decimate_overrides/ep_17_vdecimate_override.txt', dupthresh=2.0, dryrun=True)
	else:
		return core.vivtc.VDecimate(matched_clip, ovr='./decimate_overrides/ep_17_vdecimate_override.txt', dupthresh=2.0)
		
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

source = core.lsmas.LWLibavSource(source='/home/wyse/Videos/NHK_NI_YOUKOSO_01/nhk_ep_17.mkv')
decimated_clip = ivtc_clip_ovr(source)	
filtered_clip = filter_clip(decimated_clip)
filtered_clip = replace_frame_with_next(filtered_clip, 323)
filtered_clip = replace_frame_with_next(filtered_clip, 2521)
filtered_clip = replace_frame_with_next(filtered_clip, 12295)
filtered_clip = replace_frame_with_next(filtered_clip, 18188)
filtered_clip = replace_frame_with_next(filtered_clip, 20291)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 27057)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 28837)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 28841)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 28845)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 28849)

# Manual Smartfademod Start
fadefixed_clip = manual_smartfademod(filtered_clip, 4420, 4429)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 5137, 5143)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 7945, 7951)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 8024, 8036)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 11565, 11571)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 11594, 11599)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 11622, 11628)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 14926, 14961)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 18452, 18464)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 24979, 25002)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 25525, 25549)
output_clip = manual_smartfademod(fadefixed_clip, 26899, 26912)
# Manual Smartfademod End

output_clip = fvf.Depth(output_clip, 10)

if DEBUG_MODE:
	output_clip = core.text.FrameProps(output_clip, props=['VDecimateDrop'])

output_clip.set_output()