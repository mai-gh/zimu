# zimu

#### Multi-language subtitle joiner specifically targeting chinese variantion conversions (traditional, simplified, pinyin, jyutping).

<img src=example.jpg style="display: table; margin: 0 auto;" />

---

### How to use:

#### Layout:

<img src=layout.jpg style="display: table; margin: 0 auto;" />

#### Top-level arguments:

```
--hidden1
--hidden2
--hidden3
--hidden4

--layer1
--layer2
--layer3
--layer4
--layer5
--layer6
--layer7
--layer8

--out
```

#### Sub-commands for `--hiddenX` and `--layerX`:


- `encoding`
  - Description: Specify the encoding for the input subtitle file.
  - Example: `encoding utf-16`
  - Example: `encoding gb2312`


- `offset`
  - Description: Specify shifting forwards or backwards in seconds.
  - Example: `offset 4`
  - Example: `offset -2.25`


- `scale`
  - Description: Fix subtitles that scew due to fps mismatch. The first parameter is the begining of the first subtitle, the second parameter is the end of the last subtitle. Timestamp is in `hh:mm:ss.ms` format.
  - Example: `scale 0:02:45.05 1:45:22`
  - Example: `scale 2:45.05 1:45:22`


- `{target}`
  - Description: Subtitle file to load. **Required to be last** for: `encoding`, `offset`, `scale`.
  - Example: `cnt.srt`


- `convert`
  - Description: Convert an existing layer into a translated new layer. The first parameter is the source layer, the second parameter is how how to convert.
  - Example: `convert layer1 simplified`
  - Example: `convert layer1 traditional`
  - Example: `convert layer1 pinyin`
  - Example: `convert layer1 jyutping`




### Examples
- You want to watch a film from taiwan that you have english and traditional chinese subtitles for, but you want english, pinyin, simplified chinese characters to be displayed:

```
./zimu.py --hidden1 cnt.srt --layer1 convert hidden1 simplified --layer2 convert hidden1 pinyin --layer3 en.srt --out out.ssa

```

- You want to watch a film from shanghai that you have english and simplified chinese subtitles, but you want english, pinyin and simplified chinese characters to be displayed. this example also shows how to rescale off synced subtitles, the first timestamp is the start of the first subtitle, and the second timestamp is the end of the last subtitle

```
./zimu.py --layer1 encoding gb2312 scale 0:02:45.05 1:45:22 chs.srt --layer2 convert layer1 pinyin --layer3 scale 0:00:32 1:45:22  en.srt --out out.ssa
```

- You want to watch a film from hongkong that you have english and traditional subtitles, but you want english, traditional chinese characters and jyutping to be displayed

```
./zimu.py --layer1 cn.srt --layer2 convert layer1 jyutping --layer3 en.srt --out out.ssa
```
