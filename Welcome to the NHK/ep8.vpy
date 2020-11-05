import vapoursynth as vs
from vapoursynth import core
import fvsfunc as fvf
import havsfunc as haf

DEBUG_MODE = False

def decomb_clip_frame(clip, frame, mask_file):
	combmask = core.resize.Point(core.lsmas.LWLibavSource(source='./combmasks/' + mask_file), format=vs.GRAY8, matrix_s="170m").std.Binarize(180, v0=0, v1=255)
	decombed_clip = core.eedi3.eedi3(clip, 1)
	merged_clip = core.std.MaskedMerge(clip, decombed_clip, combmask)
	return core.std.Trim(clip, 0, frame - 1) + core.std.Trim(merged_clip, frame, frame) + core.std.Trim(clip, frame + 1)
	
def decomb_ed_frame_nced(clip, nced_clip, frame, mask_file):
	decombed_nced = filter_clip(core.eedi3.eedi3(nced_clip, 1), True)
	nced_mod = core.std.Trim(clip, 0, frame - 1) + core.std.Trim(decombed_nced, frame - 29505)
	combmask = core.resize.Point(core.lsmas.LWLibavSource(source='./combmasks/' + mask_file), format=vs.GRAY8, matrix_s="170m").std.Binarize(180, v0=0, v1=255)
	merged_clip = core.std.MaskedMerge(clip, nced_mod, combmask)
	return core.std.Trim(clip, 0, frame - 1) + core.std.Trim(merged_clip, frame, frame) + core.std.Trim(clip, frame + 1)
	
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
		return core.vivtc.VDecimate(matched_clip, ovr='./decimate_overrides/ep_8_vdecimate_override.txt', dupthresh=2.0, dryrun=True)
	else:
		return core.vivtc.VDecimate(matched_clip, ovr='./decimate_overrides/ep_8_vdecimate_override.txt', dupthresh=2.0)
		
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
	fixed_edge_clip = haf.FixColumnBrightnessProtect2(cropped_clip, 713, 22)
	fixed_edge_clip = haf.FixColumnBrightnessProtect2(fixed_edge_clip, 712, 2)
	fixed_edge_clip = haf.FixColumnBrightnessProtect2(fixed_edge_clip, 711, -2, 6)
	filtering_done_clip = fvf.Depth(fixed_edge_clip, 8)				
	return filtering_done_clip;
	
def decomb_clip_whole_frame(clip, frame, order=1):
	deint = core.tdm.TDeintMod(clip, order=order, edeint=core.nnedi3.nnedi3(clip, field=order))
	return core.std.Trim(clip, 0, frame - 1) + core.std.Trim(deint, frame, frame) + core.std.Trim(clip, frame + 1)

source = core.lsmas.LWLibavSource(source='/home/wyse/Videos/NHK_NI_YOUKOSO_01/nhk_ep_8.mkv')
nced = core.lsmas.LWLibavSource(source='/home/wyse/Videos/NHK_NI_YOUKOSO_01/nhk_ncop_nced.mkv')
decimated_clip = ivtc_clip_ovr(source)
filtered_clip = filter_clip(decimated_clip)
filtered_clip = replace_frame_with_next(filtered_clip, 323)
filtered_clip = replace_frame_with_next(filtered_clip, 27362)
decimated_nced = ivtc_clip(nced)

# Manual Decombing Start
decombed_clip = decomb_clip_frame(filtered_clip, 32301 - 2, '32301_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32302 - 2, '32301_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32303 - 2, '32303_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32304 - 2, '32304_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32305 - 2, '32304_combmask.png')
decombed_clip = decomb_ed_frame_nced(decombed_clip, decimated_nced, 32441, 'ep8/32441_combmask.png')
decombed_clip = decomb_ed_frame_nced(decombed_clip, decimated_nced, 32442, 'ep8/32442_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32445 - 2, '32445_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32446 - 2, '32447_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32447 - 2, '32447_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32448 - 2, '32447_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32589 - 2, '32589_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32590 - 2, '32590_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32591 - 2, '32590_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32592 - 2, '32593_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32593 - 2, '32593_combmask.png')
# Manual Decombing End

# Manual Smartfademod Start
fadefixed_clip = manual_smartfademod(decombed_clip, 2170, 2194)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 15617, 15666)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 23380, 23404)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 23838, 23856)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 28052, 28075)
output_clip = manual_smartfademod(fadefixed_clip, 31016, 31051)
# Manual Smartfademod End

output_clip = fvf.Depth(output_clip, 10)

if DEBUG_MODE:
	output_clip = core.text.FrameProps(output_clip, props=['VDecimateDrop'])

output_clip.set_output()