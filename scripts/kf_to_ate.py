#!/bin/python
"""
Convert Kansei Hagaki II csv format to Hajimeteno Jushoroku csv
"""

import argparse
import csv
import sys

sys.stdout.reconfigure(encoding='utf8')

KF2ATE_MAP = {
    '識別番号'             : None,
    '氏名'                 : '名前'    , #  名前をセットします。（例':  #山田  太郎 
    'フリガナ'             : 'カナ'    , #  カナをセットします。（例':  #ﾔﾏﾀﾞ ﾀﾛｳ）
    '生年月日'             : '生年月日', #  生年月日をセットします。  （例':  # 2002/02/11）※２
    'コールサイン'         : None,
    '会員コード'           : None,
    '敬称'                 : '敬称'    , #  敬称をセットします。（例':  #様、殿、御中、先生）※１
    '年賀フラグ'           : None,
    '暑中フラグ'           : None,
    'クリスマスフラグ'     : None,
    '喪中フラグ'           : None,
    '連名'                 : '備考１'  , #  備考をセットします
    '自宅郵便番号'         : '郵便番号', #  郵便番号をセットします。  （例':  #123-4567）
    '自宅住所１'           : '住所１'  , #  住所をセットします。（例':  #札幌市中央区旭ケ丘１２３－４）
    '自宅住所２'           : '住所２'  , #  住所をセットします。（住所１の長い場合、残りの住所）
    '自宅電話番号'         : '電話番号', #  電話番号をセットします。（例':  #012-34-5678）
    '自宅Ｆａｘ番号'       : 'ＦＡＸ'  , #  ＦＡＸ番号をセットします。（例':  #012-34-6789）
    '個人携帯電話'         : '携帯番号', #  携帯番号をセットします。（例':  #123-45-6789）
    '個人メールアドレス'   : 'メール'  , #  メールをセットします。（例':  #n_sakurai@ma3.justnet.ne.jp）
    '個人ホームページ'     : 'ＨＰ'    , #  ＨＰのＵＲＬをセットします。
    '勤務先フリガナ'       : None,
    '勤務先名'             : None,
    '勤務先郵便番号'       : None,
    '勤務先住所１'         : None,
    '勤務先住所２'         : None,
    '部署名'               : None,
    '役職名'               : None,
    '勤務先電話番号'       : None,
    '勤務先Ｆａｘ番号'     : None,
    '勤務先携帯電話番号'   : None,
    '勤務先内線番号'       : None,
    '勤務先メールアドレス' : None,
    '勤務先ホームページ'   : None,
    '実家郵便番号'         : None,
    '実家住所１'           : None,
    '実家住所２'           : None,
    '実家電話番号'         : None,
    '実家Ｆａｘ番号'       : None,
    '実家携帯電話番号'     : None,
    '備考'                 : None,
    '登録年月日'           : None,
    '更新年月日'           : None,
    # Unassigned ATE fields,
    # '性別'    , #  性別をセットします。（例':  #男  女）※１
    # '都道府県', #  都道府県をセットします。（例':  #東京都、大阪府）
    # '大分類',   #  大分類をセットします。（マスタで登録した項目名をセットします。）
    }

FIXED_MAP = {
    '宛名区分':  '0', #  宛名の場合'0'  差出人の場合'1'をセットします。
    '印字区分':  '1', #  印字するレコードの場合'1'  しない場合'0'をセットします。
}

ATE_ITEMS = [
    '宛名区分', '印字区分', '名前', 'カナ', '敬称', '性別', '生年月日', '郵便番号', '都道府県', '住所１', '住所２',
    '電話番号', 'ＦＡＸ', '携帯番号', 'メール', 'ＨＰ', '大分類', '小分類', '小分類２', '備考１', '備考２', '顔写真', '更新日', '登録日'
]

def kf_csv_sanity_check(kf_csv_header):
    for val in kf_csv_header:
        assert val in KF2ATE_MAP, f'Unknown field "{val}"'


def kf_to_ate_line(header, kf_line):
    ret = ['' for k in ATE_ITEMS]

    # Fixed field
    for key, val in FIXED_MAP.items():
        ret[ATE_ITEMS.index(key)] = val

    # Copy corresponding fields
    for i, key in enumerate(header):
        if key in KF2ATE_MAP and KF2ATE_MAP[key] is not None:
            ret[ATE_ITEMS.index(KF2ATE_MAP[key])] = kf_line[i]

    return ret

def kf_to_ate_csv(kf_csv, ate_csv):
    if ate_csv is None:
        ate_of = sys.stdout
    else:
        ate_of = open(ate_csv, "w", encoding='shift_jis', newline='')

    ate_writer = csv.writer(ate_of)

    with open(kf_csv, encoding='shift_jis') as kf_if:
        kf_reader = csv.reader(kf_if)
    
        header = [v for v in kf_reader.__next__()]
        kf_csv_sanity_check(header)

        ate_writer.writerow(ATE_ITEMS)
        for kf_line in kf_reader:

            ate_writer.writerow(kf_to_ate_line(header, kf_line))


def main():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("-i", "--input", metavar="kf_csv", required=True,
                        help="Kansei Hagaki csv file")
    parser.add_argument("-o", "--output", metavar="kf_csv", default=None,
                        help="Hajimeteno Jushoroku csv (usnig stdout if omitted)")

    args = parser.parse_args()

    kf_to_ate_csv(args.input, args.output)

    return


if __name__ == "__main__":
    sys.exit(main())
