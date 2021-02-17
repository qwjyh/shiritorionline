def iskatahira(strj):
    #日本語チェック用
    hiragana = "ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをん"
    katakana = "ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴ"

    #文字列の中身がすべてカタカナかひらがなの場合のみTrueを返す
    return all([ch in katakana or ch in hiragana for ch in strj])


def judger(word, word_list):
    # 最後の文字が「ん」「ン」
    if word[-1] == "ん" or word[-1] == "ン":
        status = 1  # 終了
        return status
    
    # 日本語チェック(かな)
    if iskatahira(word):
        # 最初の入力
        if word_list == []:    
            word_list.append(word)
            status = 0
            return status
        elif word[0] == word_list[-1][-1]:
            for words in word_list:
                # 重複チェック
                if words == word:
                    status = 3
                    return status
            # ジャッジをパス
            word_list.append(word)
            status = 0
            return status
        else:
            status = 2 # つながってない
            return status
    else:
        status = 4 # 日本語じゃない
        return status