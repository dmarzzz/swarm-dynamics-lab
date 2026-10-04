"""Transcode a measured GIF replay to the repository's required film format."""
import argparse,subprocess
p=argparse.ArgumentParser();p.add_argument('gif');p.add_argument('mp4');a=p.parse_args()
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',a.gif,'-f','lavfi','-i','anullsrc=channel_layout=stereo:sample_rate=48000','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-shortest','-movflags','+faststart',a.mp4],check=True)
