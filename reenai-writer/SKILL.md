---
name: reenai-writer
description: Reen 的个人写作风格 Skill。用 Reen 的声音写作、改稿、跨平台改编（公众号、视频口播与脚本、小红书、随笔、简介和各类文案），讨论选题，以及记录反馈、归纳并更新这份风格。用户说「按我的风格写」「帮我写篇」「把这些想法写出来」「改一下」「废话太多」「改成口播」「记下这条反馈」「归纳一下我的风格」时使用。
---

# ReenAI Writer

把 Reen 想说的东西写成 Reen 自己的话，并让这份风格随每次合作变得更准。

```
voice/        个人声音，换成别人的就是别人的 skill
  profile.md    风格画像，写作前必读
  samples/      原文、亲改对照、认可稿
  checks.txt    自检词表
references/   通用方法，formats.md 形式，visual.md 配图
evolution/    迭代记录，写作时不用读
scripts/      check.py 自检脚本
```

## 写作

1. 读 [voice/profile.md](voice/profile.md)，看清这次的用途、读者和长度。用户这次说的要求优先于画像。
2. 按题材选语气档位（见画像），形式要求读 [formats.md](references/formats.md) 对应的一节。语气拿不准时，从 [samples](voice/samples/README.md) 里挑一篇同档位的读一读。
3. 用作者给的材料、经历和判断来写，外部事实需要就去查。作者没讲过的亲身经历和感受不要替作者补，缺了就问一句，或者在正文后注明哪里需要补。
4. 从具体的事、人或判断开始，顺着读者需要的顺序讲。把作者为什么这样选、哪里觉得有意思、哪里还有疑问讲出来，比整理通用结论重要。
5. 写完跑一遍自检，然后通读，看每段有没有新东西、结尾是不是在重复前文。

   ```bash
   python3 -I scripts/check.py 稿件.md
   ```

6. 默认交一份成品。需要说明的假设或缺口，在正文后写一两行。

**改稿**只动要改的范围，作者原话里有效的部分保留。**跨平台改编**按新平台重新取重点和顺序，不是截短或断行。**选题讨论**给建议、理由和提纲，作者要全文时再写。**配图、封面、分镜**读 [visual.md](references/visual.md)。

## 迭代

每次合作都顺手做，不用先问。

- 作者提了修改意见，或者亲手改了稿，在 [feedback-log.md](evolution/feedback-log.md) 追加一条，写日期、场景、原话或改动对照，以及你看出的规律。
- 作者认可了一稿，或者给了自己写的文字，存进 `voice/samples/`，标上类型，并更新样本索引。
- 同一个规律出现两次以上、作者说「以后都这样」，或者作者让你「归纳一下」时，更新 profile.md，在 [CHANGELOG.md](evolution/CHANGELOG.md) 记一行，再告诉作者改了哪几条。

怎么归纳、证据怎么分级、怎么把这套东西分享给别人，见 [PROCESS.md](evolution/PROCESS.md)。
