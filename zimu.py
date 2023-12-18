#!/usr/bin/env python3
import sys
import pysubs2
from pysubs2 import Alignment, Color, SSAFile, SSAStyle 
from hanziconv import HanziConv
from pinyin_jyutping_sentence import pinyin, jyutping
ms = pysubs2.subrip.SubripFormat.ms_to_timestamp

"""
+===========================+
|          LAYER 8          |
|          LAYER 7          |
|          LAYER 6          |
|          LAYER 5          |
|                           |
|          LAYER 4          |
|          LAYER 3          |
|          LAYER 2          |
|          LAYER 1          |
+===========================+
"""

streams = {}
ssa = SSAFile()
ssa.styles = {
    "layer8": SSAStyle(alignment=Alignment.TOP_CENTER, primarycolor=Color(255, 255, 255), marginv=0),
    "layer7": SSAStyle(alignment=Alignment.TOP_CENTER, primarycolor=Color(0, 128, 128), marginv=24),
    "layer6": SSAStyle(alignment=Alignment.TOP_CENTER, primarycolor=Color(0, 128, 128), marginv=48),
    "layer5": SSAStyle(alignment=Alignment.TOP_CENTER, primarycolor=Color(0, 128, 128), marginv=72),
    "layer4": SSAStyle(alignment=Alignment.BOTTOM_CENTER, primarycolor=Color(0, 128, 128), marginv=72),
    "layer3": SSAStyle(alignment=Alignment.BOTTOM_CENTER, primarycolor=Color(200, 200, 100), marginv=48),
    "layer2": SSAStyle(alignment=Alignment.BOTTOM_CENTER, primarycolor=Color(200, 200, 100), marginv=24),
    "layer1": SSAStyle(alignment=Alignment.BOTTOM_CENTER, primarycolor=Color(200, 200, 200), marginv=0),
}

SA = []
c = -1
for a in sys.argv[1:]:
  if a.startswith('--'):
    SA.append({"option": a[2:], "params": []})
    c += 1
  else:
    SA[c]['params'].append(a)

def timestamp_to_sec(time_str):
  time_str = time_str.replace("," , ".")
  time_split = time_str.split(":")
  if len(time_split) == 3:
    return (int(time_split[0])*60*60) + (int(time_split[1])*60) + float(time_split[2]) 
  elif len(time_split) == 2:
    return (int(time_split[0])*60) + float(time_split[1]) 
  elif len(time_split) == 1:
    return float(time_split[0])
  else:
    raise Exception(f"cant parse time_str: {time_str}")

def add_to_ssa(stream, layer):
  for e in stream:
    e.text = e.text.replace('\\N', ' ')
    e.style = layer
    ssa.append(e)

for key, value in [(x['option'], x['params']) for x in SA]:
  if value and ("layer" in key or "hidden" in key):
    encoding = "utf-8"
    offset = 0
    scale = 1
    film_first = 0
    film_last = 0
    while len(value) != 0:
      if len(value) == 1:
        streams[key] = pysubs2.load(value[0], encoding)
        if film_last == 0:
          streams[key].shift(s=offset)
        else:
          offset_ms = film_first - streams[key][0].start
          streams[key].shift(ms=offset_ms)
          sos = streams[key][0].start #start offset 
          scale = film_last / streams[key][-1].end
          for e in streams[key]:
            for se in ["start", "end"]:
              t = getattr(e, se)
              spp = (t - sos) / (streams[key][-1].end - sos) # sub position percent
              nt = int(t + (t * ((scale - 1) * spp)))
              setattr(e, se, nt)
        if "layer" in key:
          add_to_ssa(streams[key], key)
        value.pop()
      elif value[0] == "encoding":
        encoding = value[1]
        value = value[2:]
      elif value[0] == "offset":
        offset = float(value[1])
        value = value[2:]
      elif value[0] == "scale":
        film_first = int(timestamp_to_sec(value[1]) * 1000)
        film_last = int(timestamp_to_sec(value[2]) * 1000)
        value = value[3:]
      elif value[0] == "convert":
        src_layer = streams[value[1]]
        convertion_type = value[2]
        if convertion_type == "simplified":
          counter = 0
          tmp_srt = ""
          for e in src_layer:
            counter += 1
            tmp_srt += f"{counter}\n{ms(e.start)} --> {ms(e.end)}\n{HanziConv.toSimplified(e.text)}\n\n"
          streams[key] = SSAFile.from_string(tmp_srt)
          add_to_ssa(streams[key], key)
          value = value[3:]
        elif convertion_type == "traditional":
          counter = 0
          tmp_srt = ""
          for e in src_layer:
            counter += 1
            tmp_srt += f"{counter}\n{ms(e.start)} --> {ms(e.end)}\n{HanziConv.toTraditional(e.text)}\n\n"
          streams[key] = SSAFile.from_string(tmp_srt)
          add_to_ssa(streams[key], key)
          value = value[3:]
        elif convertion_type == "pinyin":
          counter = 0
          tmp_srt = ""
          for e in src_layer:
            counter += 1
            tmp_srt += f"{counter}\n{ms(e.start)} --> {ms(e.end)}\n{pinyin(e.text)}\n\n"
          streams[key] = SSAFile.from_string(tmp_srt)
          add_to_ssa(streams[key], key)
          value = value[3:]
        elif convertion_type == "jyutping":
          counter = 0
          tmp_srt = ""
          for e in src_layer:
            counter += 1
            tmp_srt += f"{counter}\n{ms(e.start)} --> {ms(e.end)}\n{jyutping(e.text)}\n\n"
          streams[key] = SSAFile.from_string(tmp_srt)
          add_to_ssa(streams[key], key)
          value = value[3:]
        else:
          print(f"invalid conversion type: {convertion_type}")
          exit()
      else:
        print(f"invalid sub-command: {value[0]}")
        exit()

filename = next((x['params'][0] for x in SA if x['option'] == 'out'), None) 
with open(filename, "w") as f:
  ssa.to_file(fp=f, format_="ssa", header_notice="Generated with zimu: https://github.com/mai-gh/zimu\n" + " ".join([sys.argv[0].split('/')[-1], *sys.argv[1:]]))
