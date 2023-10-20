# zimu

## multi-language subtitle joiner


### how to use:

- You want to watch a film from taiwan that you have english and traditional chinese subtitles for, but you want english, pinyin, simplified chinese and traditional chinese characters to be displayed:
```
.zimu.py --layer1 cn.srt --layer2 convert layer1 simplified --layer3 convert layer1 pinyin --layer4 en.srt --out out.ssa
```


- You want to watch a film from shanghai that you have english and simplified subtitles, but you want english, pinyin and simplified chinese characters to be displayed. this example also shows how to rescale off synced subtitles, the first timestamp is the start of the first subtitle, and the second timestamp is the end of the last subtitle
```
./zimu.py --layer1 encoding gb2312 scale 0:02:45.05 1:45:22 chs.srt --layer2 convert layer1 pinyin --layer3 scale 0:00:32 1:45:22  en.srt --out out.ssa
```

- You want to watch a film from hongkong that you have english and traditional subtitles, but you want english, traditional chinese characters and jyutping to be displayed

```
.zimu.py --layer1 cn.srt --layer2 convert layer1 jyutping --layer3 en.srt --out out.ssa
```
