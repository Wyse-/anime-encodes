import vapoursynth as vs
from vapoursynth import core
import fvsfunc as fvf
import havsfunc as haf

DEBUG_MODE = False

def decomb_clip_credits(clip, mask_file):
	combmask = core.resize.Point(core.lsmas.LWLibavSource(source='./combmasks/' + mask_file), format=vs.GRAY8, matrix_s="170m").std.Binarize(180, v0=0, v1=255)
	decombed_clip = core.tdm.TDeintMod(clip, order=1, edeint=core.nnedi3.nnedi3(clip, field=1))
	merged_clip = core.std.MaskedMerge(clip, decombed_clip, combmask)
	return merged_clip

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
		return core.vivtc.VDecimate(matched_clip, ovr='./decimate_overrides/ep_23_vdecimate_override.txt', dupthresh=2.0, dryrun=True)
	else:
		return core.vivtc.VDecimate(matched_clip, ovr='./decimate_overrides/ep_23_vdecimate_override.txt', dupthresh=2.0)
		
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

source = core.lsmas.LWLibavSource(source='/home/wyse/Videos/NHK_NI_YOUKOSO_01/nhk_ep_23.mkv')
main_ep = core.std.Trim(source, 0, 40186)
credits = core.std.Trim(source, 40186, 42099)
preview = core.std.Trim(source, 42099, 42587)

decimated_clip_main = ivtc_clip_ovr(main_ep)
decimated_clip_preview = ivtc_clip_ovr(preview)
clip_credits = core.vivtc.VFM(credits, 1)
filtered_clip_credits = filter_clip(clip_credits)
decimated_clip_main = filter_clip(decimated_clip_main)
filtered_clip_preview = filter_clip(decimated_clip_preview)

clip_main = core.std.AssumeFPS(decimated_clip_main, fpsnum=24000,fpsden=1001)
clip_credits = core.std.AssumeFPS(filtered_clip_credits, fpsnum=30000,fpsden=1001)
# TODO: there may be a better way to deinterlace the 29.970fps credits
clip_credits = decomb_clip_credits(clip_credits, "credits_combmask_ep23.png")
clip_preview = core.std.AssumeFPS(filtered_clip_preview, fpsnum=24000,fpsden=1001)
full_clip = clip_main + clip_credits + clip_preview

full_clip = replace_frame_with_next(full_clip, 323)
full_clip = replace_frame_with_previous(full_clip, 10200)
full_clip = decomb_clip_whole_frame(full_clip, 15935)
full_clip = replace_frame_with_previous(full_clip, 20034)
full_clip = replace_frame_with_previous(full_clip, 22320)
full_clip = replace_frame_with_next(full_clip, 23349)
full_clip = decomb_clip_whole_frame(full_clip, 25962)
full_clip = replace_frame_with_previous(full_clip, 26285)
full_clip = replace_frame_with_previous(full_clip, 26467)
full_clip = replace_frame_with_next(full_clip, 29733)
full_clip = replace_frame_with_next(full_clip, 29580)
full_clip = replace_frame_with_next(full_clip, 31686)
full_clip = replace_frame_with_next(full_clip, 31278)
full_clip = decomb_clip_whole_frame(full_clip, 32172)
full_clip = decomb_clip_whole_frame(full_clip, 32294)
full_clip = decomb_clip_whole_frame(full_clip, 32463)
full_clip = replace_frame_with_previous(full_clip, 34264)

# Manual Smartfademod Start
fadefixed_clip = manual_smartfademod(full_clip, 9923, 9970)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 19529, 19564)
fadefixed_clip = manual_smartfademod(fadefixed_clip, 26868, 26903)
output_clip = manual_smartfademod(fadefixed_clip, 26928, 26951)
# Manual Smartfademod End

output_clip = fvf.Depth(output_clip, 10)

if DEBUG_MODE:
	output_clip = core.text.FrameProps(output_clip, props=['VDecimateDrop'])

output_clip.set_output()