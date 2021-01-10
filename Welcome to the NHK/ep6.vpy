import vapoursynth as vs
from vapoursynth import core
import fvsfunc as fvf
import havsfunc as haf
import mvsfunc as mvf
import functools

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
		return core.vivtc.VDecimate(matched_clip, ovr='./decimate_overrides/ep_6_vdecimate_override.txt', dupthresh=2.0, dryrun=True)
	else:
		return core.vivtc.VDecimate(matched_clip, ovr='./decimate_overrides/ep_6_vdecimate_override.txt', dupthresh=2.0)
		
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

def edgefix_clip(clip, additional=False):
	filterable_clip = fvf.Depth(clip, 16)
	fixed_edge_clip = haf.FixColumnBrightnessProtect2(filterable_clip, 713, 22)
	if additional:
		fixed_edge_clip = haf.FixColumnBrightnessProtect2(fixed_edge_clip, 712, 2)
		fixed_edge_clip = haf.FixColumnBrightnessProtect2(fixed_edge_clip, 711, -2, 6)
	filtering_done_clip = fvf.Depth(fixed_edge_clip, 8)
	return filtering_done_clip;

def conditional_edgefix(n, f, clip, clip_edgefix, clip_edgefix_additional):
	if f[0].props['PlaneStatsAverage'] < 0.07 or f[0].props['PlaneStatsAverage'] < 0.11 and f[1].props['PlaneStatsAverage'] < 0.3:
		clip_edgefix = core.std.SetFrameProp(clip_edgefix, prop='LeftLuma', floatval=f[0].props['PlaneStatsAverage'])
		clip_edgefix = core.std.SetFrameProp(clip_edgefix, prop='RightLuma', floatval=f[1].props['PlaneStatsAverage'])
		clip_edgefix = core.std.SetFrameProp(clip_edgefix, prop='EdgeFix', intval=1)
		additional_diff = f[3].props['PlaneStatsAverage'] - f[2].props['PlaneStatsAverage']
		clip_edgefix = core.std.SetFrameProp(clip_edgefix, prop='EdgeFixAdditional', floatval=additional_diff)
		if additional_diff > 0.002:
			clip_edgefix_additional = core.std.SetFrameProp(clip_edgefix_additional, prop='LeftLuma', floatval=f[0].props['PlaneStatsAverage'])
			clip_edgefix_additional = core.std.SetFrameProp(clip_edgefix_additional, prop='RightLuma', floatval=f[1].props['PlaneStatsAverage'])
			clip_edgefix_additional = core.std.SetFrameProp(clip_edgefix_additional, prop='EdgeFix', intval=1)
			clip_edgefix_additional = core.std.SetFrameProp(clip_edgefix_additional, prop='EdgeFixAdditional', floatval=additional_diff)
			return clip_edgefix_additional
		else:
			return clip_edgefix
	else:
		clip = core.std.SetFrameProp(clip, prop='LeftLuma', floatval=f[0].props['PlaneStatsAverage'])
		clip = core.std.SetFrameProp(clip, prop='RightLuma', floatval=f[1].props['PlaneStatsAverage'])
		clip = core.std.SetFrameProp(clip, prop='EdgeFix', intval=0)
		return clip

def automated_edgefix(clip, unfiltered_clip):
	leftmost_edge = mvf.GetPlane(unfiltered_clip, 0)
	leftmost_edge = leftmost_edge.std.CropAbs(width=1, height=leftmost_edge.height, left=0)
	leftmost_edge = leftmost_edge.std.PlaneStats()
	
	rightmost_edge = mvf.GetPlane(unfiltered_clip, 0)
	rightmost_edge = rightmost_edge.std.CropAbs(width=1, height=leftmost_edge.height, left=719)
	rightmost_edge = rightmost_edge.std.PlaneStats()
	
	rightdark_edge = mvf.GetPlane(unfiltered_clip, 0)
	rightdark_edge = rightdark_edge.std.CropAbs(width=1, height=leftmost_edge.height, left=716)
	rightdark_edge = rightdark_edge.std.PlaneStats()	
	
	rightbright_edge = mvf.GetPlane(unfiltered_clip, 0)
	rightbright_edge = rightbright_edge.std.CropAbs(width=1, height=leftmost_edge.height, left=715)
	rightbright_edge = rightbright_edge.std.PlaneStats()
	
	postprocessed_clip = core.std.FrameEval(output_clip, functools.partial(conditional_edgefix, clip=output_clip, clip_edgefix=edgefix_clip(output_clip), clip_edgefix_additional=edgefix_clip(output_clip, True)), prop_src=[leftmost_edge, rightmost_edge, rightdark_edge, rightbright_edge])
	return postprocessed_clip;

source = core.lsmas.LWLibavSource(source='/home/wyse/Videos/NHK_NI_YOUKOSO_01/nhk_ep_6.mkv')
nced = core.lsmas.LWLibavSource(source='/home/wyse/Videos/NHK_NI_YOUKOSO_01/nhk_ncop_nced.mkv')
decimated_clip = ivtc_clip_ovr(source)
filtered_clip = filter_clip(decimated_clip)
filtered_clip = replace_frame_with_next(filtered_clip, 323)
filtered_clip = replace_frame_with_next(filtered_clip, 8810)
filtered_clip = replace_frame_with_next(filtered_clip, 8831)
filtered_clip = replace_frame_with_next(filtered_clip, 12045)
filtered_clip = replace_frame_with_next(filtered_clip, 24634)
filtered_clip = replace_frame_with_next(filtered_clip, 26062)
filtered_clip = replace_frame_with_next(filtered_clip, 33817)
decimated_nced = ivtc_clip(nced)

# Manual Decombing Start
decombed_clip = decomb_clip_frame(filtered_clip, 32301 - 1, '32301_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32302 - 1, '32301_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32303 - 1, '32303_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32304 - 1, '32304_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32305 - 1, '32304_combmask.png')
decombed_clip = decomb_ed_frame_nced(decombed_clip, decimated_nced, 32442, 'ep6/32442_combmask.png')
decombed_clip = decomb_ed_frame_nced(decombed_clip, decimated_nced, 32443, 'ep6/32443_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32445 - 1, '32445_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32446 - 1, '32447_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32447 - 1, '32447_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32448 - 1, '32447_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32589 - 1, '32589_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32590 - 1, '32590_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32591 - 1, '32590_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32592 - 1, '32593_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32593 - 1, '32593_combmask.png')
# Manual Decombing End

# Manual Smartfademod Start
fadefixed_clip = manual_smartfademod(decombed_clip, 20214, 20249)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 26779, 26784)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 2171, 2194)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 3625, 3643)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 3865, 3876)
output_clip = manual_smartfademod(fadefixed_clip, 28005, 28016)
# Manual Smartfademod End

# Automated Edgefix Start
output_clip = automated_edgefix(output_clip, decimated_clip)
# Automated Edgefix End

output_clip = fvf.Depth(output_clip, 10)

if DEBUG_MODE:
	output_clip = core.text.FrameProps(output_clip, props=['VDecimateDrop', 'LeftLuma'])
	
output_clip = core.text.FrameProps(output_clip, props=['LeftLuma', 'RightLuma', 'EdgeFix', 'EdgeFixAdditional'])

output_clip.set_output()