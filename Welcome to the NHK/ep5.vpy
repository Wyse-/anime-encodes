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
		return core.vivtc.VDecimate(matched_clip, ovr='./decimate_overrides/ep_5_vdecimate_override.txt', dupthresh=2.0, dryrun=True)
	else:
		return core.vivtc.VDecimate(matched_clip, ovr='./decimate_overrides/ep_5_vdecimate_override.txt', dupthresh=2.0)
		
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
	#rightdarkest_edge = 0
	#rightdark_edge = 1
	#rightbright_edge = 2
	#leftmost_edge = 3
	edgefix_value = f[1].props['PlaneStatsAverage'] - f[0].props['PlaneStatsAverage']
	
	if f[3].props['PlaneStatsAverage'] < 0.11 and edgefix_value > 0.009:
		clip_edgefix = core.std.SetFrameProp(clip_edgefix, prop='LeftLuma', floatval=f[3].props['PlaneStatsAverage'])
		clip_edgefix = core.std.SetFrameProp(clip_edgefix, prop='EdgeFix', floatval=edgefix_value)
		additional_diff = f[2].props['PlaneStatsAverage'] - f[1].props['PlaneStatsAverage']
		clip_edgefix = core.std.SetFrameProp(clip_edgefix, prop='EdgeFixAdditional', floatval=additional_diff)
		if additional_diff > 0.002:
			clip_edgefix_additional = core.std.SetFrameProp(clip_edgefix_additional, prop='LeftLuma', floatval=f[3].props['PlaneStatsAverage'])
			clip_edgefix_additional = core.std.SetFrameProp(clip_edgefix_additional, prop='EdgeFix', floatval=edgefix_value)
			clip_edgefix_additional = core.std.SetFrameProp(clip_edgefix_additional, prop='EdgeFixAdditional', floatval=additional_diff)
			return clip_edgefix_additional
		else:
			return clip_edgefix
	else:
		clip = core.std.SetFrameProp(clip, prop='LeftLuma', floatval=f[3].props['PlaneStatsAverage'])
		clip = core.std.SetFrameProp(clip, prop='EdgeFix', floatval=edgefix_value)
		return clip
		
def automated_edgefix(clip, unfiltered_clip):	
	rightdarkest_edge = mvf.GetPlane(unfiltered_clip, 0)
	rightdarkest_edge = rightdarkest_edge.std.CropAbs(width=1, height=rightdarkest_edge.height, left=717)
	rightdarkest_edge = rightdarkest_edge.std.PlaneStats()
	
	rightdark_edge = mvf.GetPlane(unfiltered_clip, 0)
	rightdark_edge = rightdark_edge.std.CropAbs(width=1, height=rightdark_edge.height, left=716)
	rightdark_edge = rightdark_edge.std.PlaneStats()	
	
	rightbright_edge = mvf.GetPlane(unfiltered_clip, 0)
	rightbright_edge = rightbright_edge.std.CropAbs(width=1, height=rightbright_edge.height, left=715)
	rightbright_edge = rightbright_edge.std.PlaneStats()
	
	leftmost_edge = mvf.GetPlane(unfiltered_clip, 0)
	leftmost_edge = leftmost_edge.std.CropAbs(width=1, height=leftmost_edge.height, left=0)
	leftmost_edge = leftmost_edge.std.PlaneStats()
	
	postprocessed_clip = core.std.FrameEval(clip, functools.partial(conditional_edgefix, clip=clip, clip_edgefix=edgefix_clip(clip), clip_edgefix_additional=edgefix_clip(clip, True)), prop_src=[rightdarkest_edge, rightdark_edge, rightbright_edge, leftmost_edge])
	return postprocessed_clip;
	

source = core.lsmas.LWLibavSource(source='/home/wyse/Videos/NHK_NI_YOUKOSO_01/nhk_ep_5.mkv')
nced = core.lsmas.LWLibavSource(source='/home/wyse/Videos/NHK_NI_YOUKOSO_01/nhk_ncop_nced.mkv')
decimated_clip = ivtc_clip_ovr(source)
filtered_clip = filter_clip(decimated_clip)

# Automated Edgefix Start
filtered_clip = automated_edgefix(filtered_clip, decimated_clip)
# Automated Edgefix End

filtered_clip = replace_frame_with_next(filtered_clip, 323)
filtered_clip = replace_frame_with_next(filtered_clip, 8211)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 8806)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 8807)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 8808)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 8809, 0)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 8810, 0)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 8811, 0)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 8812)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 8813)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 8814)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 8815)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 8816)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 8817)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 8819, 0)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 8821)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 8823, 0)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 8825)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 8827)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 9068)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 9070)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 9071)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 9073, 0)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 9075, 0)
filtered_clip = replace_frame_with_next(filtered_clip, 14190)
filtered_clip = replace_frame_with_next(filtered_clip, 19413)
decimated_nced = ivtc_clip(nced)

# Manual Decombing Start
decombed_clip = decomb_clip_frame(filtered_clip, 32301 - 1, '32301_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32302 - 1, '32301_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32303 - 1, '32303_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32304 - 1, '32304_combmask.png')
decombed_clip = decomb_clip_frame(decombed_clip, 32305 - 1, '32304_combmask.png')
decombed_clip = decomb_ed_frame_nced(decombed_clip, decimated_nced, 32442, 'ep5/32442_combmask.png')
decombed_clip = decomb_ed_frame_nced(decombed_clip, decimated_nced, 32443, 'ep5/32443_combmask.png')
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
fadefixed_clip = manual_smartfademod(decombed_clip, 2171, 2206)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 5676, 5688)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 7481, 7505)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 8805, 8829)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 9065, 9077)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 9125, 9137)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 13639, 13650)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 13710, 13722)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 16221, 16260)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 26144, 26148)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 26171, 26176)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 26194, 26198)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 26224, 26235)
output_clip = manual_smartfademod(fadefixed_clip, 28005, 28016)
# Manual Smartfademod End

output_clip = fvf.Depth(output_clip, 10)

if DEBUG_MODE:
	output_clip = core.text.FrameProps(output_clip, props=['VDecimateDrop', 'LeftLuma'])

output_clip = core.text.FrameProps(output_clip, props=['LeftLuma', 'EdgeFix', 'EdgeFixAdditional'])

output_clip.set_output()