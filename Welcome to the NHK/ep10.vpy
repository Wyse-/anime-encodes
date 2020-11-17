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
	nced_mod = core.std.Trim(clip, 0, frame - 1) + core.std.Trim(decombed_nced, frame - 29506)
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
		return core.vivtc.VDecimate(matched_clip, ovr='./decimate_overrides/ep_10_vdecimate_override.txt', dupthresh=2.0, dryrun=True)
	else:
		return core.vivtc.VDecimate(matched_clip, ovr='./decimate_overrides/ep_10_vdecimate_override.txt', dupthresh=2.0)
		
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

source = core.lsmas.LWLibavSource(source='/home/wyse/Videos/NHK_NI_YOUKOSO_01/nhk_ep_10.mkv')
nced = core.lsmas.LWLibavSource(source='/home/wyse/Videos/NHK_NI_YOUKOSO_01/nhk_ncop_nced.mkv')
decimated_clip = ivtc_clip_ovr(source)
filtered_clip = filter_clip(decimated_clip)
filtered_clip = replace_frame_with_next(filtered_clip, 323)
filtered_clip = replace_frame_with_previous(filtered_clip, 4988)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 9597)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 9602, 0)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 9604)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 9613)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 9614)
filtered_clip = replace_frame_with_next(filtered_clip, 17194)
filtered_clip = replace_frame_with_next(filtered_clip, 15748)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 26565)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 26571)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 26577)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 29783)
decimated_nced = ivtc_clip(nced)

# Manual Decombing Start
decombed_clip = decomb_clip_frame(filtered_clip, 32301 - 1, '32301_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32302 - 1, '32301_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32303 - 1, '32303_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32304 - 1, '32304_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32305 - 1, '32304_combmask.png')
decombed_clip = decomb_ed_frame_nced(decombed_clip, decimated_nced, 32442, 'ep10/32442_combmask.png')
decombed_clip = decomb_ed_frame_nced(decombed_clip, decimated_nced, 32443, 'ep10/32443_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32445 - 1, '32445_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32446 - 1, '32447_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32447 - 1, '32447_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32448 - 1, '32447_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32589 - 1, '32590_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32590 - 1, '32591_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32591 - 1, '32592_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32592 - 2, '32592_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32593 - 2, '32593_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32594 - 2, '32593_combmask.png')
# Manual Decombing End

# Manual Smartfademod Start
fadefixed_clip = manual_smartfademod(decombed_clip, 2170, 2199)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 2913, 2927)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 13556, 13561)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 13577, 13582)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 13597, 13602)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 16362, 16386)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 20504, 20528)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 26550, 26585)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 26903, 26920)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 29845, 29847)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 29711, 29716)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 29780, 29786)
output_clip = manual_smartfademod(fadefixed_clip, 29924, 29930)
# Manual Smartfademod End

output_clip = fvf.Depth(output_clip, 10)

if DEBUG_MODE:
	output_clip = core.text.FrameProps(output_clip, props=['VDecimateDrop'])

output_clip.set_output()