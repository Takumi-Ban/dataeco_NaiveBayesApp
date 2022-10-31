import numpy as np
import pandas as pd
import MeCab
import pickle
from dbsetting import Engine
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB

class Model:
    def __init__(self):
        return

    # 文章から単語を取り出す
    def parsewithelimination(self, sentense):
        m=MeCab.Tagger()
        m.parse('')
        node=m.parseToNode(sentense)
        
        result=np.array([])
        while node:
            if node.feature.split(',')[6] == '*': # 原形を取り出す
                term=node.surface
            else :
                term=node.feature.split(',')[6]
                
            if node.feature.split(',')[1] in ['数','非自立','接尾']:
                node=node.next
                continue

            if node.feature.split(',')[0] in ['名詞', '動詞', '形容詞']:
                result=np.append(result, term)
                
            node=node.next

        return result

    # 単語を抽出しdfに格納する
    def create_df(self, df):
        for i in range(df.shape[0]):
            result = self.parsewithelimination(df.iloc[i, 1])
            word = ''
            for w in result:
                word += w
                word += ' '
            df.iloc[i, 1] = word
        return


    def create_model(self):
        sql = 'SELECT class, text FROM outline;'
        df = pd.read_sql(sql, Engine)
        self.create_df(df)

        # train, validationにデータを分ける
        X = pd.DataFrame(df['text'])
        y = pd.DataFrame(df['class'])
        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, test_size=0.3)

        # 単語の出現回数を数える
        vec_cnt = CountVectorizer(min_df=2)
        vec_cnt.fit(X_train['text'])

        # ベクトル化
        X_train_vec = vec_cnt.transform(X_train['text'])
        X_test_vec = vec_cnt.transform(X_test['text'])

        # モデルの作成
        model = BernoulliNB()
        model.fit(X_train_vec, y_train['class'])

        # 精度検証
        train_acc = model.score(X_train_vec, y_train)
        test_acc = model.score(X_test_vec, y_test)

        # モデルの保存
        with open('vec.pickle', mode='wb') as fp1:
            pickle.dump(vec_cnt, fp1)
        with open('model.pickle', mode='wb') as fp2:
            pickle.dump(model, fp2)
        return train_acc, test_acc

    # モデルで予測
    def predict(self, in_):
        # 作成済みモデルの読み込み
        with open('vec.pickle', mode='rb') as fp1:
            loaded_vec = pickle.load(fp1)
        with open('model.pickle', mode='rb') as fp2:
            loaded_model = pickle.load(fp2)
        df_in = pd.DataFrame([{'class': 'pred', 'text': in_}])
        self.create_df(df_in)
        in_vec = loaded_vec.transform(df_in['text'])
        
        # 予測
        pred = loaded_model.predict(in_vec)
        return pred[0]