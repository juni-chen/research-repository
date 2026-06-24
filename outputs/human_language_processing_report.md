# 人間の言語処理メカニズムに関する研究レポート

作成日: 2026-06-24  
対象: 音声・文字・手話を含む人間の言語理解、言語産出、会話処理の神経・認知メカニズム

## 要旨

人間の言語処理研究は、19世紀の失語症例に基づく「Broca野=産出、Wernicke野=理解」という局在論から出発した。しかし現在の知見では、言語は単一部位ではなく、左半球優位の前頭・側頭・頭頂領域を中心とする分散ネットワークによって支えられる。さらに、この中核的な言語ネットワークは、聴覚・視覚・運動などの低次入出力系、記憶・推論・社会認知などの高次認知系と協調するが、それらとは機能的に区別される。

近年の大きな進展は三つある。第一に、個人別fMRI、ECoG、自然会話データにより、実験室的な短文処理だけでなく、実際の会話中の理解・産出・話者交替が解析できるようになった。第二に、脳は受動的に単語を積み上げるだけでなく、複数の時間スケールで次の語、構文、意味、談話文脈を予測していることが明確になってきた。第三に、大規模言語モデルや音声認識モデルの内部表現を使うことで、単語、文、会話内容と神経活動を同じ計算空間で比較できるようになった。ただし、モデルと脳の対応は有用な計算的近似であり、LLMが人間と同じように理解・推論していることを意味するわけではない。

本レポートの結論は、現代的な言語処理観を次のようにまとめられる。人間の言語処理は、入力信号の解析、語彙アクセス、構文・意味の合成、予測、記憶、発話計画、社会的意図理解が、時間的に重なり合いながら進む分散的・予測的・相互作用的なプロセスである。

## 1. 歴史的背景

### 1.1 古典的局在論

19世紀の神経心理学は、脳損傷と失語症状の対応から言語機能を推定した。Brocaは発話困難を示した患者の左前頭葉病変を報告し、言語産出と左前頭葉の関連を示した。Wernickeは、流暢だが意味理解が障害される失語を左後方側頭領域と結びつけ、さらに前方と後方の言語中枢を結ぶ連絡路の損傷という考えを提示した。これが後のWernicke-Lichtheim-Geschwind型モデルにつながった。

この時代の貢献は、言語が脳に局在するという発想を確立した点にある。一方で、現代のデータから見ると「Broca野」「Wernicke野」は単一機能を持つ固定的な中枢ではない。発話、統語、作業記憶、意味、音韻、運動計画は広いネットワークにまたがる。

### 1.2 心理言語学とオンライン処理

20世紀後半には、行動実験、反応時間、眼球運動、ERPにより、言語処理の時間展開が研究された。語彙認識では、複数候補が同時に活性化し文脈と競合しながら絞られるという考えが広まった。代表例として、音声単語認識のCohort model、TRACE model、文処理のガーデンパス理論、相互作用的制約充足モデルがある。

ERP研究では、意味的逸脱に対するN400、統語・再解析に関連するP600が、語彙意味処理と構文処理の時間的指標として重要になった。特にKutasとHillyardのN400研究は、脳が文脈から語の意味的適合性を非常に早く評価することを示した。

### 1.3 神経画像とネットワーク論

1990年代以降、PET、fMRI、MEG、ECoG、拡散MRIにより、言語処理は前頭葉と側頭葉の複数領域を結ぶネットワークとして再構成された。HickokとPoeppelの二経路モデルでは、腹側経路が音声・文字入力を意味へ写像し、背側経路が音韻表象と発話運動表象を結びつけるとされた。これは古典的な「Broca/Wernicke二中枢」よりも柔軟で、理解、復唱、発話、音韻作業記憶を説明しやすい。

2010年代以降は、集団平均だけでなく個人ごとの機能局在を同定する方法が重視されるようになった。言語ネットワークは個人差が大きいため、個人別の局在化は、機能選択性やネットワーク内の役割分担を理解する上で重要である。

## 2. 現代的な処理アーキテクチャ

### 2.1 低次の入力・出力系

音声理解では、聴覚皮質が音響特徴を処理し、音素、音節、韻律、語形へと情報が抽象化される。読字では、視覚野と腹側側頭領域が文字列を処理し、手話では視覚・運動関連領域が重要になる。発話産出では、語彙選択、音韻符号化、発声運動計画、呼吸・喉頭・口腔運動が連携する。

重要なのは、これらの低次系は言語入力の表面特徴に強く反応するが、それだけで文や談話の意味を担うわけではない点である。現代のレビューでは、低次知覚・運動系、中核的言語ネットワーク、推論・社会認知系を分けて考える枠組みが提案されている。

### 2.2 中核的言語ネットワーク

近年の代表的な整理では、中核的言語ネットワークは左半球の下前頭回、中前頭回、上・中側頭回、前側頭、角回周辺などを含む。Fedorenkoらの2024年レビューは、このネットワークが入力モダリティや出力モダリティを超えて言語に選択的であり、語彙アクセスと構成的意味処理を支えると整理している。

このネットワークは「文法だけ」「意味だけ」のように単純分業しているのではなく、語彙、構文、意味統合に広く関与する。構文処理は特定の単一領域に閉じるより、言語ネットワーク全体に分散しているという見方が強い。

### 2.3 知識・推論・社会認知との接続

言語使用では、言語ネットワークだけでなく、世界知識、記憶、注意、実行制御、心の理論、デフォルトモードネットワークも関与する。たとえば皮肉、含意、比喩、語用論、会話の意図理解では、話者の信念や文脈モデルが必要になる。

ただし、近年の議論では、言語システムと汎用的思考システムは重なる部分を持ちながらも同一ではないと考えられている。Fedorenko、Piantadosi、Gibsonは2024年のNature論文で、言語は複雑な思考の前提条件というより、思考を他者へ伝達する強力なコミュニケーション道具だと論じた。

## 3. 主要な計算メカニズム

### 3.1 語彙アクセス

語を聞く・読むとき、脳は入力を一語ずつ確定的に解読しているのではなく、音韻、綴字、語頻度、文脈、意味的期待を使って複数候補を同時に評価する。音声では、語頭から候補集合が形成され、後続音と文脈によって候補が削られる。読字では、視覚的単語形、音韻、意味が相互に活性化する。

この過程は逐次的であると同時に相互作用的である。低次入力だけでなく、話題、構文、意味、予測が語の認識速度と正確性に影響する。

### 3.2 構文・意味の合成

文理解では、単語の意味を足し合わせるだけでなく、語順、格、依存関係、句構造、談話文脈を統合する必要がある。古典的にはBroca野が統語処理に特化すると考えられたが、現在では、統語と意味は言語ネットワーク内で広く相互依存的に処理されるという見方が有力である。

Hagoortは、単語を文脈に統合する「結合問題」を言語神経科学の中心課題として整理した。文理解では、記憶から語と構文パターンを検索し、それらを現在の文脈に結びつけ、矛盾があれば再解析する。

### 3.3 予測処理

現在の言語処理研究で最も重要な概念の一つが予測である。人間は次に来る語を完全に当てる必要はないが、音韻、語、構文、意味、談話の複数レベルで確率的な期待を形成している。予測が外れたときには、N400、surprisal効果、前頭・側頭領域の活動変化として現れる。

Goldsteinらは2022年、自然な物語を聞くECoG研究で、人間の脳と自己回帰型深層言語モデルが、文脈依存の次語予測、語出現後の予測誤差、文脈埋め込みによる語表現という計算原理を共有することを示した。Caucheteuxらは2023年、304名のfMRIデータから、予測は単語直後だけでなく複数語先まで広がり、前頭・頭頂領域ほど長距離で高次の予測を担うことを示した。

### 3.4 時間スケールの階層性

言語はミリ秒単位の音響変化から、音節、単語、句、文、談話まで、多層的な時間スケールを持つ。近年のECoG研究では、言語ネットワーク内の神経集団が、およそ1語、4語、6語程度の異なる時間窓で入力を統合することが示された。この多時間スケール表現は、文脈を保持しつつ高速な語処理を行うための基盤と考えられる。

2025年の自然会話fMRI研究では、会話内容の表現が、理解と産出で共有される短時間スケールの表現と、モダリティ固有の長短異なる統合過程に分かれることが示された。会話理解では長い文脈を保持し、発話産出では短い時間窓で次の発話を計画する必要があるため、この差は理にかなっている。

### 3.5 言語産出

発話は、概念化、語彙選択、文法構成、音韻符号化、音声運動計画、発声という段階を含む。ただし、これらは完全な直列処理ではなく、自己モニタリング、予測、聞き手への適応によって相互作用する。

自然会話のECoG研究では、発話前に高次言語表現から音声・運動表現へ向かう時間的流れが観察され、理解では逆に音響・音声から言語表現へ向かう流れが観察された。これは理解と産出が同じネットワークの一部を共有しつつ、方向性と時間構造が異なることを示している。

## 4. 2020年代の最新知見

### 4.1 言語ネットワークは「自然種」として扱えるか

Fedorenko、Ivanova、Regevの2024年レビューは、言語ネットワークを、脳全体の中で比較的まとまりのある機能システムとして整理した。主張の要点は、言語ネットワークが言語に選択的で、強く相互接続され、入力・出力モダリティに依存せず、低次知覚系や汎用的推論系とは区別されるということである。

これは古典的局在論への単純な回帰ではない。むしろ、個々の「領域」ではなく、複数領域からなる機能的ネットワークを分析単位にする点が現代的である。

### 4.2 言語と思考の分離

Fedorenko、Piantadosi、Gibsonの2024年Nature論文は、言語は思考の本体ではなく、主としてコミュニケーションのための道具だと論じた。根拠として、重度失語でも非言語的推論が残る例、数学や社会推論が言語ネットワークと別ネットワークに依存する証拠、言語構造が効率的な伝達に適応している証拠が挙げられる。

この見方は「言語が思考に影響しない」という意味ではない。内言、カテゴリー化、記憶補助、文化的知識の伝達において言語は大きな役割を持つ。しかし、言語ネットワークそのものが人間のすべての思考を生成しているわけではない。

### 4.3 LLMと脳の対応

2020年代には、LLMの埋め込み表現を使って脳活動を予測する研究が急増した。Schrimpfらの2021年PNAS研究は、多様な言語モデルのうち、次語予測性能が高いモデルほど人間の神経・行動データに合いやすいことを示した。Goldsteinらの2022年ECoG研究は、GPT-2の文脈埋め込みと予測誤差が自然音声理解中の脳活動をよく説明することを示した。

2024年から2025年にかけては、対応関係がさらに細かく調べられている。Goldsteinらの2025年Nature Communications論文では、GPT-2 XLやLlama 2の層階層が、ECoGで測定した脳内の時間的処理階層に対応することが示された。つまり、モデルの深い層が、脳のより遅い・文脈的な活動に対応する傾向がある。

重要な注意点は、これらは「同じ入力を処理したときの表現の対応」であり、脳とLLMが同じ学習履歴、身体性、意図、社会的目的を持つことを意味しないことである。LLMは言語処理メカニズムを探る実験器具として有用だが、人間の理解そのものと同一視すべきではない。

### 4.4 自然会話への展開

従来の実験は、短文、単語、人工的課題に偏っていた。2025年の研究では、病院内の日常会話や実験者との自由会話を長時間記録し、自然会話中の神経活動をモデル化する方向へ進んでいる。

Goldsteinらの2025年Nature Human Behaviour論文は、4名のECoG患者から約100時間の会話データを集め、Whisperの音響・音声・言語埋め込みが、理解と産出の神経活動を階層的に説明することを示した。Caiらの2025年Nature Communications論文は、14名の頭蓋内記録から、自然会話中の発話、理解、話者交替に対応する活動が前頭・側頭領域に広く分布することを示した。

これらの研究は、言語処理を「刺激への反応」ではなく、相手と交互に意味を作る動的過程として捉える方向を強めている。

### 4.5 多言語・個人差データ

言語処理の普遍性と多様性を調べる研究も拡大している。Malik-Moraledaらは2022年、45言語・12語族を対象に、言語ネットワークの左側性、機能的統合、言語選択性が言語差を超えて比較的安定していることを示した。

2026年には、Basque-Spanish多言語環境の725名を含むNEUROLINGUAデータセットがScientific Dataで公開された。これは、年齢、習得時期、使用頻度、熟達度、社会言語学的背景が、言語ネットワークの構造・機能にどう影響するかを大規模に検討する基盤になる。ただし、公開時点では未編集版として提供されており、細部の解釈には今後の分析蓄積が必要である。

## 5. 統合モデル

現代的な人間の言語処理は、次のような連続的・相互作用的パイプラインとして捉えられる。

```mermaid
flowchart LR
  A["音声・文字・手話などの入力"] --> B["知覚処理: 音響・視覚・運動特徴"]
  B --> C["語彙アクセス: 語形・音韻・意味候補"]
  C --> D["中核的言語ネットワーク: 構文・意味の合成"]
  D --> E["談話・文脈・予測"]
  E --> D
  D --> F["知識・推論・社会認知"]
  F --> D
  D --> G["発話計画: 語彙選択・音韻符号化"]
  G --> H["運動制御・発声・手話表出"]
  H --> I["聞き手からのフィードバック"]
  I --> E
```

この図で重要なのは、処理が一方向ではない点である。文脈と予測は入力の解釈を変え、聞き手や会話状況は発話計画を変え、自分の発話を聞くことが自己モニタリングとして次の産出を調整する。

## 6. 未解決問題

第一に、脳内表現と記号的言語単位の対応はまだ完全には分かっていない。LLM埋め込みは脳活動をよく予測するが、その次元が音韻、統語、意味、語用論にどう対応するかは解釈が難しい。

第二に、予測と統合の区別が難しい。ある単語で脳活動が変化したとき、それが事前予測の失敗なのか、語を文脈へ統合する負荷なのか、記憶検索の難しさなのかを分ける必要がある。

第三に、言語ネットワークと汎用認知ネットワークの関係は課題依存である。日常会話では世界知識、社会認知、情動、注意制御が不可欠であり、実験室で同定される「中核的言語処理」と自然なコミュニケーションをどう接続するかが課題である。

第四に、個人差・多言語性・発達・加齢・神経可塑性の理解がまだ不十分である。大規模多言語データセットと個人別解析は、この問題に取り組むための重要な方向である。

第五に、因果性の検証が不足している。fMRIやLLM符号化モデルは相関を示すが、どの表現が必要条件なのかを知るには、脳刺激、病変研究、神経心理学、計算モデルの介入実験を組み合わせる必要がある。

## 7. 今後の研究方向

今後は、短文課題から自然会話へ、単一言語から多言語・方言・手話へ、平均脳から個人脳へ、相関解析から因果的介入へ進むことが重要である。また、LLMや音声モデルは、言語処理理論をテストする「比較対象」としてさらに使われるだろう。特に、モデルの予測、内部層、文脈窓、注意機構を操作し、その変化が人間の脳活動や行動とどう対応するかを調べる研究が有望である。

臨床応用では、失語症、発達性言語障害、認知症、聴覚障害、ブレイン・コンピュータ・インターフェースへの展開が期待される。自然会話を扱えるモデルと神経記録が発展すれば、単語復唱や絵名称課題だけでは見えなかった、実生活に近い言語能力を評価できる可能性がある。

## 8. 結論

人間の言語処理は、かつて考えられたような「一つの言語中枢」による処理ではない。現代の知見は、左半球優位の中核的言語ネットワークが、知覚・運動系、記憶、推論、社会認知と協調しながら、語彙、構文、意味、談話、発話計画を同時並行的に処理するという像を支持している。

最新研究の中心は、自然な言語環境で、脳がどのように文脈を蓄積し、先を予測し、相手と意味を共有するかに移っている。LLMを含む深層学習モデルは、この過程を数理的に記述する強力な道具になった。ただし、人間の言語処理は、身体、社会、目的、経験、文化の中で働くシステムであり、モデルとの対応は慎重に解釈する必要がある。

総じて、現在最も妥当な見方は、人間の言語処理を「分散ネットワーク上で進む、多時間スケールの予測的コミュニケーション処理」と捉えることである。

## 主要参考文献

- Broca, P. (1861). Remarques sur le siège de la faculté du langage articulé. Bulletin de la Société Anatomique de Paris.
- Wernicke, C. (1874). Der aphasische Symptomencomplex: Eine psychologische Studie auf anatomischer Basis.
- Kutas, M., & Hillyard, S. A. (1980). Reading senseless sentences: Brain potentials reflect semantic incongruity. Science. https://doi.org/10.1126/science.7350657
- McClelland, J. L., & Elman, J. L. (1986). The TRACE model of speech perception. Cognitive Psychology. https://doi.org/10.1016/0010-0285(86)90015-0
- Marslen-Wilson, W. D. (1987). Functional parallelism in spoken word-recognition. Cognition. https://doi.org/10.1016/0010-0277(87)90005-9
- Hickok, G., & Poeppel, D. (2004). Dorsal and ventral streams: A framework for understanding aspects of the functional anatomy of language. Cognition. https://doi.org/10.1016/j.cognition.2003.10.011
- Hickok, G., & Poeppel, D. (2007). The cortical organization of speech processing. Nature Reviews Neuroscience. https://doi.org/10.1038/nrn2113
- Hagoort, P. (2019). The neurobiology of language beyond single-word processing. Science. https://doi.org/10.1126/science.aax0289
- Huth, A. G. et al. (2016). Natural speech reveals the semantic maps that tile human cerebral cortex. Nature. https://doi.org/10.1038/nature17637
- Ding, N. et al. (2016). Cortical entrainment to hierarchical linguistic structures in natural speech. Nature Neuroscience. https://doi.org/10.1038/nn.4186
- Schrimpf, M. et al. (2021). The neural architecture of language: Integrative modeling converges on predictive processing. PNAS. https://doi.org/10.1073/pnas.2105646118
- Goldstein, A. et al. (2022). Shared computational principles for language processing in humans and deep language models. Nature Neuroscience. https://doi.org/10.1038/s41593-022-01026-4
- Malik-Moraleda, S. et al. (2022). An investigation across 45 languages and 12 language families reveals a universal language network. Nature Neuroscience. https://doi.org/10.1038/s41593-022-01114-5
- Caucheteux, C., Gramfort, A., & King, J.-R. (2023). Evidence of a predictive coding hierarchy in the human brain listening to speech. Nature Human Behaviour. https://doi.org/10.1038/s41562-022-01516-2
- Fedorenko, E., Ivanova, A. A., & Regev, T. I. (2024). The language network as a natural kind within the broader landscape of the human brain. Nature Reviews Neuroscience. https://doi.org/10.1038/s41583-024-00802-4
- Fedorenko, E., Piantadosi, S. T., & Gibson, E. A. F. (2024). Language is primarily a tool for communication rather than thought. Nature. https://doi.org/10.1038/s41586-024-07522-w
- Regev, T. I. et al. (2024). Neural populations in the language network differ in the size of their temporal receptive windows. Nature Human Behaviour. https://doi.org/10.1038/s41562-024-01944-2
- Tuckute, G. et al. (2024). Driving and suppressing the human language network using large language models. Nature Human Behaviour. https://doi.org/10.1038/s41562-023-01783-7
- Goldstein, A. et al. (2025). A unified acoustic-to-speech-to-language embedding space captures the neural basis of natural language processing in everyday conversations. Nature Human Behaviour. https://doi.org/10.1038/s41562-025-02105-9
- Cai, J. et al. (2025). Natural language processing models reveal neural dynamics of human conversation. Nature Communications. https://doi.org/10.1038/s41467-025-58620-w
- Yamashita, M., Kubo, R., & Nishimoto, S. (2025). Conversational content is organized across multiple timescales in the brain. Nature Human Behaviour. https://doi.org/10.1038/s41562-025-02231-4
- Goldstein, A. et al. (2025). Temporal structure of natural language processing in the human brain corresponds to layered hierarchy of large language models. Nature Communications. https://doi.org/10.1038/s41467-025-65518-0
- Quiñones, I. et al. (2026). Unraveling the Complexity of Multilingual Comprehension: Neuroimaging and Linguistic Profiling in 700+ Adults. Scientific Data. https://doi.org/10.1038/s41597-026-07423-9
