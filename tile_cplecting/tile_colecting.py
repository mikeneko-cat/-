import android_auto_play_opencv as am
from random import randint as ran
import glob

adbpath = 'C:/Users/seiki/anaconda3/envs/python_vscode/'


def main():
    
    aapo = am.AapoManager(adbpath)
    x=0
    while True:
        # 画面キャプチャ
        aapo.screencap()

        #ゲーム画面制御---------------------
            #広告特典の購入
        if aapo.touchImg('tile_cplecting\\data\\gameplay\\kounyuu.png'):
            aapo.sleep(10)
            #タイトル画面のスタートボタン
        if aapo.touchImg('tile_cplecting\\data\\gameplay\\PLAY.png'):     
            aapo.sleep(3)

            #ポップアップの閉じるボタン
        if aapo.touchImg('tile_cplecting\\data\\gameplay\\toziru.png'):
            aapo.sleep(3)
        
            #ポップアップの閉じるボタン
        if aapo.touchImg('tile_cplecting\\data\\gameplay\\resutart.png'):
            aapo.sleep(3)

            #ゲームスタートボタン
        if aapo.touchImg('tile_cplecting\\data\\gameplay\\gamestart2.png'):
            aapo.sleep(10)
        
            #playstoreに飛んだ時
        if aapo.chkImg('tile_cplecting\\data\\gameplay\\playstore.png'):
            aapo.inputkeyevent(4)
            aapo.sleep(3)
            if aapo.touchImg('tile_cplecting\\data\\gameplay\\gamestart.png'):
                aapo.sleep(5)

            #webサイトに飛んだ時
        if aapo.chkImg('tile_cplecting\\data\\gameplay\\web.png'):
            aapo.inputkeyevent(4)
            aapo.sleep(3)
            if aapo.touchImg('tile_cplecting\\data\\gameplay\\gamestart.png'):
                aapo.sleep(5)
        
        if aapo.touchImg('tile_cplecting\data\\ads\\ad18.png'):
            aapo.sleep(1)
        
        #ゲームプレイ--------------------
        if aapo.chkImg('tile_cplecting\\data\\gameplay\\playgamen.png'):
            tiles=glob.glob('tile_cplecting\\data\\tiles\\*.png')
            for tile in tiles:
                ret, poss = aapo.chkImg2(tile,_multi = True)
                if ret:
                    if len(poss) >= 3:
                        for i in range(3):
                            aapo.touchPos(poss[i][0], poss[i][1])
                        x=0
                        aapo.sleep(1)
                        aapo.screencap()
                    pass
            x+=1
        
            if x >=2:
                if aapo.touchImg('tile_cplecting\\data\\gameplay\\shaful.png'):
                    aapo.sleep(2)
                    aapo.screencap()
                    aapo.touchImg('tile_cplecting\\data\\gameplay\\usecoin.png')


        #それ以外の時
        else:
            #広告対策--------------------------
            ads=glob.glob('tile_cplecting\\data\\ads\\*.png')
            for ad in ads:
                if aapo.touchImg(ad):
                    aapo.sleep(3)
    
        aapo.sleep(1)
            

if __name__ == '__main__':
    main()