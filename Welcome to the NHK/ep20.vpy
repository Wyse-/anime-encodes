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
		return core.vivtc.VDecimate(matched_clip, ovr='./decimate_overrides/ep_20_vdecimate_override.txt', dupthresh=2.0, dryrun=True)
	else:
		return core.vivtc.VDecimate(matched_clip, ovr='./decimate_overrides/ep_20_vdecimate_override.txt', dupthresh=2.0)
		
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
	
def decomb_clip_whole_frame_interlaced_transition(clip, frame_start, frame_end, order=1):
	deint = core.tdm.TDeintMod(clip, order=order, edeint=core.nnedi3.nnedi3(clip, field=order), length=6, athresh=6)
	return core.std.Trim(clip, 0, frame_start - 1) + core.std.Trim(deint, frame_start, frame_end) + core.std.Trim(clip, frame_end + 1)

source = core.lsmas.LWLibavSource(source='/home/wyse/Videos/NHK_NI_YOUKOSO_01/nhk_ep_20.mkv')
decimated_clip = ivtc_clip_ovr(source)	
filtered_clip = filter_clip(decimated_clip)
filtered_clip = replace_frame_with_next(filtered_clip, 323)
filtered_clip = replace_frame_with_previous(filtered_clip, 4252)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 6757)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 6760)
filtered_clip = replace_frame_with_next(filtered_clip, 9455)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 13299)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 13301)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 13303)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 13305)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 13307)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 13309)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 13310)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 13311)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 13313)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 13314)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 13315)
filtered_clip = replace_frame_with_next(filtered_clip, 13539)
filtered_clip = replace_frame_with_previous(filtered_clip, 14222)
filtered_clip = replace_frame_with_previous(filtered_clip, 15474)
filtered_clip = replace_frame_with_previous(filtered_clip, 19699)
filtered_clip = replace_frame_with_next(filtered_clip, 20840)
filtered_clip = replace_frame_with_previous(filtered_clip, 21213)
filtered_clip = replace_frame_with_next(filtered_clip, 21407)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 22132, 0)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 22139)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 22183)
filtered_clip = replace_frame_with_previous(filtered_clip, 25680)
filtered_clip = replace_frame_with_next(filtered_clip, 25876)
filtered_clip = replace_frame_with_previous(filtered_clip, 28307)
filtered_clip = replace_frame_with_previous(filtered_clip, 28568)
filtered_clip = replace_frame_with_next(filtered_clip, 28909)
filtered_clip = replace_frame_with_next(filtered_clip, 33806)

# TODO: there may be a better way to handle the combed line during transition in frames 18472-18507
filtered_clip = decomb_clip_whole_frame_interlaced_transition(filtered_clip, 18472, 18507)

# Manual Smartfademod Start
fadefixed_clip = manual_smartfademod(filtered_clip, 2170, 2195)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 4930, 4935)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 6340, 6363)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 6459, 6482)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 7126, 7150)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 7264, 7287)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 7417, 7452)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 8372, 8395)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 13296, 13317)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 14427, 14450)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 15251, 15274)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 17490, 17514)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 27597, 27603)
output_clip = manual_smartfademod(fadefixed_clip, 27802, 27813)

# Manual Smartfademod End

output_clip = fvf.Depth(output_clip, 10)

if DEBUG_MODE:
	output_clip = core.text.FrameProps(output_clip, props=['VDecimateDrop'])

output_clip.set_output()