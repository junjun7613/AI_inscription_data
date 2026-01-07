import pandas as pd
import json
import os


def convert_tsv_to_json(tsv_path, output_path=None):
    """
    TSVファイルをフィルタリングせずにJSON形式に変換する

    Parameters:
    -----------
    tsv_path : str
        TSVファイルのパス
    output_path : str, optional
        出力JSONファイルのパス（指定しない場合は自動生成）

    Returns:
    --------
    list
        変換された碑文データのリスト
    str
        出力ファイルパス
    """
    # TSVファイルを読み込む
    print(f"TSVファイルを読み込み中: {tsv_path}")
    df = pd.read_csv(tsv_path, sep='\t')
    print(f"読み込み完了: {len(df)}件")

    # NaN値を空文字列に変換してから辞書のリストとして取得
    df_clean = df.fillna('')
    inscriptions = df_clean.to_dict('records')

    # statusフィールドを;で分割してリストに変換
    for item in inscriptions:
        if item.get('status'):
            # ;で分割し、各要素の前後の空白を削除
            status_list = [s.strip() for s in item['status'].split(';') if s.strip()]
            item['status'] = status_list
        else:
            item['status'] = []

    # 出力ファイルパスを生成
    if output_path is None:
        output_path = tsv_path.replace('.tsv', '.json').replace('data/', 'filtered_data/')

    # 出力ディレクトリが存在しない場合は作成
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"ディレクトリを作成: {output_dir}")

    # JSONファイルとして保存
    print(f"\nJSONファイルに保存中: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(inscriptions, f, ensure_ascii=False, indent=2)

    print(f"変換完了: {len(inscriptions)}件の碑文をJSONに変換しました")

    return inscriptions, output_path


if __name__ == "__main__":
    # スクリプト内でパスを指定
    input_file = 'data/2025-12-26-EDCS_via_Lat_Epig-place_Al-KhumsKhomsHomsLebdahLebidaLabdahWadiZennadWadiazZannadLeptisMagnaLepcisMagnaNeapolis-922.tsv'
    output_file = None  # Noneの場合は自動生成: filtered_data/[basename].json

    # 変換実行
    inscriptions, output_path = convert_tsv_to_json(input_file, output_file)

    # 統計情報を表示
    print("\n" + "=" * 80)
    print("統計情報:")
    print(f"総件数: {len(inscriptions)}件")
    print(f"出力ファイル: {output_path}")

    # サンプルを表示
    if inscriptions:
        print("\n最初の碑文のサンプル:")
        print("-" * 80)
        first_item = inscriptions[0]
        print(f"EDCS-ID: {first_item.get('EDCS-ID', 'N/A')}")
        print(f"Province: {first_item.get('province', 'N/A')}")
        print(f"Place: {first_item.get('place', 'N/A')}")
        print(f"Status: {first_item.get('status', 'N/A')}")
        print(f"Dating: {first_item.get('dating_from', 'N/A')} - {first_item.get('dating_to', 'N/A')}")
        print(f"\nInscription (interpretive):")
        print(first_item.get('inscription_interpretive_cleaning', 'N/A')[:200])
        if len(first_item.get('inscription_interpretive_cleaning', '')) > 200:
            print("...")
