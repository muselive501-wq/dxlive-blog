import os
from datetime import datetime

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | DXLIVE FAN BLOG</title>
    <meta name="description" content="{description}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>

<body>
    <header class="navbar">
        <div class="header-container">
            <a href="index.html" class="logo">DXLIVE<span>FAN BLOG</span></a>
            <button class="hamburger" id="hamburger-btn" aria-label="メニュー"><span></span><span></span><span></span></button>
            <nav class="nav-links">
                <a href="index.html">Home</a>
                <a href="category.html?type=news">News</a>
                <a href="category.html?type=creators">Creators</a>
                <a href="category.html?type=events">Events</a>
                <a href="category.html?type=knowhow">ノウハウ</a>
            </nav>
        </div>
    </header>
    <div class="mobile-overlay" id="mobile-overlay"></div>

    <main class="main-content">
        <article class="section-container article-body" style="background: var(--bg-secondary); padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
            <div class="article-meta" style="margin-bottom: 20px; color: var(--text-tertiary); font-size: 0.9rem;">
                <a href="index.html" style="color: var(--text-tertiary); text-decoration: none;">Home</a> > {category}
                <div style="margin-top: 10px;">{date}</div>
            </div>
            
            <h1 style="font-size: 2rem; margin-bottom: 30px; line-height: 1.4; color: var(--text-primary);">{title}</h1>
            <img src="{image_path}" alt="アイキャッチ画像" class="article-image" style="margin-top: 1.5rem; margin-bottom: 2rem;">

{content}

            <div style="margin-top: 50px; text-align: center; padding: 40px; background: rgba(255, 42, 85, 0.1); border-radius: 12px; border: 1px solid rgba(255, 42, 85, 0.3);">
                <h3 style="color: var(--accent-primary); margin-bottom: 15px; font-size: 1.5rem;">＼今すぐ無料で試してみる／</h3>
                <p style="margin-bottom: 25px; color: var(--text-secondary);">DXLIVEに無料登録して、今すぐ最高のライブチャット体験を始めよう！</p>
                <a href="https://www.dxlive.com" target="_blank" class="read-more" style="font-size: 1.2rem; padding: 15px 40px;">公式サイト（仮）へ</a>
            </div>
        </article>
    </main>

    <footer>
        <div class="footer-content">
            <a href="index.html" class="footer-logo">DXLIVE<span>FAN BLOG</span></a>
            <p>© 2026 DXLIVE FAN BLOG. All Rights Reserved.</p>
            <div class="footer-nav" style="margin-top: 1rem;">
                <a href="about.html" style="color: var(--text-secondary); margin: 0 10px;">About / Disclaimer</a>
            </div>
        </div>
    </footer>
    <script>(function(){{var h=document.getElementById("hamburger-btn"),n=document.querySelector(".nav-links"),o=document.getElementById("mobile-overlay");if(!h||!n||!o)return;function t(){{h.classList.toggle("active");n.classList.toggle("open");o.classList.toggle("active")}}h.addEventListener("click",t);o.addEventListener("click",t);n.querySelectorAll("a").forEach(function(l){{l.addEventListener("click",function(){{if(n.classList.contains("open"))t()}})}})}})();</script>
</body>
</html>
"""

ARTICLES = [
    {
        "filename": "rumors-and-legality.html",
        "title": "【徹底検証】DXLIVEは危険？違法？5chやTwitterの口コミから安全性と実態を暴く",
        "description": "DXLIVEの安全性、違法性、詐欺の噂を2ch/5ch/Twitterの口コミと運営実態から徹底検証。安心して遊ぶためのポイントを解説します。",
        "category": "安全性レビュー",
        "image_path": "assets/images/eyecatch_rumors_legality.png",
        "content": """
            <h2>DXLIVEは危険？違法？結論から言うと「極めて安全」</h2>
            <p>「DXLIVEって本当に安全なの？」「詐欺サイトじゃないの？」と不安に思う方もいるかもしれません。結論から申し上げますと、<strong>DXLIVEは法的に全く問題がない、極めて安全な合法ライブチャットサイト</strong>です。</p>
            <p>運営歴20年以上の実績があり、セキュリティ対策も万全。悪質な詐欺サイトによくある「サクラ」や「架空請求」といったトラブルは一切報告されていません。日本の法律を遵守しており、違法性はありませんので、安心して楽しむことができます。</p>
            <img src="assets/images/beginner_guide.png" alt="安全性の説明" class="article-image">

            <h2>5ch・Twitter（X）のリアルな口コミと評判</h2>
            <p>ネット掲示板（2ch/5ch）やSNS（Twitter/X）でのリアルな声を調査しました。良い口コミとしては「素人の女の子が多くてリアル」「画質が他のサイトより圧倒的に良い」「サポートの返信が早い」といった声が目立ちます。</p>
            <p>一方で、「お気に入りの子がすぐ辞めてしまった」「料金が少し高い」といったネガティブな意見も見られました。しかし、これらはサイトの安全性や違法性に関わるものではなく、サービスに対する個人の感想レベルに留まっています。詐欺被害などの報告は確認できませんでした。</p>

            <h2>なぜ「怪しい」「詐欺」と検索されるのか？</h2>
            <p>では、なぜ検索候補に「怪しい」「危険」といった言葉が出てくるのでしょうか。その理由は主に以下の2点です。</p>
            <ul>
                <li style="margin-bottom: 10px;"><strong>ライブチャット業界全体のイメージ：</strong> 一部の悪質な出会い系サイトや詐欺サイトの存在により、「ライブチャット＝怪しい」という先入観を持つ人が多いため。</li>
                <li style="margin-bottom: 10px;"><strong>利用前の不安による検索：</strong> 初めて課金するユーザーが、安全を確認するためにあえて「DXLIVE 詐欺」「DXLIVE 違法」とネガティブなキーワードで検索するため（サジェスト汚染）。</li>
            </ul>
            <p>つまり、実際に被害に遭ったから検索されているのではなく、<strong>「安全かどうか確認したい」という心理が検索結果に表れているだけ</strong>なのです。信頼できる運営会社（DTI）が提供しているため、個人情報の漏洩や不正請求の心配はありません。</p>
        """
    },
    {
        "filename": "recording-rules.html",
        "title": "要注意！DXLIVEでの録画・スクショはバレる？規約違反のペナルティとルール",
        "description": "DXLIVE（デラックスライブ）の配信録画やスクリーンショット撮影の可否について。バレる仕組みやアカウント凍結などのペナルティを解説。",
        "category": "利用ルール",
        "image_path": "assets/images/eyecatch_recording.png",
        "content": """
            <h2>DXLIVEでの録画・スクショは「絶対NG」</h2>
            <p>お気に入りのキャストとの配信中、「この可愛い瞬間を保存したい！」と思うことは誰にでもあるでしょう。しかし、結論から言うと、<strong>DXLIVEでは一切の録画・スクリーンショット（画面キャプチャ）が利用規約で固く禁止されています</strong>。</p>
            <p>これはキャストのプライバシーと著作権、肖像権を守るための非常に重要なルールです。個人的な手段で保存する目的であっても、システムの規約上許されていません。</p>
            <img src="assets/images/camera_icon_bg.png" alt="スクショ禁止のイメージ" class="article-image">

            <h2>録画やスクショは運営やキャストに「バレる」のか？</h2>
            <p>「スマホの標準機能ならバレないのでは？」「PCのキャプチャソフトを使えば平気だろう」と考えるのは非常に危険です。DXLIVEのシステムは高度化されており、特定のキャプチャ動作などを検知する仕組みが導入されている可能性があります。</p>
            <p>また、悪意を持って録画した動画を無断でネット上にアップロードした場合、デジタルウォーターマーク（電子透かし）などの技術により、誰のアカウントから流出したかが特定されるリスクもあります。バレないだろうという油断は禁物です。</p>

            <h2>発覚した場合のペナルティ（アカウント凍結・法的措置）</h2>
            <p>録画やスクショ行為が発覚した場合、以下のような厳しいペナルティが課せられます。</p>
            <ul>
                <li style="margin-bottom: 10px;"><strong>即時アカウント凍結・強制退会：</strong> 警告なしでアカウントが停止され、二度とログインできなくなります。</li>
                <li style="margin-bottom: 10px;"><strong>保有ポイントの没収：</strong> 購入していたポイントはすべて無効となり、返金は一切されません。</li>
                <li style="margin-bottom: 10px;"><strong>法的措置：</strong> 悪質な動画の拡散などが行われた場合、運営またはキャストから損害賠償請求や刑事告訴が行われる可能性があります。</li>
            </ul>
            <p>一時の出来心で、多大なリスクを負うことになります。DXLIVEは「その場限りのリアルタイムな交流」を楽しむツールです。ルールとマナーを守って、キャストと気持ちの良い時間を過ごしましょう。</p>
        """
    },
    {
        "filename": "advanced-techniques.html",
        "title": "DXLIVEの裏技テクニック！多窓・ミッション攻略・キャストが喜ぶ会話術",
        "description": "DXLIVEをもっと楽しむための中・上級者向け裏技ガイド。複数視聴（多窓）のやり方やミッションによるポイント稼ぎ、モテる会話術を公開。",
        "category": "攻略テクニック",
        "image_path": "assets/images/eyecatch_advanced.png",
        "content": """
            <h2>効率よくポイント獲得！ミッション（デイリー・ウィークリー）攻略</h2>
            <p>DXLIVEを無課金・微課金で長く楽しむための最大の裏技が「ミッション機能」の活用です。結論として、<strong>毎日ログインして簡単なタスクをこなすだけで、1ヶ月にかなりの無料ポイントを貯めることができます。</strong></p>
            <p>「3人の配信を視聴する」「特定のスタンプを送る」「プロフィールを更新する」など、負担の少ないデイリーミッションを毎日確実にクリアしましょう。また、週末限定のボーナスミッションなどは獲得ポイントが大きいため、見逃さない工夫（リマインダー設定など）が重要です。</p>
            <img src="assets/images/campaign_info.png" alt="ミッション攻略" class="article-image">

            <h2>一度に複数人を楽しむ「多窓（複数視聴）」のやり方と注意点</h2>
            <p>「推し候補の女の子がたくさんいて絞れない！」という場合におすすめなのが、PCブラウザを活用した「多窓（複数視聴）」テクニックです。ブラウザのタブやウィンドウを複数開き、同時に複数のパーティーチャットを視聴することができます。（※スマホでは原則不可）</p>
            <p><strong>注意点：</strong>多窓視聴は、同時に複数の視聴料金（1分あたりのポイント×人数分）が発生します。「無料視聴期間だけ多窓でチェックし、一番好みの女の子の部屋に絞る」という使い方が最もコスパの良い裏技です。また、PCのスペックによっては画面が重くなるため、画質設定を調整しましょう。</p>

            <h2>キャストに名前を覚えてもらえる！モテる「会話術とコメント」</h2>
            <p>何千人といる視聴者の中で、キャストに特別扱いされるための「会話術」を紹介します。重要なのは、<strong>他の人が言わない「具体的な褒め言葉」と「プロフィールへの言及」</strong>です。</p>
            <ul>
                <li style="margin-bottom: 10px;"><strong>NGな例：</strong> 「かわいいね」「何してるの？」「脱いで」などの定型文・要求。</li>
                <li style="margin-bottom: 10px;"><strong>OKな例：</strong> 「ネイル変えた？ピンク似合ってるね」「プロフに猫好きって書いてたけど、うちも飼ってるんだ！」など、彼女自身に関心があることを示すコメント。</li>
            </ul>
            <p>まずは「挨拶＋1アクション（具体的な質問や褒め言葉）」から始め、彼女が話しやすいパスを出すことで、圧倒的に好感度が上がり、2ショットチャットへの誘導もスムーズになります。</p>
        """
    },
    {
        "filename": "coupons-and-benefits.html",
        "title": "【損しない】DXLIVEのクーポン＆ありがとうポイント完全活用ガイド",
        "description": "DXLIVEの料金を極限まで安くする！割引クーポンやキャンペーン情報、長く続けるほどお得になる「ありがとうポイント」の仕組みを解説。",
        "category": "料金・ポイント",
        "image_path": "assets/images/eyecatch_coupons.png",
        "content": """
            <h2>見逃し厳禁！お得な「割引クーポン・キャンペーン」の特徴</h2>
            <p>DXLIVEで通常料金のままポイントを購入するのは非常にもったいないです。結論から言うと、<strong>定期的に開催されるキャンペーンや割引クーポンを狙い撃ちすることで、実質半額近くで遊ぶことが可能</strong>です。</p>
            <p>特に狙い目なのは以下のタイミングです。ゲリラ的に開催される「ポイント増量キャンペーン（例：10,000円購入で+30%ボーナス）」や、長期休暇（GW、お盆、年末年始）に配布されるメルマガ限定クーポンです。必ずメール通知をONにしておき、これらのタイミングでポイントを「まとめ買い」するのが最強の節約術です。</p>
            <img src="assets/images/pricing_guide.png" alt="クーポンのイメージ" class="article-image">

            <h2>「ありがとうポイント」とは？継続利用で得するVIP制度</h2>
            <p>DXLIVEには、使えば使うほど還元される「ありがとうポイント」という独自のマイレージ制度が存在します。これは、ポイントを消費してチャットを利用したり、ギフトを贈ったりするたびに一定の割合で自動的に貯まっていくポイントです。</p>
            <p>貯まったありがとうポイントは、通常の視聴ポイントに交換することができます。長く遊んでいる常連ユーザーほど、この還元率の恩恵を大きく受けられる仕組みになっており、他社サイトに乗り換えるよりも圧倒的にお得に継続利用できる理由の1つとなっています。</p>

            <h2>無料でポイント（無料チップ）をゲットする小ワザ</h2>
            <p>課金しなくても得られる「無料ポイント」も存在します。最も有名なのは「新規登録ボーナス」ですが、それ以外にも以下のような方法で獲得できます。</p>
            <ul>
                <li style="margin-bottom: 10px;"><strong>ログインルーレット：</strong> 1日1回挑戦できるルーレットで、数百ポイントが当たるチャンス。</li>
                <li style="margin-bottom: 10px;"><strong>プロフィールの充実：</strong> 自身のアバター設定や自己紹介文を100%入力することで貰える達成ボーナス。</li>
                <li style="margin-bottom: 10px;"><strong>不具合報告・アンケート回答：</strong> 運営からのアンケートに協力することで謝礼として付与されるケース。</li>
            </ul>
            <p>少額ですが、塵も積もれば山となります。2ショットチャットの「あと1分延長したい！」という場面で役立つため、コツコツ貯めておくことをおすすめします。</p>
        """
    },
    {
        "filename": "competitor-comparison.html",
        "title": "DXLIVE vs 人気ライブチャット5社（SakuraLive・Mライブ等）徹底比較！",
        "description": "デラックスライブは他と比べてどう？SakuraLive、Mライブ、STRIPCHAT、ライブJASMINなどの国内外有名サイトと画質・料金・キャストの質で徹底比較。",
        "category": "サイト比較",
        "image_path": "assets/images/eyecatch_comparison_ext.png",
        "content": """
            <h2>【結論】日本人向けの使いやすさと画質なら「DXLIVE」一択</h2>
            <p>数あるライブチャットサイトの中でどこを選ぶべきか迷っている方へ。結論から言うと、<strong>「日本人キャストの多さ」「高画質・遅延の少なさ」「サイトの使いやすさ（UI）」の総合力において、DXLIVEは国内トップクラス</strong>です。</p>
            <p>海外発の安価なサイトもありますが、コミュニケーションの取りやすさや、日本人好みの清楚系・素人系・人妻系のキャストを探すのであれば、DXLIVEを選んで間違いはありません。</p>
            <img src="assets/images/comparison.png" alt="比較の結論" class="article-image">

            <h2>国内ライバル比較：DXLIVE vs SakuraLive / Mライブ / 感熟ライブ</h2>
            <p>まずは国内向けに展開している主要ライバルサイトと比較してみましょう。</p>
            <ul>
                <li style="margin-bottom: 10px;"><strong>vs SakuraLive（サクラライブ）：</strong> どちらも老舗ですが、DXLIVEの方がモダンなインターフェースでスマホ操作に優れています。また、素人系の在籍率はDXLIVEに軍配が上がります。</li>
                <li style="margin-bottom: 10px;"><strong>vs Mライブ：</strong> Mライブはアイドル系が強いですが、DXLIVEは「清楚」から「アダルト・過激」までジャンルの幅広さが特徴。料金体系はDXLIVEの方が若干リーズナブルに設定されています。</li>
                <li style="margin-bottom: 10px;"><strong>vs 感熟ライブ：</strong> 人妻・熟女に特化した感熟ライブに対し、DXLIVEも実は人妻系のレベルが非常に高いです。DXLIVEなら若者から熟女まで1サイトでカバーできるのが強みです。</li>
            </ul>

            <h2>海外巨大サイト比較：DXLIVE vs STRIPCHAT / ライブJASMIN</h2>
            <p>次に、世界最大規模の海外発ライブチャットとの比較です。</p>
            <p><strong>STRIPCHAT（ストリップチャット）やライブJASMIN（LiveJasmin）</strong>は、世界中から何万人ものモデルが配信しており、非常に過激で料金も安い（チップ制など）のが魅力です。しかし、英語でのコミュニケーションが必須となる場面が多く、日本人モデルは圧倒的少数です。</p>
            <p>「言葉の壁を気にせず、日本語で深いコミュニケーションを取りたい」「日本人ならではの細やかな気遣いやエロティックなやり取りを楽しみたい」という方には、やはり完全日本語対応のDXLIVEが圧倒的におすすめです。目的（とにかく過激な映像が見たいか、会話を楽しみたいか）に合わせて使い分けるのが正解です。</p>
        """
    },
    {
        "filename": "genre-guide.html",
        "title": "【マニア必見】素人・人妻から無修正まで！DXLIVEのジャンル別キャストの探し方",
        "description": "素人、人妻、コスプレ、巨乳などフェティッシュな欲求を満たすDXLIVEのジャンル検索攻略法。おすすめの探し方を紹介します。",
        "category": "キャスト紹介",
        "image_path": "assets/images/eyecatch_genre.png",
        "content": """
            <h2>圧倒的人気！「素人・人妻・美少女」の探し方と選び方</h2>
            <p>DXLIVE最大の魅力は、プロの役者ではない「一般の女の子（素人・人妻・学生）」とリアルな会話ができる点です。結論として、<strong>「新人ランキング」と「詳細検索のタグ絞り込み」を駆使するのが最高の出逢いへの近道</strong>です。</p>
            <p>「素人ぽさ」を求めるなら、登録して2週間以内の「新人（New）」マークがついた子を狙いましょう。まだ配信に慣れていない初々しさが楽しめます。「人妻・熟女」好きの方は、検索条件で『年齢30代〜40代』『昼間の時間帯に配信している子』をソートすると、旦那が不在の間にこっそり配信しているリアルな主婦とマッチングしやすくなります。</p>
            <img src="assets/images/popular_casts.png" alt="ジャンル検索" class="article-image">

            <h2>フェチに刺さる「巨乳・コスプレ・外国人」の発掘術</h2>
            <p>特定のフェティッシュな属性を持つキャストも多数在籍しています。「詳細検索」のフリーワード機能が大活躍します。</p>
            <ul>
                <li style="margin-bottom: 10px;"><strong>巨乳・爆乳：</strong> 身長・体重・スリーサイズ（バスト）の条件を指定して検索。「Gカップ以上」などのタグも有効です。</li>
                <li style="margin-bottom: 10px;"><strong>コスプレ・制服：</strong> 「ナース」「JK」「メイド」などのキーワードで検索。週末の夜はコスプレ配信が増える傾向にあります。</li>
                <li style="margin-bottom: 10px;"><strong>外国人（ハーフ）：</strong> 「英語OK」「留学経験」や、国名で検索。異国情緒あふれるエキゾチックな体験が可能です。</li>
            </ul>

            <h2>無修正や過激なアダルト要素はどこまでOK？</h2>
            <p>過激な配信を期待するユーザーから「無修正は見れるの？」「オナニー配信はある？」といった疑問が多く寄せられます。</p>
            <p>明確なルールとして、DXLIVEは日本の法律に基づいて運営されているため、<strong>日本国内で違法となる「完全無修正」のポルノ配信は禁止されており、存在しません。</strong></p>
            <p>しかし、下着姿、セクシーなコスプレ、音声やアングルを駆使した非常にエロティックで過激なパフォーマンス（バイブ連動機能などを用いた疑似体験）は豊富に提供されています。法律の範囲内で最大限のスリルと「リアルタイムの興奮」を味わえるのがDXLIVEの強みです。</p>
        """
    },
    {
        "filename": "high-quality-settings.html",
        "title": "映像が重い・カクつく？DXLIVEの高画質化と快適設定＆トラブルシューティング",
        "description": "DXLIVEの配信画質を最高にする設定方法と、「重い」「映像が止まる」「カクつく」といった頻出トラブルの解決策をネットワーク・端末側の視点から解説。",
        "category": "トラブル解決",
        "image_path": "assets/images/eyecatch_quality.png",
        "content": """
            <h2>最高画質で楽しむための「画質設定」の基本</h2>
            <p>DXLIVEは業界最高水準の高画質（HD・フルHD相当）配信に対応しています。しかし、デフォルト設定のままではそのポテンシャルを引き出せていない可能性があります。結論、<strong>視聴画面右下の「設定（歯車アイコン）」から、手動で画質を『高画質（High）』に変更すること</strong>をおすすめします。</p>
            <p>自動（Auto）の設定になっていると、通信状況に応じて画質が下がってしまうことがあります。Wi-Fi環境が安定している自宅などで視聴する場合は、常に最高画質に固定設定しておくことで、キャストの表情や肌の質感まで鮮明に楽しむことができます。</p>
            <img src="assets/images/troubleshooting.png" alt="画質設定" class="article-image">

            <h2>「重い」「映像がカクつく・止まる」原因と対処法</h2>
            <p>いざ高画質に設定した、あるいは週末の夜など混雑する時間帯に「映像がカクつく」「音声がズレる・止まる」といった症状が出た場合の対処法です。</p>
            <ul>
                <li style="margin-bottom: 10px;"><strong>ブラウザのキャッシュクリア：</strong> 最も多い原因です。ブラウザ（ChromeやSafari）の閲覧履歴とキャッシュ画像を削除し、再起動してください。</li>
                <li style="margin-bottom: 10px;"><strong>別のブラウザを試す：</strong> 特定のブラウザ（例：旧式のEdgeやアドオンを多数入れたChrome）と相性が悪い場合があります。シークレットモードを利用するのも有効です。</li>
                <li style="margin-bottom: 10px;"><strong>画質を一時的に下げる：</strong> あなたの家のWi-Fi回線やスマホの通信速度が一時的に低下している可能性があります。その場合は「低画質」に落として配信がスムーズになるか確認してください。</li>
            </ul>

            <h2>スマホ・PCデバイスのスペック要件について</h2>
            <p>サイト側のサーバー問題ではなく、使用しているスマートフォンやPCのスペック不足が原因で重くなっているケースも少なくありません。</p>
            <p>快適に視聴するための推奨環境は、スマートフォンであれば比較的新しいモデル（iPhoneなら11以降、Androidなら直近3〜4年以内のミドルスペック以上）が理想です。また、バックグラウンドで多数のアプリが起動しているとメモリ不足に陥るため、DXLIVEを視聴する前は他のアプリを完全に終了（タスクキル）させておくのが裏技的な快適設定です。</p>
        """
    },
    {
        "filename": "support-and-refund.html",
        "title": "困った時のDXLIVE対応表！ログイン忘れ・ポイント返金・退会後のトラブル",
        "description": "DXLIVE退会後のデータはどうなる？間違えて買ったポイントは返金できる？パスワードを忘れた場合のログイン方法やサポートへの問い合わせ先まとめ。",
        "category": "トラブル解決",
        "image_path": "assets/images/eyecatch_support.png",
        "content": """
            <h2>パスワード・IDを忘れてログインできない時の解決手順</h2>
            <p>久しぶりにDXLIVEにログインしようとしたら、IDやパスワードを忘れてしまった…というトラブルは非常に多いです。結論、<strong>焦って新規アカウントを作り直す前に（規約違反の複数アカウント所持になるため）、「パスワードをお忘れの方」リンクを利用しましょう。</strong></p>
            <p>ログイン画面の下部にあるリンクから、登録した覚えのあるメールアドレスを入力して送信ボタンを押します。正しいメアドであれば、数分以内にパスワード再設定の認証メールが届きます。「どのメアドで登録したかも忘れた」という場合は、サイト下部の「お問い合わせ」から、サポートに直接連絡して本人確認を行う必要があります。</p>
            <img src="assets/images/privacy_rules.png" alt="ログイン問題" class="article-image">

            <h2>間違えて購入した！ポイントの「返金」は可能？</h2>
            <p>「操作ミスで高額なポイントプランを購入してしまった」「少し使ったけどもう利用しないから残りのポイントを払い戻してほしい」というケースについて。</p>
            <p>結論として、<strong>DXLIVEの利用規約上、デジタルコンテンツという性質上、一度購入したポイントの返品・返金・現金化は【例外なく一切不可】</strong>となっています。クーリングオフの対象外です。そのため、ポイントを購入する前は金額の桁や支払い方法に間違いがないか、必ず確認画面でダブルチェックする癖をつけてください。</p>

            <h2>退会後のアカウントデータと「再登録」について</h2>
            <p>退会手続きを完了した後のデータや、再び遊びたくなった時の再登録に関する疑問にお答えします。</p>
            <ul>
                <li style="margin-bottom: 10px;"><strong>退会後の個人情報：</strong> 退会が完了すると、プロフィール情報やお気に入り登録、メッセージ履歴、保有ポイントはすべて完全に消去されます。（復旧は不可能です）</li>
                <li style="margin-bottom: 10px;"><strong>退会完了のメールが届かない：</strong> メールが迷惑フォルダに入っているか、退会手続きの最後の「確定ボタン」を押し忘れている可能性があります。マイページでもう一度確認してください。</li>
                <li style="margin-bottom: 10px;"><strong>再登録は可能？：</strong> もちろん同じメールアドレスで後日「再登録」することは可能です。ただし、新規登録ボーナスなどを目的とした悪質な短期間での退会・登録の繰り返しはシステムで弾かれます。</li>
            </ul>
        """
    }
]

for article in ARTICLES:
    # Set date to 2026.03.10
    html_content = HTML_TEMPLATE.format(
        title=article["title"],
        description=article["description"],
        category=article["category"],
        date="2026.03.10",
        image_path=article["image_path"],
        content=article["content"]
    )
    with open(article["filename"], "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated {article['filename']}")

print("Successfully generated 8 articles.")
