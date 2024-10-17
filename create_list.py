## それぞれの種のリスト（ncopiesをそのまま使用）　科＞属＞種の優先順に並び替え
import pandas as pd
import os

# ファイルパスリスト
file_list = ["community_qc_fishes_japanese1.tsv",
             "community_qc_fishes_japanese2.tsv",
             "community_qc_fishes_japanese3.tsv",
             "community_qc_fishes_japanese4.tsv",
             "community_qc_fishes_japanese1_NC.tsv"]

# 出力ファイルパスリスト
output_file_path_list = ["/content/species_with_ratios1.csv",
                         "/content/species_with_ratios2.csv",
                         "/content/species_with_ratios3.csv",
                         "/content/species_with_ratios4.csv",
                         "/content/species_with_ratios1_NC.csv"]

# ネガティブコントロールファイルの読み込み
nc_file = "community_qc_fishes_japanese1_NC.tsv"
nc_df = pd.read_csv(nc_file, sep='\t')

# 'family', 'genus', 'species', 'nreads', 'ncopies' カラムの存在確認
if not {'family', 'genus', 'species', 'nreads', 'ncopies'}.issubset(nc_df.columns):
    print(f"Error: Required columns not found in negative control file: {nc_file}")
else:
    # ネガティブコントロールのデータを辞書形式で保存 (family, genus, species) -> nreads, ncopies
    nc_dict = {}
    for index, row in nc_df.iterrows():
        key = (row['family'], row['genus'], row['species'])
        nc_dict[key] = {'nreads': row['nreads'], 'ncopies': row['ncopies']}


# 各ファイルを処理
for num, file_path in enumerate(file_list):

    # ファイルの存在を確認
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        continue

    # ファイルサイズを確認
    if os.path.getsize(file_path) == 0:
        print(f"Error: File is empty: {file_path}")
        continue

    # TSVファイルを読み込む
    try:
        df = pd.read_csv(file_path, sep='\t')

        # 'family', 'genus', 'species', 'nreads' カラムの存在確認
        if {'family', 'genus', 'species', 'nreads', 'ncopies'}.issubset(df.columns):

            if file_path != nc_file:
                # ネガティブコントロールデータのリード数とコピー数を引く
                for index, row in df.iterrows():
                    key = (row['family'], row['genus'], row['species'])
                    if key in nc_dict:
                        # コピー数をネガティブコントロールの値だけ引く
                        df.at[index, 'ncopies'] -= nc_dict[key]['ncopies']

                        # マイナスになった場合はその行を削除
                        if df.at[index, 'ncopies'] <= 0:
                            df.drop(index, inplace=True)

            # 科、属、種ごとのnreadsの合計を計算
            family_genus_species_counts = df.groupby(['family', 'genus', 'species'])['ncopies'].sum().reset_index()

            # 全体に対する割合を計算
            family_genus_species_counts['ratio'] = family_genus_species_counts['ncopies'] / family_genus_species_counts['ncopies'].sum()

            # 科 → 属 → 種の順でソート
            sorted_df = family_genus_species_counts.sort_values(by=['family', 'genus', 'species'], ascending=[True, True, True])

            # 出力ファイルパス
            output_file_path = output_file_path_list[num]

            # CSVファイルに保存（UTF-8エンコーディングを使用）
            sorted_df.to_csv(output_file_path, index=False, encoding='shift-jis')

        else:
            print(f"Error: Required columns 'family', 'genus', 'species', 'ncopies', or 'nreads' not found in file: {file_path}")

    except pd.errors.EmptyDataError:
        print(f"Error: No columns to parse from file: {file_path}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


## 全体の種のリスト（ncopies使用）　　科＞属＞種を優先並び替え
# ファイルパスリスト
file_list = ["community_qc_fishes_japanese1.tsv",
             "community_qc_fishes_japanese2.tsv",
             "community_qc_fishes_japanese3.tsv",
             "community_qc_fishes_japanese4.tsv"]

# ネガティブコントロールファイルの読み込み
nc_file = "community_qc_fishes_japanese1_NC.tsv"
nc_df = pd.read_csv(nc_file, sep='\t')

# 'family', 'genus', 'species', 'nreads', 'ncopies' カラムの存在確認
if not {'family', 'genus', 'species', 'nreads', 'ncopies'}.issubset(nc_df.columns):
    print(f"Error: Required columns not found in negative control file: {nc_file}")
else:
    # ネガティブコントロールのデータを辞書形式で保存 (family, genus, species) -> nreads, ncopies
    nc_dict = {}
    for index, row in nc_df.iterrows():
        key = (row['family'], row['genus'], row['species'])
        nc_dict[key] = {'nreads': row['nreads'], 'ncopies': row['ncopies']}

# 統合データ用の辞書
family_genus_species_counts = {}

# 各ファイルからデータを読み込んで統合
for file_path in file_list:
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
    else:
        if os.path.getsize(file_path) == 0:
            print(f"Error: File is empty: {file_path}")
        else:
            try:
                df = pd.read_csv(file_path, sep='\t')

                # 'family', 'genus', 'species', 'nreads' 'ncopies'カラムの存在確認
                if {'family', 'genus', 'species', 'nreads', 'ncopies'}.issubset(df.columns):
                    # 科、属、種ごとのncopiesの集計
                    for index, row in df.iterrows():
                        key = (row['family'], row['genus'], row['species'])
                        if key in nc_dict:
                            # コピー数をネガティブコントロールの値だけ引く
                            df.at[index, 'ncopies'] -= nc_dict[key]['ncopies']

                            # マイナスになった場合はその行を削除
                            if df.at[index, 'ncopies'] <= 0:
                                df.drop(index, inplace=True)

                        family = row['family']
                        genus = row['genus']
                        species = row['species']
                        nreads = row['nreads']
                        ncopies = row['ncopies']

                        # 科、属、種の階層でデータを統合
                        key = (family, genus, species)
                        if key in family_genus_species_counts:
                            family_genus_species_counts[key] += ncopies
                        else:
                            family_genus_species_counts[key] = ncopies
                else:
                    print(f"Error: Required columns 'family', 'genus', 'species', 'ncopies', or 'nreads' not found in file: {file_path}")
            except pd.errors.EmptyDataError:
                print(f"Error: No columns to parse from file: {file_path}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

# 統合したデータから出現割合を計算
family_genus_species_series = pd.Series(family_genus_species_counts)
total_ncopies = family_genus_species_series.sum()
family_genus_species_ratios = family_genus_species_series / total_ncopies

# データフレームにまとめる
combined_df = pd.DataFrame({
    'family': [key[0] for key in family_genus_species_series.index],
    'genus': [key[1] for key in family_genus_species_series.index],
    'species': [key[2] for key in family_genus_species_series.index],
    'ncopies': family_genus_species_series.values,
    'ratio': family_genus_species_ratios.values
})

# 科、属、種の順でソート
combined_df = combined_df.sort_values(by=['family', 'genus', 'species'], ascending=[True, True, True])


# 出力ファイルパス
output_file_path = '/content/all_species_with_ratios.csv'

# CSVファイルに保存（UTF-8エンコーディングを使用）
combined_df.to_csv(output_file_path, index=False, encoding='shift-jis')

## unidentifiedの日本語訳
# 存在しない種のリスト
unidentified_list = ["unidentified Euteleosteomorpha", "unidentified Gobionellinae", "unidentified Apogoninae", "unidentified Clupeinae", "unidentified Exocoetidae", "Hemitrygon", "unidentified Labridae", "unidentified Sparidae", "unidentified Tetraodontidae", "Nipponocypris", "unidentified Cyprinoidei"]
unidentified_japanese_list = ["unidentified Euteleosteomorpha(特定できない真骨類)", "unidentified Gobionellinae(特定できないハゼ科)", "unidentified Apogoninae(特定できないテンジクダイ科)", "unidentified Clupeinae(特定できないニシン科)", "unidentified Exocoetidae(特定できないトビウオ科)", "Hemitrygon(アカエイ属)", "unidentified Labridae(特定できないベラ科)", "unidentified Sparidae(特定できないタイ科)", "unidentified Tetraodontidae(特定できないフグ科)", "Nipponocypris(カワムツ属)", "unidentified Cyprinoidei(特定できないコイ科)"]

# 変換辞書の作成
conversion_dict = dict(zip(unidentified_list, unidentified_japanese_list))

file_list = ["/content/species_with_ratios1.csv", "/content/species_with_ratios2.csv", "/content/species_with_ratios3.csv", "/content/species_with_ratios4.csv", "/content/species_with_ratios1_NC.csv", "/content/all_species_with_ratios.csv"]
output_file_path_list = ["/content/species_with_ratios1.csv", "/content/species_with_ratios2.csv", "/content/species_with_ratios3.csv", "/content/species_with_ratios4.csv", "/content/species_with_ratios1_NC.csv", '/content/all_species_with_ratios.csv']

for i in range(len(file_list)):
    file_path = file_list[i]
    output_file_path = output_file_path_list[i]
    # CSVファイルの読み込み
    df = pd.read_csv(file_path, encoding='shift-jis')

    # 名前の変換関数
    def convert_names(df, column_name):
        df[column_name] = df[column_name].apply(lambda x: conversion_dict.get(x, x))
        return df

    # 各列に対して変換を実行
    df = convert_names(df, 'family')
    df = convert_names(df, 'genus')
    df = convert_names(df, 'species')

    # 変換後のデータフレームを表示
    print(df)

    # 出力ファイルパス

    # CSVファイルに保存（UTF-8エンコーディングを使用）
    df.to_csv(output_file_path, index=False, encoding='utf-8')


## 2ページ分け　五島全体なし、index付き　　科＞属＞種付き
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, PageBreak, Paragraph
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from matplotlib import font_manager
from matplotlib.ticker import MaxNLocator
import io
import re

file_list = ["/content/species_with_ratios1.csv", "/content/species_with_ratios2.csv", "/content/species_with_ratios3.csv", "/content/species_with_ratios4.csv", "/content/species_with_ratios1_NC.csv"]
pdf_list = ['/content/species_list_with_graph1.pdf', '/content/species_list_with_graph2.pdf', '/content/species_list_with_graph3.pdf', '/content/species_list_with_graph4.pdf', '/content/species_list_with_graph1_NC.pdf']
title_list = ["環境DNA調査　五島1野々切　2020/06/12", "環境DNA調査　五島2戸岐　2020/06/12", "環境DNA調査　五島3白良ヶ浜　2020/06/12", "環境DNA調査　五島4三井楽　2020/06/12", "環境DNA調査　五島1_NC野々切　2020/06/12"]

# 日本語フォントの設定
font_path = '/content/NotoSansJP-VariableFont_wght.ttf'
italic_font_path = '/content/NotoSans-Italic-VariableFont_wdth,wght.ttf'
pdfmetrics.registerFont(TTFont('NotoSans', font_path))
pdfmetrics.registerFont(TTFont('ItalicFont', italic_font_path))

# フォントプロパティの設定を追加
font_prop = font_manager.FontProperties(fname=font_path)

def add_page_number(canvas, doc):
    page_number = canvas.getPageNumber()
    text = f"Page {page_number}"
    canvas.drawRightString(200 * mm, 15 * mm, text)  # ページ番号の位置を調整

def format_cell(value, column):
    if column == 'リード数':
        try:
            int_value = int(value)
            formatted_value = f"{int_value}"
            return Paragraph(formatted_value, style=styles['CustomNormal'])
        except ValueError:
            return Paragraph(str(value), style=styles['CustomNormal'])

    value_str = str(value)

    # ラテン語と日本語を分ける正規表現
    match = re.match(r"([^\(]+)\s*\((.+)\)", value_str)
    if match:
        latin_name = match.group(1).strip()
        japanese_text = match.group(2).strip()

        # ラテン語部分を斜体で、日本語部分を通常フォントでフォーマット
        formatted_value = f'<font name="ItalicFont">{latin_name}</font> <font name="NotoSans">({japanese_text})</font>'
        return Paragraph(formatted_value, style=styles['CustomNormal'])
    else:
        return Paragraph(value_str, style=styles['CustomNormal'])

# メインループの修正
for i in range(len(file_list)):
    file_path = file_list[i]
    pdf_file_path = pdf_list[i]
    title = title_list[i]

    # データの読み込み
    species_df = pd.read_csv(file_path, encoding='utf-8')

    # インデックスをリセットして番号を新しい列として追加
    species_df.reset_index(inplace=True, drop=True)
    species_df.index = species_df.index + 1
    species_df.reset_index(inplace=True)
    species_df.rename(columns={'index': ' 番号 '}, inplace=True)

    # '割合'を100倍にする
    species_df['ratio'] = species_df['ratio'] * 100

    # 列名を変更
    species_df.rename(columns={'family': '科', 'genus': '属', 'species': '種', 'ncopies': 'コピー数', 'ratio': '割合(%)'}, inplace=True)

    # 新しいカラム '番号_種' を作成
    species_df['番号_種'] = species_df[' 番号 '].astype(str) + ' ' + species_df['種']

    # データを2ページに分ける
    mid_index = len(species_df) // 2
    df1 = species_df.iloc[:mid_index]
    df2 = species_df.iloc[mid_index:]

    # 全データの最大割合を取得
    y_max = species_df['割合(%)'].max()

    # PDFの作成
    document = SimpleDocTemplate(pdf_file_path, pagesize=letter, title=title, onFirstPage=add_page_number, onLaterPages=add_page_number)
    elements = []

    # タイトルを追加
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='JapaneseTitle', fontName='NotoSans', fontSize=18, leading=22, spaceAfter=20))
    styles.add(ParagraphStyle(name='CustomNormal', fontName='NotoSans', fontSize=10, leading=12))
    title_paragraph = Paragraph(title, styles['JapaneseTitle'])
    elements.append(title_paragraph)

    # テーブル用のデータを整形
    table_data = species_df.drop(columns=['番号_種'])  # '番号_種' を除外
    formatted_data = [table_data.columns.tolist()] + [[format_cell(v, c) for c, v in zip(table_data.columns, row)] for row in table_data.values.tolist()]

    # テーブルの作成
    table = Table(formatted_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'NotoSans'),
        ('WIDTH', (species_df.columns.get_loc('コピー数'), 0), (species_df.columns.get_loc('コピー数'), -1), 100),
    ]))
    elements.append(table)

    # 1ページ目のグラフの作成
    fig, ax = plt.subplots(figsize=(6, 6))
    df1.plot(kind='bar', x='番号_種', y='割合(%)', ax=ax, color='skyblue')
    ax.set_ylim(0, y_max+3)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.title(f'環境DNA調査 - ページ 1', fontproperties=font_prop)
    plt.xlabel('生物の種類', fontproperties=font_prop)
    plt.ylabel('割合(%)', fontproperties=font_prop)
    plt.xticks(rotation=90, fontproperties=font_prop)
    ax.legend().set_visible(False)
    plt.tight_layout()

    # y軸の最大値を取得
    #y_max = ax.get_ylim()[1]

    # グラフを画像として保存
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()
    image_stream.seek(0)

    # グラフ画像をPDFに追加
    graph_image = Image(image_stream)
    elements.append(graph_image)

    # テーブルの下に説明を追加
    explanation = Paragraph(
        '<font name="NotoSans" size=10>注: 生物の種類は　番号　＋　種　です。</font>',
        styles['Normal']
    )
    elements.append(explanation)

    # ページ区切り
    elements.append(PageBreak())

    # 2ページ目のグラフの作成
    fig, ax = plt.subplots(figsize=(6, 6))
    df2.plot(kind='bar', x='番号_種', y='割合(%)', ax=ax, color='skyblue')
    ax.set_ylim(0, y_max+3)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.title(f'環境DNA調査 - ページ 2', fontproperties=font_prop)
    plt.xlabel('生物の種類', fontproperties=font_prop)
    plt.ylabel('割合(%)', fontproperties=font_prop)
    plt.xticks(rotation=90, fontproperties=font_prop)
    ax.legend().set_visible(False)
    plt.tight_layout()

    # グラフを画像として保存
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()
    image_stream.seek(0)

    # グラフ画像をPDFに追加
    graph_image = Image(image_stream)
    elements.append(graph_image)

    # テーブルの下に説明を追加
    explanation = Paragraph(
        '<font name="NotoSans" size=10>注: 生物の種類は　番号　＋　種　です。</font>',
        styles['Normal']
    )
    elements.append(explanation)


    # PDFを保存
    document.build(elements)

    print(f"PDF created at {pdf_file_path}")


## 3ページ分け　五島全体だけ、index付き　　科＞属＞種付き　　基準：ncopies
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, PageBreak, Paragraph
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from matplotlib import font_manager
from matplotlib.ticker import MaxNLocator
import io

file_list = ["/content/all_species_with_ratios.csv"]
pdf_list = ['/content/species_list_with_graph_all.pdf']
title_list = ["環境DNA調査　五島全体　2020/06/12"]

# 日本語フォントの設定
font_path = '/content/NotoSansJP-VariableFont_wght.ttf'
italic_font_path = '/content/NotoSans-Italic-VariableFont_wdth,wght.ttf'
pdfmetrics.registerFont(TTFont('NotoSans', font_path))
pdfmetrics.registerFont(TTFont('ItalicFont', italic_font_path))

# フォントプロパティの設定を追加
font_prop = font_manager.FontProperties(fname=font_path)

def add_page_number(canvas, doc):
    page_number = canvas.getPageNumber()
    text = f"Page {page_number}"
    canvas.drawRightString(200 * mm, 15 * mm, text)  # ページ番号の位置を調整

def format_cell(value, column):
    if column == ' 番号 ':
        try:
            int_value = int(value)
            formatted_value = f"{int_value}"
            return Paragraph(formatted_value, style=styles['CustomNormal'])
        except ValueError:
            return Paragraph(str(value), style=styles['CustomNormal'])

    value_str = str(value)

    # ラテン語と日本語を分ける正規表現
    match = re.match(r"([^\(]+)\s*\((.+)\)", value_str)
    if match:
        latin_name = match.group(1).strip()
        japanese_text = match.group(2).strip()

        # ラテン語部分を斜体で、日本語部分を通常フォントでフォーマット
        formatted_value = f'<font name="ItalicFont">{latin_name}</font> <font name="NotoSans">({japanese_text})</font>'
        return Paragraph(formatted_value, style=styles['CustomNormal'])
    else:
        return Paragraph(value_str, style=styles['CustomNormal'])


for i in range(len(file_list)):
    file_path = file_list[i]
    pdf_file_path = pdf_list[i]
    title = title_list[i]

    # データの読み込み
    species_df = pd.read_csv(file_path, encoding='utf-8')

    # インデックスをリセットして番号を新しい列として追加
    species_df.reset_index(inplace=True, drop=True)
    species_df.index = species_df.index + 1
    species_df.reset_index(inplace=True)
    species_df.rename(columns={'index': ' 番号 '}, inplace=True)

    # '割合'を100倍にする
    species_df['ratio'] = species_df['ratio'] * 100

    # 列名を変更
    species_df.rename(columns={'family': '科', 'genus': '属', 'species': '種', 'ncopies': 'コピー数', 'ratio': '割合(%)'}, inplace=True)
    #species_df['リード数'] = species_df['リード数'].astype(int)

    # 新しいカラム '番号_種' を作成
    species_df['番号_種'] = species_df[' 番号 '].astype(str) + ' ' + species_df['種']


    # データを3ページに分ける
    third_index = len(species_df) // 3
    df1 = species_df.iloc[:third_index]
    df2 = species_df.iloc[third_index:2*third_index]
    df3 = species_df.iloc[2*third_index:]

    # 全データの最大割合を取得
    y_max = species_df['割合(%)'].max()

    # PDFの作成
    document = SimpleDocTemplate(pdf_file_path, pagesize=letter, title=title, onFirstPage=add_page_number, onLaterPages=add_page_number)
    elements = []

    # タイトルを追加
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='JapaneseTitle', fontName='NotoSans', fontSize=18, leading=22, spaceAfter=20))
    styles.add(ParagraphStyle(name='CustomNormal', fontName='NotoSans', fontSize=10, leading=12))
    title_paragraph = Paragraph(title, styles['JapaneseTitle'])
    elements.append(title_paragraph)

    # テーブル用のデータを整形
    table_data = species_df.drop(columns=['番号_種'])  # '番号_種' を除外
    formatted_data = [table_data.columns.tolist()] + [[format_cell(v, c) for c, v in zip(table_data.columns, row)] for row in table_data.values.tolist()]

    # テーブルの作成
    table = Table(formatted_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'NotoSans'),
        ('WIDTH', (species_df.columns.get_loc('コピー数'), 0), (species_df.columns.get_loc('コピー数'), -1), 100),
    ]))
    elements.append(table)


    # 1ページ目のグラフの作成
    fig, ax = plt.subplots(figsize=(6, 6))
    df1.plot(kind='bar', x='番号_種', y='割合(%)', ax=ax, color='skyblue')
    ax.set_ylim(0, y_max+3)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.title(f'環境DNA調査 - ページ 1', fontproperties=font_prop)
    plt.xlabel('生物の種類', fontproperties=font_prop)
    plt.ylabel('割合(%)', fontproperties=font_prop)
    plt.xticks(rotation=90, fontproperties=font_prop)
    ax.legend().set_visible(False)
    plt.tight_layout()

    # y軸の最大値を取得
    #y_max = ax.get_ylim()[1]

    # グラフを画像として保存
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()
    image_stream.seek(0)

    # グラフ画像をPDFに追加
    graph_image = Image(image_stream)
    elements.append(graph_image)

        # テーブルの下に説明を追加
    explanation = Paragraph(
        '<font name="NotoSans" size=10>注: 生物の種類は　番号　＋　種　です。</font>',
        styles['Normal']
    )
    elements.append(explanation)

    # ページ区切り
    elements.append(PageBreak())

    # 2ページ目のグラフの作成
    fig, ax = plt.subplots(figsize=(6, 6))
    df2.plot(kind='bar', x='番号_種', y='割合(%)', ax=ax, color='skyblue')
    ax.set_ylim(0, y_max+3)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.title(f'環境DNA調査 - ページ 2', fontproperties=font_prop)
    plt.xlabel('生物の種類', fontproperties=font_prop)
    plt.ylabel('割合(%)', fontproperties=font_prop)
    plt.xticks(rotation=90, fontproperties=font_prop)
    ax.legend().set_visible(False)
    plt.tight_layout()

    # グラフを画像として保存
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()
    image_stream.seek(0)

    # グラフ画像をPDFに追加
    graph_image = Image(image_stream)
    elements.append(graph_image)

    # テーブルの下に説明を追加
    explanation = Paragraph(
        '<font name="NotoSans" size=10>注: 生物の種類は　番号　＋　種　です。</font>',
        styles['Normal']
    )
    elements.append(explanation)

    # ページ区切り
    elements.append(PageBreak())

    # 3ページ目のグラフの作成
    fig, ax = plt.subplots(figsize=(6, 6))
    df3.plot(kind='bar', x='番号_種', y='割合(%)', ax=ax, color='skyblue')
    ax.set_ylim(0, y_max+3)  # y軸の範囲を1ページ目と合わせる
    #ax.yaxis.set_major_locator(MaxNLocator(integer=True))  # y軸を整数に設定
    plt.title(f'環境DNA調査 - ページ 3', fontproperties=font_prop)
    plt.xlabel('生物の種類', fontproperties=font_prop)
    plt.ylabel('割合(%)', fontproperties=font_prop)
    plt.xticks(rotation=90, fontproperties=font_prop)
    # 凡例を消す
    ax.legend().set_visible(False)
    plt.tight_layout()

    # グラフを画像として保存
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()
    image_stream.seek(0)

    # グラフ画像をPDFに追加
    graph_image = Image(image_stream)
    elements.append(graph_image)

    # テーブルの下に説明を追加
    explanation = Paragraph(
        '<font name="NotoSans" size=10>注: 生物の種類は　番号　＋　種　です。</font>',
        styles['Normal']
    )
    elements.append(explanation)

    # PDFを保存
    document.build(elements)

    print(f"PDF created at {pdf_file_path}")