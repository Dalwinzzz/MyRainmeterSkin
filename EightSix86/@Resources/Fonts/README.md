# 字体目录 · @Resources/Fonts

v5 设计稿用了 3 个非 Windows 自带字体，**随皮肤包分发**到本目录，各 `.ini`
通过 `[Rainmeter]` 段或 meter 的 `FontFile=#@#Fonts\xxx.ttf` 本地引用 —— 用户**无需手动安装字体**。

## 需要放入本目录的字体文件

| 文件名 (ini 里引用的名字) | 字体 | 用途 | 下载 |
|---|---|---|---|
| `Oxanium-Light.ttf` | Oxanium Light | 时钟大字 | Google Fonts: Oxanium |
| `Oxanium-SemiBold.ttf` | Oxanium SemiBold | 标题/编号/数值 | 同上 |
| `ChakraPetch-Medium.ttf` | Chakra Petch Medium | 标签/表格/单位 | Google Fonts: Chakra Petch |
| `ChakraPetch-SemiBold.ttf` | Chakra Petch SemiBold | 区块标题 | 同上 |
| `NotoSansSC-Regular.otf` | Noto Sans SC | 中文(星期/月份/歌词) | Google Fonts: Noto Sans SC |

> 这些都是 **开源字体 (SIL OFL)**，可自由随包分发。
> 下载：https://fonts.google.com/ 搜对应名字 → Download family → 取上述字重的文件改成上表文件名放进本目录。

## 为什么不直接提交字体二进制

- 字体文件较大（Noto Sans SC 全集 ~10MB+），仓库里只放说明；
- 建议用 **Noto Sans SC 子集**（只保留常用汉字）压到几百 KB，减小包体。

## 缺字体时的兜底

`Variables.inc` 里每个字体都配了 `FontFace` 兜底：
- Oxanium / Chakra Petch 缺失 → 回退 **Bahnschrift**(Win10/11 自带)
- Noto Sans SC 缺失 → 回退 **Microsoft YaHei UI**(自带)

所以即使本目录为空，皮肤也能加载渲染，只是字形换成 Windows 自带字体（视觉略有差异，不会崩）。
要 100% 还原 v5 预览效果，请按上表放入字体文件。
